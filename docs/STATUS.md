# Importer status

## 2026-11-14 — sequential LDB2 prefab validation

Both the Python and canonical C++ readers now reject a skipped nonnegative
prefab ID before reading its flags or geometry. Negative IDs remain unregistered;
sequential registration, template reuse and unique-render behavior are preserved.
47 Python tests and compileall pass. Three focused C++ tests pass, and all
28 retained original MP2 files pass C++ read/write byte identity and isolated
float edits. The old readers fail the new skipped-ID regression controls.

The C++ code belongs to the separate formats project. Its exact tested source
and test delta, input/output hashes and validation details are available in
[the validation report](research/PREFAB_VALIDATION.md). No game DLL or on-disk
layout changed. The earlier implementation-gap statement below is superseded.
Python corpus replay:56/56 original LDB files (28MP1/28MP2),0 failures;
all source hashes are unchanged.

## 2026-11-14 — MP2 source comparison

KF2 now documents Helper, MP2 track conversion, coefficient playback,
normalization modes and scale restoration. LDB2 adds selected revision gates,
sequential prefab registration, volume decoding/sampling and dynamic-animation
translation distance units. Runtime ObjectBase/Exit state has a separate page;
no LDB/LV2 fields were inferred from state chunks or runtime class names.

Source hashes and retained finite-control boundaries are in
[the source review](research/MP2_SOURCE_REVIEW.md). No implementation, binary
layout, game DLL or Maya behavior changed. A skipped-prefab-ID validation gap
in both readers is recorded in TODO; old-revision readers remain unsupported.
Documentation checks cover links/anchors, fences, plain-English pages, excluded
references and whitespace. This follows merged PR21 on review_and_refactoring.

## 2026-11-09 — specification refresh

All 11 specification pages now use consistent, plain English. The former empty
MP2 LDB page has the revision-34 section order, shared-pool message grammar,
render/collision records, masks, volume cells, prefab rules and graph layouts.
New MP1 LVL and MP2 LV2 pages describe editable-level storage separately from
compiled levels and the currently supported Maya inputs. KF2/KFS/SKD and shared
types were revised; the MP1 LDB page now explains BSP index domains, ordered
tree traversal, finite sphere/capsule tests, material masks and result codes.

The specifications omit analysis-tool names and links. Existing research
history remains outside these format pages. Field orders were checked against
the canonical workspace specifications and the relevant readers/writers;
relative links, heading anchors, code fences, English-only text and whitespace
were checked. No implementation or serialized byte layout changed, so no new
Maya/game run or corpus replay is claimed. Unknown legacy layouts and consumer
limits remain explicit. See [format index](specification/INDEX.MD).

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
