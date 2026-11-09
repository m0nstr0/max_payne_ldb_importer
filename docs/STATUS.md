# Importer status

## 2026-11-09 — review_and_refactoring

Baseline `ca0e4ff`; [review](REVIEW.md) records confirmed defects and remaining
limits. Reader refactoring isolates KF2-family payloads, validates primitive I/O,
retains unsupported chunks and Skin ranges, corrects LDB2 unsigned indices/prefab
grammar and propagates file errors. Maya changes fix translator selection,
dense influence mapping, cancellation/cleanup and texture cache/alpha handling.

Own PCX and SCX/RIX3 decoders replace the external image package. Both embedded
LDB textures and KF2 external diffuse images use dependency-free TGA conversion.
Original game files remain unchanged; no game-format writer was added.
SCX native-static evidence covers exact MP1/MP2 DLL builds, with raw responses
retained locally; [specification](specification/IMAGES.MD) records identities.

Verification:45 headless tests, syntax checks and diff whitespace check pass.
Hash-checked parsing:3094 KF2/KFS +116 SKD +56 LDB (28 MP1/28 MP2), zero failures.
The baseline fails371 of those KF2/KFS inputs.18 supplied loose PCX images have
identical dimensions/RGBA to the pre-existing C++ reference decoder. Compact
receipts are in this directory; detailed manifests/logs are retained locally.
CI is configured for Python 3.7/3.9/3.10/3.12; its outcome is separate from local
Python 3.15 execution and must be read from the PR checks.

Remaining: live Maya qualification, native-equivalent animation sampling,
parent-order-independent hierarchy construction, multi-object Skin mapping and
unimplemented scene components; see [TODO](../TODO.md). Two hash-matched MP2
originals remain unlocated. No loose SCX original was available, so its pixel
tests use constructed fixtures. Compressed/planar ColoRIX is unsupported.
