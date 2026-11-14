# Helper corpus and MP2 consumer review — 2026-11-14

No Helper chunk was found in the retained original corpus. The complete observed
className set is empty; it does not contain an empty-string class or an unnamed
Helper. The scan covered 2899 KF2 and 195 KFS files, all matching the retained
inventory hashes before and after inspection.

| Source | KF2 | KFS | Helper chunks |
| --- | ---: | ---: | ---: |
| MP1 database | 834 | 183 | 0 |
| MP1 SDK | 3 | 12 | 0 |
| MP2 database | 2058 | 0 | 0 |
| MP2 ParticleFX SDK | 4 | 0 | 0 |
| Total | 2899 | 195 | 0 |

The input inventory SHA-256 is
`cda0e7f5ea550b47f75cf8b504900726c7d0afe364b650a2f6e1cd742826a9a4`.
This is the inventoried corpus, not proof about every unpublished exporter file,
mod or other release. MP1 WorkActor duplicates were excluded by that inventory.
Original assets and the full accepted-input list remain outside this repository.

## Reproduction and independent check

The read-only audit follows declared top-level chunk sizes and known Mesh child
streams, reads Helper's Node and class-name fields inside their bounds, and never
searches arbitrary image, matrix or other opaque bytes for a tag sequence.
Run from the Maya importer checkout:

```text
python tools/audit_helpers.py --inventory <original-inventory.json> --output <new-output.json>
```

The existing canonical `max payne formats/tools/inspect_kf2.py` independently
parsed all 3094 files on this date with zero errors, zero opaque chunks and zero
hash mismatches. Its complete chunk-version census also has no 0x10016 entry.
Its JSON embeds the tool's old fixed schema date; the receipt records the actual
new execution date separately. Four constructed audit tests prove positive
Helper detection for Node versions 0/1, exact class bytes, nested offsets,
opaque-payload exclusion and rejection of truncated/out-of-bounds fields.
All 51 importer tests pass. These fixtures are not original game samples.

[Receipt and source pins](helper-corpus-validation.json).

## What MP2KF2 actually does

- `src/loader/LoaderAuxiliaryChunks.cpp`, `HelperChunk::read`: reads a Node child,
  skips its remaining extent, then reads className. No class-name comparison,
  registry lookup or object construction follows.
- `src/loader/HelperChunk.h`: exposes the Node and class string; the data object
  has no mesh, skin-weight or specialized class payload.
- `src/loader/KF_Loader.cpp`, `KF_Loader::load`: only reads a top-level Helper
  when a Helper callback is registered. It passes the temporary HelperChunk by
  const reference to the callback's first virtual entry, then destroys it. Without
  that callback, the common chunk skip advances past the Helper.
- `src/loader/KF_LoaderCallbacks.cpp`: set/get, clear and push/pop preserve a
  caller-supplied callback pointer. They do not classify Helper names.
- `src/animation/ObjectGeometryLoading.cpp` and `ObjectAnimationLoading.cpp`
  install material/mesh/keyframe callbacks, not a built-in Helper consumer.
  Caller callback state can be restored by popState; this does not prove every
  external caller ignores Helpers.

The source paths above are relative to MP2KF2. Therefore this library provides
parsing and dispatch, not a built-in list of Helper classes or their game roles.
Any class-specific interpretation would have to be established in the external
callback implementation. No such role can be inferred from this empty corpus.

`TypedHelperClass` in `MP2KF2/tests/LoaderControls.cpp` is a constructed test
string, not a discovered original class. Retained original/owned loader controls
match 774 checks/digest295cb26e per trial with both provider sets. They support
the read/dispatch contract, not an authentic Helper class taxonomy. Those native
controls were inspected, not rerun. No DLL was built, installed or executed here.
