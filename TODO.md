# Importer follow-up

- [ ] Complete the remaining format descriptions before claiming broader
  support: legacy LVL edge/UV branches, older LV2 document/entity profiles and
  the exact version-2 selection collection. These are unknown or incomplete
  layouts, distinct from the confirmed current profiles. Keep unsupported
  light payloads opaque until their schemas are established; the MP2 Helper
  reader is now documented, but its Maya consumer is still missing. See
  [format index](docs/specification/INDEX.MD).

- [ ] Qualify real Maya 2022/2023/2024 imports (mesh/material, skeleton, SKDv0/v1,
  cancellation and repeated imports). Headless tests cannot establish DAG/API or
  viewport correctness. See [review](docs/REVIEW.md).
- [ ] Implement native KF2 animation sampling: FPS/time conversion, interpolation
  modes, scale/visibility and parent ordering. Current `importAnimation` applies
  stepped transforms at source frame IDs; this is not native playback equivalence.
- [ ] Resolve Node hierarchies independently of file order, detect missing parents
  and cycles, and verify transform/scaling preservation in `importMesh` and both
  skeleton import paths (`max_payne_maya/kf2/__init__.py`).
- [ ] Map multi-object SKD primitive ranges to their matching meshes explicitly.
  The reader retains both primitive arrays; Maya import rejects multi-object
  skins instead of silently assigning everything to the first object.
- [ ] Implement camera/light/environment/helper Maya consumers; camera import is
  currently a stub. Skipped chunks are retained as bounded raw payloads by the SDK.
- [ ] Complete strict LDB section marker/count/reference validation and polygon
  topology checks; shared primitive checks do not validate the whole document.
- [ ] Make imports transactional/undoable, including cancellation and texture
  output cleanup. Cancellation stops subsequent work but retains prior output.
- [ ] Replace placeholder legacy normals with a smoothing-mask-aware consumer;
  stored smoothing data is available, native corner-normal equivalence is unproven.
- [ ] Add hash-retained original SCX samples to the image corpus when available.
  Current SCX coverage is native-static MP1/MP2 plus constructed fixtures;
  compressed/planar ColoRIX variants are explicitly unsupported. See
  [image evidence](docs/specification/IMAGES.MD).

- [x] Validate sequential LDB2 prefab registration in Python and the canonical
  C++ reader. Skipped IDs now fail before render/collision payloads; negative IDs
  do not register templates. Complete malformed fixtures, sequential/reused IDs
  and unique-render flags are covered. See
  [validation](docs/research/PREFAB_VALIDATION.md).
- [ ] Qualify the documented MP2 normalization and scale-restoration rules against
  a Maya sampling implementation; the version-4 bool's general meaning remains
  unknown. See [playback](docs/specification/KF2.MD#mp2-animation-playback).

- [ ] Establish a Helper class-role mapping only when an authentic Helper-bearing
  asset is available: retain its hash, run `tools/audit_helpers.py`, then trace
  the external Helper callback. The current 3094-file corpus has zero Helpers;
  MP2KF2 itself only reads and dispatches them. This is unknown consumer semantics,
  separate from the already-listed missing Maya helper consumer. See
  [Helper review](docs/research/HELPER_REVIEW.md).
