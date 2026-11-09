"""Dependency-free texture decoders and Maya-compatible image output."""
from dataclasses import dataclass
import struct

from max_payne_sdk.binary import FormatError


MAX_PIXELS = 16 * 1024 * 1024


@dataclass
class RgbaImage:
    width: int
    height: int
    pixels: bytes  # top-to-bottom rows, interleaved RGBA8

    def __post_init__(self):
        check_dimensions(self.width, self.height)
        if len(self.pixels) != self.width * self.height * 4:
            raise FormatError("RGBA buffer does not match image dimensions")


def check_dimensions(width, height):
    if width <= 0 or height <= 0 or width * height > MAX_PIXELS:
        raise FormatError("Invalid or excessive image dimensions: %dx%d" % (width, height))


def encode_tga(image):
    """Uncompressed 32-bit TGA, top-left origin, eight alpha bits."""
    if image.width > 65535 or image.height > 65535:
        raise FormatError("Image dimensions exceed TGA limits")
    header = struct.pack('<BBBHHBHHHHBB', 0, 0, 2, 0, 0, 0, 0, 0,
                         image.width, image.height, 32, 0x28)
    pixels = bytearray(image.pixels)
    pixels[0::4], pixels[2::4] = image.pixels[2::4], image.pixels[0::4]
    return header + pixels
