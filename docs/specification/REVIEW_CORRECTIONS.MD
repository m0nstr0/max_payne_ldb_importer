# Specification revision notes

The current pages replace the older descriptions with consistent notation and
plain English. Previous revisions remain in Git history.

The main corrections are now part of their format pages:

- [Data types](DATA_TYPES.MD): signed compact integers, string byte lengths,
  matrix sizes, collection markers and total chunk sizes.
- [KF2](KF2.MD): child versions, packed primitive indices, material flags,
  animation version guards and the Environment byte layout.
- [SKD](SKD.MD): influence offsets, primitive ranges and external skeleton data.
- [MP1 LDB](MAXPAYNE_LDB.MD): key/index domains and BSP collision queries.
- [MP2 LDB](MAXPAYNE2_LDB.MD): pool messages, unsigned indices, masks,
  prefab sharing and animation control points.
- [MP1 LVL](MAXPAYNE_LVL.MD) and [MP2 LV2](MAXPAYNE2_LV2.MD): editable level
  records, conditional fields, references, lighting and animation graphs.

These documents describe file storage separately from load-time conversion,
scene import, compilation and game behavior. An unknown meaning is not a
missing field. Preserve unknown values instead of giving them guessed names.

## 2026-11-14 source comparison

KF2 now distinguishes normalization modes from interpolation and documents the
MP2 playback path and Helper payload. MP2 LDB now specifies sequential prefab
registration, selected older-revision gates, volume-light sampling and the
translation curve's distance units. Runtime ObjectBase and Exit state chunks
have a separate page; their fields are not added to LDB or LV2.
