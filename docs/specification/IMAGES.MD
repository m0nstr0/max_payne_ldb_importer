# PCX and Max Payne SCX images

2026-11-09. The SDK decodes images using Python's standard library and writes
uncompressed 32-bit TGA for Maya. Stored game image bytes are never rewritten.
External KF2 PCX/SCX copies go to the Maya project's
`sourceimages/max_payne_import/`; embedded LDB images go to the selected export
directory. Source PCX/SCX files remain unchanged.

## PCX

Reader: `max_payne_sdk/images/pcx.py`. The 128-byte ZSoft header defines a
little-endian image rectangle, bits per plane, number of planes and bytes per
scanline per plane. Padding is removed after decoding complete scanlines.

Supported: uncompressed and byte-RLE data; indexed/planar 1/2/4-bit layouts
addressing the 16-color header palette; indexed 8-bit with the final `0c` plus
768-byte RGB palette; and three-plane 8-bit RGB. Version0 monochrome uses black
and white. Pixel indices are assembled least-significant plane first. RLE uses
the high two bits `11` and a six-bit run count; zero runs, missing values and
scanline overruns fail. RGBA output is row-major with alpha255.

Unsupported layouts, missing palettes, invalid pitch/rectangle, truncated data
and excessive storage fail explicitly. This is not a claim to support every
historical PCX variant. 18 supplied loose PCX images match the existing workspace
`BakeTexture.hpp::decodePcx` decoder in every RGBA byte (compared by FNV64 and
dimensions); the receipt also records input and RGBA SHA256.

## SCX / RIX3

Max Payne's SCX loader consumes the linear indexed ColoRIX layout:

| Offset | Bytes | Meaning |
| --- | --- | --- |
| 0 | 4 | ASCII `RIX3` |
| 4 | 2 | little-endian unsigned width |
| 6 | 2 | little-endian unsigned height |
| 8 | 2 | ColoRIX metadata; ignored by the traced native loaders |
| 10 | 768 | 256 RGB palette entries, three bytes each |
| 778 | width*height | row-major unsigned palette indices |

Each output color channel is `(paletteByte << 2) & 255`. In particular 63 maps
to252, not255. Native pixels are BGR in four-byte slots; the SDK exposes RGBA,
then its TGA encoder writes BGRA with top-left origin and alpha255. Alpha255 is
explicit in MP1's allocation path; the SDK uses opaque alpha for SCX RGB images.

Reader: `max_payne_sdk/images/scx.py`. It checks the signature, complete palette,
dimensions and pixel storage. It accepts the linear storage byte9=0; compressed,
planar and extended ColoRIX storage is explicitly unsupported. This validation
is stricter than native, which reads the fixed layout without inspecting those
metadata bytes or receiving an input length. Byte8 remains uninterpreted.

Native static evidence, Ghidra12.1.4 / REA6.7.0:

| Module | SHA256 | Loader address | Evidence |
| --- | --- | --- | --- |
| MP1 grphmfc.dll | `8f38a7ebeb2d4be3eece73e3d9b805d863c17ed58c3b0e94a33da8297b51e5f5` | `10004d30` | `ev_d68c12833daf3081109d4414e80362d97c4c64d2fe1b80f609452bb18a7ccfed` |
| MP2 grphmfc.dll | `bcfa8ffc237bbc267c68859f5b4891ae92fa6380d0f71acd3d8c52f0bd9def25` | `10007160` | `ev_19b1e6c517d04784aa717ff8464c0e203f1c7b61ecd82064761c4d8b5325adab` |

Both exports are `?loadSCX@G_Image@@IAEXPAD@Z`. MP1's disassembly independently
confirms reads at4/6, palette at10, indices at30a and channel shifts at4f38/42/4c.
Its comparison literal at1001560c is `RIX3`; MP2's pseudocode resolves it directly.
These are observations of these DLL builds, not a dynamic native/Maya test.
Constructed fixtures cover colors, row order, dimensions and malformed storage;
no loose original SCX image was available in the inspected resource trees.
