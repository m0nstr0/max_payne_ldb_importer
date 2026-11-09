# Corrections used by the reviewed readers — 2026-11-09

Older specification pages remain as historical research. These bounded rules
supersede conflicting descriptions there; they do not introduce serialized fields.

- KF2/KFS/SKD chunks use raw `0c`, little-endian u32 ID/version/totalSize.
  The 13-byte header is included in totalSize. Nested chunks must fit inside
  their parent; unknown payload bytes are skipped/preserved by size, never by
  scanning for another tag. Mesh versions0/1/2 use the same container envelope.
- Tagged signed integers `02/12/13/14` have 32/24/16/8 payload bits and require
  sign extension. Unsigned `03/0f/10/11` are a separate family. Narrow strings
  use `0d`, signed tagged byte length, then exactly that many bytes. UTF-8 is not
  guaranteed; the SDK's Latin-1 view preserves bytes without proving source encoding.
- SKDv0 contains three consecutive influence-entry lists, followed by skin and
  skeleton names and legacy Vector3 data. Repeated vertex IDs combine influences
  in source-list order. The final vectors are retained without asserting bind-pose
  semantics. SKDv1 has eight independently marked `1c` vectors; vertexDataOffsets
  address the flat influence arrays, not geometry vertices. Primitive counts and
  offsets address global vertex slots; skin-object count is not primitive count.
- KF2 Material's opacity Texture chunk is conditional on its own opacity flag,
  independently of bump. Camera/MaterialList version belongs to the container,
  not its last child. Chunk-ID/version and material-flag fixtures exercise this.
- MP1 LDB support is revision32; MP2 is raw `LDB2` plus tagged revision34.
  MP2 raw render/collision triangle indices are unsigned16 and collision material
  IDs are unsigned8. Pool offset -1 means an absent string; other string offsets
  need a terminating NUL within the shared pool.
- MP2 v34 first prefab occurrence (or negative prefab ID) stores render and
  collision records. A repeated instance stores render records only when the
  final prefab flag is true; it never stores collision records. `useLightmaps`
  does not control this grammar. The old Python field `share_collision` remains
  for API compatibility, but its original native property name is unknown.

These rules were checked against the Max Payne workspace's canonical
DATA_TYPES, KF2, SKD and LDB2 specifications, native research retained there,
the SDK corpus and independently assembled tests. No new native execution is
claimed for these previously established rules. New SCX native-static evidence
and current image support are documented separately in [IMAGES.MD](IMAGES.MD).
See [review and validation limits](../REVIEW.md).
