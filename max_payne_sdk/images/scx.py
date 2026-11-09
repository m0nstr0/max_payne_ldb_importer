"""Max Payne's SCX path: linear indexed ColoRIX RIX3 with a VGA palette.

The native MP1 loader reads a 10-byte header, 768 palette bytes and w*h
indices. It expands palette channels by shifting left two bits, not by 255/63.
Compressed/planar ColoRIX variants are outside this consumer's format.
"""
import struct

from max_payne_sdk.binary import FormatError
from max_payne_sdk.images import RgbaImage, check_dimensions


def decode_scx(data):
    if len(data) < 778 or data[:4] != b'RIX3':
        raise FormatError("Invalid SCX/RIX3 header or palette")
    width, height = struct.unpack_from('<HH', data, 4)
    check_dimensions(width, height)
    if data[9] != 0:
        raise FormatError("Unsupported compressed/planar SCX storage type")
    size = width * height
    if len(data) < 778 + size:
        raise FormatError("Truncated SCX pixel indices")
    palette = [bytes(((data[10 + index * 3] << 2) & 255,
                       (data[11 + index * 3] << 2) & 255,
                       (data[12 + index * 3] << 2) & 255, 255))
               for index in range(256)]
    pixels = b''.join(palette[index] for index in data[778:778 + size])
    return RgbaImage(width, height, pixels)
