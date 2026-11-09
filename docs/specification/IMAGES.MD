# PCX and Max Payne SCX images

The SDK decodes PCX and SCX using Python's standard library and writes
uncompressed 32-bit TGA for Maya. Embedded LDB images go to the chosen export
folder. Converted external KF2 diffuse images go to the Maya project's
`sourceimages/max_payne_import/` folder. Original image bytes are not rewritten.
Other image formats are passed through when no conversion is needed.

## PCX

The first 128 bytes are the ZSoft header. The image rectangle uses four
little-endian u16 values: xmin, ymin, xmax and ymax. Width and height are the
inclusive differences. Header byte 3 is bits per plane, byte 65 is the plane
count, and the u16 at byte 66 is bytes per scanline per plane.

Supported layouts are:

- Indexed or planar 1-, 2- and 4-bit data using the 16-color header palette.
- Indexed 8-bit data with a final byte 0c and a 768-byte RGB palette.
- Three-plane 8-bit RGB data.

Uncompressed data and byte RLE are supported. An RLE prefix has both high bits set;
its low six bits give the run length, followed by the repeated byte. Zero
runs, missing values and scanline overruns are errors. Decode a complete row
including plane padding, then remove padding when assembling the image.
Plane 0 contributes the least significant index bits. The 8-bit RGB layout
stores red, green and blue planes, not interleaved pixels.

Version 0 monochrome uses black and white. Other unsupported historical
layouts are rejected. Missing palettes, invalid rectangles or pitch, truncated
pixels and excessive allocation sizes also fail explicitly. Output is RGBA
in top-to-bottom row order, with alpha 255.

The supplied 18 loose PCX images match the existing C++ reference decoder in
dimensions and RGBA output. The validation receipt records input and output
hashes. This is separate from checking those images in a live Maya scene.

## SCX / RIX3

The Max Payne image loader uses a linear indexed ColoRIX layout:

| Offset | Bytes | Meaning |
| --- | ---: | --- |
| 0 | 4 | ASCII RIX3 |
| 4 | 2 | Little-endian unsigned width |
| 6 | 2 | Little-endian unsigned height |
| 8 | 2 | ColoRIX metadata; ignored by the inspected game loaders |
| 10 | 768 | 256 RGB palette entries |
| 778 | width*height | Row-major u8 palette indices |

Each output channel is `(paletteByte << 2) & 255`. A palette value of 63
therefore becomes 252, not 255. The game's color slots store BGR; the SDK
returns RGBA with opaque alpha. The same signature, offsets and channel
expansion occur in the inspected MP1 and MP2 loaders.

The decoder checks the signature, complete palette, dimensions and pixel
storage. It accepts linear storage byte 9 equal to 0. Compressed, planar and
extended ColoRIX storage is unsupported. Byte 8 is retained as uninterpreted
metadata. These checks are stricter than the fixed-layout game loaders, which
do not receive an input length or interpret these metadata bytes.

Constructed tests cover colors, row order, dimensions and invalid storage.
No loose original SCX image was available in the inspected resource trees.
The supported layout should not be read as a promise to decode every
historical ColoRIX variant.

## TGA output

The output uses image type 2, 32 bits per pixel and no color map. The descriptor
is 28 hexadecimal: top-left origin and eight alpha bits. Pixels are BGRA bytes.
Widths and heights use the TGA u16 fields. Conversion rejects excessive image
sizes before allocating the pixel buffer. Writing this derived image does not
change the stored source texture's format code or payload.
