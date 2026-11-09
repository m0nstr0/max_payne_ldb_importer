import struct
import unittest
import tempfile
from pathlib import Path

from max_payne_sdk.binary import FormatError
from max_payne_sdk.images import RgbaImage, encode_tga
from max_payne_sdk.images.pcx import decode_pcx
from max_payne_sdk.images.scx import decode_scx
from max_payne_sdk.images.export import prepare_texture, convert_texture_file


def pcx(width, height, bits, planes, pitch, pixels, palette=None, compressed=False):
    header = bytearray(128)
    header[:4] = bytes((10, 5, int(compressed), bits))
    struct.pack_into('<4H', header, 4, 2, 3, width + 1, height + 2)
    header[65] = planes
    struct.pack_into('<H', header, 66, pitch)
    header[16:64] = bytes(range(48))
    return bytes(header) + pixels + (b'\x0c' + palette if palette is not None else b'')


def palette256():
    return b''.join(bytes((index, 255 - index, index // 2)) for index in range(256))


def scx(width=2, height=2, storage=0):
    palette = bytearray(768)
    palette[3:9] = bytes((63, 32, 1, 0, 16, 48))
    return b'RIX3' + struct.pack('<HHBB', width, height, 0xaf, storage) + palette + bytes((1, 2, 2, 1))


class ImageTests(unittest.TestCase):
    def test_pcx_indexed8_padding_and_origin(self):
        image = decode_pcx(pcx(2, 2, 8, 1, 4, bytes((1, 2, 99, 99, 3, 4, 99, 99)), palette256()))
        self.assertEqual((2, 2), (image.width, image.height))
        self.assertEqual(bytes((1, 254, 0, 255, 2, 253, 1, 255,
                                3, 252, 1, 255, 4, 251, 2, 255)), image.pixels)

    def test_pcx_rle_escape_and_runs(self):
        image = decode_pcx(pcx(4, 1, 8, 1, 4, b'\xc1\xc0\xc3\x02', palette256(), True))
        self.assertEqual(bytes((192, 63, 96, 255)) + bytes((2, 253, 1, 255)) * 3, image.pixels)

    def test_pcx_rgb_planar(self):
        image = decode_pcx(pcx(2, 1, 8, 3, 2, bytes((255, 1, 0, 2, 3, 4))))
        self.assertEqual(bytes((255, 0, 3, 255, 1, 2, 4, 255)), image.pixels)

    def test_pcx_low_bit_palette_and_planar_order(self):
        for bits, planes, raw, expected in ((1, 1, b'\x80', [1, 0]),
                                           (2, 1, b'\x60', [1, 2]),
                                           (4, 1, b'\x12', [1, 2]),
                                           (1, 4, b'\x80\x40\x00\x80', [9, 2])):
            image = decode_pcx(pcx(2, 1, bits, planes, 1, raw))
            with self.subTest(bits=bits, planes=planes):
                self.assertEqual(b''.join(bytes((i * 3, i * 3 + 1, i * 3 + 2, 255))
                                           for i in expected), image.pixels)

    def test_pcx_bad_headers_palette_and_rle(self):
        malformed = [b'', b'\x0a' * 127,
                     pcx(2, 1, 8, 1, 2, b'\x01\x02'),
                     pcx(2, 1, 8, 1, 1, b'\x01', palette256()),
                     pcx(2, 1, 8, 1, 2, b'\xc0\x01', palette256(), True),
                     pcx(2, 1, 8, 1, 2, b'\xc3\x01', palette256(), True),
                     pcx(2, 1, 8, 1, 2, b'\xc2', palette256(), True),
                     pcx(2, 1, 8, 4, 2, b'\x00' * 8)]
        for index, data in enumerate(malformed):
            with self.subTest(case=index), self.assertRaises(FormatError):
                decode_pcx(data)

    def test_pcx_run_must_not_cross_row(self):
        with self.assertRaises(FormatError):
            decode_pcx(pcx(2, 2, 8, 1, 2, b'\xc4\x00', palette256(), True))

    def test_scx_rix3_palette_shift_and_row_order(self):
        image = decode_scx(scx())
        a, b = bytes((252, 128, 4, 255)), bytes((0, 64, 192, 255))
        self.assertEqual(a + b + b + a, image.pixels)

    def test_scx_rejects_unknown_storage_and_truncation(self):
        for data in (b'', b'RIX3', scx()[:777], scx()[:-1], scx(width=0),
                     scx(storage=0x80), scx(storage=1), b'BAD!' + scx()[4:]):
            with self.subTest(length=len(data)), self.assertRaises(FormatError):
                decode_scx(data)

    def test_image_limits_before_allocation(self):
        for data in (scx(width=65535, height=65535),):
            with self.assertRaises(FormatError):
                decode_scx(data)

    def test_tga_bgra_channels_alpha_and_top_left_origin(self):
        image = RgbaImage(1, 2, bytes((1, 2, 3, 4, 10, 20, 30, 40)))
        output = encode_tga(image)
        self.assertEqual((1, 2), struct.unpack_from('<HH', output, 12))
        self.assertEqual((32, 0x28), tuple(output[16:18]))
        self.assertEqual(bytes((3, 2, 1, 4, 30, 20, 10, 40)), output[18:])

    def test_rgba_size_validation(self):
        with self.assertRaises(FormatError):
            RgbaImage(2, 2, b'bad')

    def test_embedded_texture_conversion_dispatch(self):
        for data, extension in ((scx(), 'scx'),
                                (pcx(1, 1, 8, 1, 1, b'\x01', palette256()), 'PCX')):
            converted, ext = prepare_texture(data, extension)
            self.assertEqual('tga', ext)
            self.assertEqual(2, converted[2])
        self.assertEqual((b'unchanged', 'dds'), prepare_texture(b'unchanged', 'dds'))

    def test_external_texture_conversion_keeps_source_and_reuses_copy(self):
        with tempfile.TemporaryDirectory(dir=Path.cwd()) as temporary:
            root = Path(temporary)
            source = root / 'source.SCX'
            source.write_bytes(scx())
            output = root / 'maya' / 'sourceimages'
            result = convert_texture_file(source, output)
            self.assertEqual(output, Path(result).parent)
            self.assertEqual(encode_tga(decode_scx(scx())), Path(result).read_bytes())
            self.assertEqual(result, convert_texture_file(source, output))
            self.assertEqual(scx(), source.read_bytes())
            self.assertEqual(str(root / 'image.dds'), convert_texture_file(root / 'image.dds', output))


if __name__ == '__main__':
    unittest.main()
