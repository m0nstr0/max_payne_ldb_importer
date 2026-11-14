# Max Payne 2 runtime object state

These are small records used by the runtime state loader and writer. This page
does not describe the complete savegame container. The records are separate
from compiled [LDB](MAXPAYNE2_LDB.MD) and editable [LV2](MAXPAYNE2_LV2.MD).
Use [DATA_TYPES.MD](DATA_TYPES.MD) for tags and chunk headers.

## ObjectBase

The current writer emits chunk ID 0, version 5:

```text
TMatrix4x3f transform
TString currentRoomName
```

An empty room name represents no current room. The loader looks up a nonempty
name in the supplied room container. If found, it applies the loaded position
and rotation and updates room memberships. If no room is found, it removes the
object from its current room; that branch does not simply assign the saved
matrix as a world transform. The name is a TString, not an LDB pool offset.

The loader also accepts these older chunk branches, after the matrix and name:

```text
if version == 1: TULong discarded
if version < 3: TBool discardedA, discardedB
if version < 4:
    TULong oldRoomCount
    TString oldRoomNames[oldRoomCount]
    TVector3f oldPosition
    TBool discardedC
if version < 5: TBool discardedD
if version < 3: TBool discardedE, discardedF
```

The original meanings of the discarded fields are not established here.
TULong uses fixed tag 01; it is not a compact TUInt. The loader skips to the end
of its chunk after these fields, so trailing extension bytes do not become the
next record. A lossless tool must retain those bytes if it rewrites the stream.

## Exit

The writer emits chunk ID 0, version 1:

```text
TBool enabled
TBool aiActivationEnabled
```

The inspected Exit loader reads these two fields without a version branch,
then skips to the chunk end. This does not establish arbitrary future-version
support. Both ObjectBase and Exit use ID 0: the calling context selects the
class. ID 0 alone is not a unique record type or a signature for a savegame.

## Evidence limits

Retained comparisons cover ObjectBase versions 0 through 5, discarded room-name
lists, trailing bytes, a no-room save/reload and Exit versions 0 through 5 with
four stored bool pairs. Original and reconstructed consumers produced matching
saved bytes and observations in those cases. Positive room lookup, the complete
savegame container and damaged-input behavior were not established by those
isolated controls. This page adds no runtime-state Maya reader.
