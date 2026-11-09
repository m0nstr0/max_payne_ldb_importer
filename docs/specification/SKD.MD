# Max Payne 1 and 2 SKD files

SKD stores bone influences for skin vertices. It does not contain the full mesh,
skeleton hierarchy, bind matrices or animation. Those come from matching model
and skeleton resources. A valid SKD file alone is not a complete rig.

## Header

The observed files contain one Skin chunk followed by EOF:

```text
raw u8 tag = 0c
raw u32 id = 00010014
raw u32 version
raw u32 totalSize
raw u8 payload[totalSize - 13]
```

The header is little-endian and includes itself in `totalSize`. Version 0 is
used by the supplied MP1 skins; version 1 by the supplied MP2 skins. This is
the same Skin chunk that can appear in a KF2-family stream.

## Version 0

```text
repeat 3:
    TInt influenceEntryCount
    repeat influenceEntryCount:
        TInt vertexId
        TInt boneIndex
        TFloat weight
TInt skinObjectNameCount
TString skinObjectNames[skinObjectNameCount]
TInt skeletonObjectNameCount
TString skeletonObjectNames[skeletonObjectNameCount]
TInt legacyVertexVectorCount
TVector3f legacyVertexVectors[legacyVertexVectorCount]
```

There is no vector marker before these three influence lists. A list count
counts influence entries, not vertices. The same vertex can appear in more
than one list. Combine its entries in source-list order. `boneIndex` addresses
`skeletonObjectNames`; `vertexId` addresses the source mesh's vertex domain.

The three original list names and the exact role of the final Vector3 array
are not established. In particular, do not rename the final array to bind
matrices or discard it when writing the file.

A loader can build per-vertex counts and prefix offsets from the triples. The
observed legacy conversion uses `max(vertexId)+1` slots, or zero when no
influences exist. A temporary vector's reserved capacity is not a serialized
minimum vertex count.

## Version 1

Each row below is one independently marked vector:

```text
Vector(T):
    raw u8 marker = 1c
    TInt count
    T values[count]
```

| Order | Vector | Element type | Meaning |
| ---: | --- | --- | --- |
| 1 | skinObjectNames | TString | Names of source skin objects |
| 2 | skeletonObjectNames | TString | Bone-name table |
| 3 | vertexDataOffsets | TInt | Start of each vertex's influence range |
| 4 | vertexBoneCounts | TInt | Number of influences for each vertex slot |
| 5 | boneIndices | TInt | Bone-name indices for all influences |
| 6 | vertexWeights | TFloat | Weight for each influence |
| 7 | primitiveVertexCounts | TUInt | Number of slots in each primitive |
| 8 | primitiveVertexOffsets | TUInt | First global slot of each primitive |

Lookup for primitive `p`, local vertex `v` and influence `k`:

```text
globalVertex = primitiveVertexOffsets[p] + v
influence = vertexDataOffsets[globalVertex] + k
boneName = skeletonObjectNames[boneIndices[influence]]
weight = vertexWeights[influence]
influenceCount = vertexBoneCounts[globalVertex]
```

Primitive offsets address vertex tables. Vertex-data offsets address influence
tables. These are different index domains. The number of skin-object names
is not the number of render primitives. A single named skin can have several
primitive ranges.

## Validation

Check equal lengths for offsets/counts and bones/weights. Check every influence
and primitive range, and each bone-name index. Compare the primitive counts
with the matching packed Geometry chunk. Preserve source weights and their
order; normalization is a separate import operation. Do not insert a stored
`isSortedByPrimitive` bool: it is loader metadata, not a field in this layout.

The supplied corpus has 47 version-0 skins and 69 version-1 skins with matching
model geometry. The version-1 primitive counts match their geometry ranges.
This checks storage relationships, not every skinning or deformation rule.

## DCC and game compatibility

Match bones by source identity, then map to the destination application's own
influence order. A Maya skinCluster's physical influence order is distinct
from both source bone IDs and sparse matrix-plug indices. If geometry is split
at UV or normal seams, copy the exact source influences to every split vertex.

The tested MP2 legacy render path can expand mesh vertices without remapping
all legacy per-vertex skin counts. A storage-valid Mesh 1 / Skin 0 pair can therefore
be unsafe when rendering creates more vertices. This is a consumer limitation,
not a reason to change the version-0 file grammar. Keep a converted Mesh 2 / Skin 1
pair consistent if that conversion is chosen explicitly.
