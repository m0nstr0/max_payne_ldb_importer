# Review and refactoring — 2026-11-09

Reviewed baseline: `ca0e4ff03adaccb54c6eec9c47b8391b83995e7e` (`master`).
Scope: MP1/MP2 LDB, KF2/KFS/SKD SDK readers, Maya translator selection,
skin weights, texture export and cancellation. Existing public reader names
remain available. This plugin imports assets; it does not write game formats.

## Confirmed findings and changes

| Priority | Baseline behavior | Result / regression coverage |
| --- | --- | --- |
| P1 | KF2 readers ignored chunk sizes; skipped light/environment payloads became the next header, and nested Mesh parsing crossed container boundaries. | One envelope reader, exact header reads, payload-isolated nested readers, full consumption checks; unsupported IDs retain header/raw bytes. Sibling/truncation/unknown-child tests. |
| P1 | Opacity Texture parsing depended on the bump flag. | Independent flags; all four bump/opacity combinations tested. |
| P1 | Skin import mixed SKD bone IDs, sparse cluster plug IDs and dense influence positions, with duplicate/misaligned indices and weights. | Explicit dense physical ordering from `influenceObjects()`, complete zero-filled rows, duplicate source influences accumulated. Missing/ambiguous scene mappings fail explicitly. |
| P1 | LDB2 repeated prefab parsing branched on useLightmaps and could read nonexistent collision bodies. | The final prefab flag controls unique render data; collision templates remain shared. Four independent flag combinations are tested. The historical `share_collision` public field name is retained, with corrected semantics documented. |
| P1 | LDB2 raw triangle indices were signed16. | Unsigned16 indices; values 32768/40000/65535 tested. Collision material bytes are unsigned too. |
| P2 | Truncated integers silently decoded shorter data; negative collection counts skipped sections; UTF-8-only strings rejected narrow asset names. | Shared exact reads and nonnegative collection counts; string-length tag validation and reversible Latin-1 byte view. Encoding is not claimed to be universally Latin-1. |
| P2 | I/O errors returned partial documents; LDB2 signature/pool offsets were unchecked; trailing data was ignored. | Errors propagate; LDB versions/signature, pool bounds/NUL and document EOF are checked. Pool sentinel -1 maps to an empty string. |
| P2 | MP1 Mesh v0 was rejected; an unused normal-calculation pass divided by zero on degenerate faces. | Admit the documented v0 container, remove the unused computation. This does not implement smoothing-aware normals. |
| P2 | Camera/MaterialList returned child versions; duplicate Geometry dataclass shadowed the first. | Preserve enclosing versions; keep one Geometry definition. |
| P2 | Both Maya translators claimed every file; empty folder selections indexed an empty list; progress divided by zero or cancellation continued into later phases. | Extension-specific identification, safe empty selection, zero-op progress and exception-based cancellation with `finally` cleanup. No success notification after cancellation. |
| P2 | PCX required an external imaging dependency; SCX produced an empty material. | Own PCX/SCX decoders and 32-bit TGA output, shared by LDB extraction and KF2 external diffuse textures. No third-party Python image dependency. |
| P2 | Texture cache conflated identical paths with different image bytes; diffuse and explicit alpha could connect the same destination twice. | Cache includes destination, type and content hash. An explicit alpha texture takes precedence; deterministic output suffixes. |

## Evidence and verification

Run the dependency-free suite and syntax checks:

```console
python -m unittest discover -s tests -v
python -m compileall -q max_payne_sdk max_payne_maya max_payne_sdk_ldb_importer.py max_payne_sdk_kf2_importer.py
```

CI runs the same checks on Python 3.7, 3.9, 3.10 and 3.12. Local test evidence
uses the Python version recorded in the corpus receipts; CI results must be
reported separately from local execution.

The hash-checked KF2/KFS/SKD comparison uses the same retained inventories:
the baseline fails 371 KF2/KFS files, while the reviewed reader parses all
3094 KF2/KFS and 116 SKD. See [baseline](corpus-baseline.json) and
[reviewed reader](corpus-validation.json). This is a parsing check, not proof of
Maya scene fidelity or native animation/skinning equivalence.

LDB qualification and image qualification are recorded in separate receipts.
All 56 hash-matched LDB inputs pass parsing through EOF:28 MP1 and28 MP2;
[receipt](ldb-corpus-validation.json). Two MP2 originals (Upper East Side and
Police Station) were not located with their retained hashes and remain outside
this qualification. No generated replacement was substituted for them.
Input paths whose bytes differ from retained original hashes are rejected before
parsing. Original game resources are not included in this repository.

SCX structure is independently confirmed in the original MP1 and MP2
`grphmfc.dll` loaders through REA/Ghidra, with instruction-level corroboration
for MP1. See [image specification](specification/IMAGES.MD) and its module hashes
and Evidence IDs. Raw decompiler output is retained locally, not distributed.
The 18 supplied loose PCX textures decode to the same dimensions/RGBA as the
pre-existing workspace C++ decoder; [receipt](pcx-corpus-validation.json).
No original loose SCX samples were found: SCX tests are constructed fixtures
based on the native consumer layout. Compressed/planar ColoRIX is rejected.

Maya's physical influence-index contract is documented by
[Autodesk](https://help.autodesk.com/cloudhelp/2024/ENU/MAYA-API-REF/cpp_ref/class_m_fn_skin_cluster.html).
The pure weight mapper and mocked progress command boundaries have headless
tests. A live Maya installation was unavailable; actual DAG operations,
skinCluster binding and viewport output remain unqualified.

## Remaining work

[TODO.md](../TODO.md) separates confirmed missing Maya features from unknown
native semantics. In particular, animation sampling is still a stepped preview;
Node construction assumes parent-first order; multi-object skins require an
explicit mesh/range mapping; camera import is a stub. Cancellation stops future
work but retains already-created nodes/files. These are documented follow-ups,
not claims of completed native-equivalent import.
