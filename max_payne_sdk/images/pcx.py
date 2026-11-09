"""ZSoft PCX: indexed/planar 1/2/4-bit, indexed 8-bit and planar RGB8."""
import struct

from max_payne_sdk.binary import FormatError
from max_payne_sdk.images import RgbaImage, check_dimensions


def decode_pcx(data):
    if len(data) < 128 or data[0] != 0x0a or data[2] not in (0, 1):
        raise FormatError("Invalid PCX header")
    xmin, ymin, xmax, ymax = struct.unpack_from('<4H', data, 4)
    if xmax < xmin or ymax < ymin:
        raise FormatError("Invalid PCX image rectangle")
    width, height = xmax - xmin + 1, ymax - ymin + 1
    check_dimensions(width, height)
    bits, planes = data[3], data[65]
    pitch = struct.unpack_from('<H', data, 66)[0]
    rgb = bits == 8 and planes == 3
    indexed = bits in (1, 2, 4, 8) and 1 <= planes <= 4 and bits * planes <= 8
    if not (rgb or indexed) or pitch * 8 < width * bits:
        raise FormatError("Unsupported PCX pixel layout or scanline pitch")
    row_size = pitch * planes
    if row_size * height > 64 * 1024 * 1024:
        raise FormatError("Excessive PCX scanline storage")

    end = len(data)
    if bits == 8 and planes == 1:
        if end < 128 + 769 or data[end - 769] != 0x0c:
            raise FormatError("Missing PCX 256-color palette")
        palette = data[-768:]
        end -= 769
    elif indexed:
        if bits * planes > 4:
            raise FormatError("PCX header palette cannot address more than 16 colors")
        palette = data[16:64]
        if data[1] == 0 and bits == 1 and planes == 1:
            palette = b'\x00\x00\x00\xff\xff\xff' + palette[6:]
    else:
        palette = b''

    output = bytearray(width * height * 4)
    position = 128
    mask = (1 << bits) - 1
    for y in range(height):
        row = bytearray()
        while len(row) < row_size:
            if position >= end:
                raise FormatError("Truncated PCX scanline")
            value = data[position]
            position += 1
            count = 1
            if data[2] == 1 and value & 0xc0 == 0xc0:
                count = value & 0x3f
                if count == 0 or position >= end:
                    raise FormatError("Invalid PCX RLE packet")
                value = data[position]
                position += 1
            if count > row_size - len(row):
                raise FormatError("PCX RLE packet exceeds scanline")
            row.extend(bytes([value]) * count)
        for x in range(width):
            at = (y * width + x) * 4
            if rgb:
                output[at:at + 4] = bytes((row[x], row[pitch + x], row[2 * pitch + x], 255))
            else:
                index = 0
                for plane in range(planes):
                    value = row[plane * pitch + (x * bits) // 8]
                    index |= ((value >> (8 - bits - (x * bits) % 8)) & mask) << (plane * bits)
                output[at:at + 4] = palette[index * 3:index * 3 + 3] + b'\xff'
    return RgbaImage(width, height, bytes(output))
