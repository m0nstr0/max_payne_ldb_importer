# Max Payne 1 and 2 KF2 files

KF2 stores models, object animation, camera paths, materials and related data.
The extension does not mean that a file belongs only to Max Payne 2. A KF2 file
can contain animation without geometry. KFS uses the same chunk format; SKD
uses its Skin chunk. See [KFS](KFS.MD) and [SKD](SKD.MD).

This page describes stored fields. It does not promise that every chunk has a
Maya scene implementation. Unknown fields and unsupported versions must not be
silently converted into guessed data. The current description supersedes the
older field names and chunk-size description in this file's previous revisions.

## Reading a file

Use [DATA_TYPES.MD](DATA_TYPES.MD) for tagged values. There is no file-level magic
before the first chunk. Read chunks until EOF. Each header has raw `0c`, u32 ID,
u32 version and u32 totalSize. All integers in that header are little-endian.
The size includes the 13-byte header. Bound every child read by its parent.

| ID | Chunk | Layout covered here |
| --- | --- | --- |
| `00010000` | Node | 0, 1 |
| `00010001` | Camera | 0 |
| `00010002` | Point light | Not fully specified |
| `00010003` | Directional light | Not fully specified |
| `00010004` | Spot light | Not fully specified |
| `00010005` | Mesh | Containers 0, 1, 2 |
| `00010006` | Geometry | 0, 1 |
| `00010007` | Polygons | 0, 1 |
| `00010008` | Polygon | 0 |
| `0001000b` | Smoothing | 0 |
| `0001000c` | PolygonMaterial | 0, 1 |
| `0001000e` | UVMapping | 0, 1 |
| `0001000f` | MaterialList | 0 |
| `00010010` | Material | 0, 1, 2 |
| `00010011` | Texture | 1; same observed reader layout for 0 |
| `00010012` | KeyframeAnimation | 0 through 5 |
| `00010013` | Animation | 0 |
| `00010014` | Skin | 0, 1; see SKD |
| `00010015` | Environment | 0 |
| `00010016` | Helper | Not fully specified |
| `00010017` | Point-light animation | Not fully specified |
| `00010018` | Directional-light animation | Not fully specified |
| `00010019` | Spot-light animation | Not fully specified |
| `0001001a` | ReferenceToData | 0 |

The enclosing chunk determines a child's role. A known ID does not justify
using the layout of a different version. Preserve an unsupported payload as
opaque data or report that it is unsupported.

## Node

Node version 0 or 1:

```text
TString name
TString parentName
TMatrix4x3f objectToParentTransform
TBool hasParent
if version >= 1: TString userDefinedString
```

The matrix is relative to the named parent. It is not necessarily a world
matrix. Preserve `parentName` and `hasParent` separately. An importer should
resolve the hierarchy before building world transforms, rather than assuming
that parents always appear first. Do not bake a Node matrix into vertices and
then apply the same matrix again to the scene object.

## Mesh

Mesh versions 0, 1 and 2 are containers of child chunks. Their children can
include Node, Geometry, Polygons, Smoothing, PolygonMaterial, multiple UVMappings
and ReferenceToData. Some children may be absent. Unknown children still have
the normal chunk header and must be skipped by their declared size.

Older meshes commonly use tagged geometry and polygon records. Mesh version 2
commonly uses packed geometry. These are separate child versions; do not select
a Geometry layout from the Mesh version alone. Conversion of an older mesh into
render primitives is a separate operation from reading its stored chunks.

## Geometry

Version 0:

```text
TInt vertexCount
TVector3f positions[vertexCount]
```

Version 1:

```text
TUInt vertexCount
raw float32 positions[vertexCount][3]
raw float32 normals[vertexCount][3]
TUInt primitiveCount
TUInt verticesPerPrimitive[primitiveCount]
```

Positions and normals are separate arrays. Raw floats have no per-value tags.
Primitive counts divide the arrays into contiguous ranges. A normal is a
vector, so translation must not be applied when transforming it.

## Polygon and Polygons

Polygon version 0:

```text
TInt vertexCount
TInt vertexIndices[vertexCount]
```

Polygons version 0:

```text
TInt polygonCount
Polygon chunks[polygonCount]
TInt reservedWord0
TInt reservedWord1
```

The reserved words are stored even though the observed loader discards them.
Their full meaning is unknown. Preserve them when writing a source file.
A stored polygon is not necessarily a triangle.

Polygons version 1:

```text
TUInt indexCount
raw uint16 indices[indexCount]
TUInt primitiveCount
TUInt trianglesPerPrimitive[primitiveCount]
```

`indexCount` counts indices, not triangles. Triangle indices are local to each
primitive. For a combined vertex buffer, add the prefix sum of earlier
`verticesPerPrimitive` values. Do not add this base more than once.

## Smoothing

Version 0:

```text
TInt count
TUInt smoothingGroupMasks[count]
```

Each value is a bit mask, not a single smoothing-group number. Rebuilding
corner normals from these masks is an importer task. Storage alone does not
define how a DCC application should merge or split vertices.

## PolygonMaterial

Version 0:

```text
TInt materialNameCount
TString materialNames[materialNameCount]
TInt polygonMaterialCount
TInt polygonMaterialIndices[polygonMaterialCount]
```

Version 1 stores only the material-name count and names. Primitive grouping
provides the packed mesh's material association. Validate each association
against the actual primitive and material tables before creating scene faces.

## UVMapping

Version 0:

```text
TInt layer
TInt polygonCount
Polygon chunks[polygonCount]     # indices into this mapping's coordinates
TInt reservedWord0
TInt reservedWord1
TInt coordinateCount
TVector3f coordinates[coordinateCount]
```

Version 1:

```text
TUInt layer
TUInt coordinateCount
raw float32 coordinates[coordinateCount][3]
TUInt primitiveCount
TUInt coordinatesPerPrimitive[primitiveCount]
```

Coordinates have three components, even when a consumer uses only U and V.
Version 0 has separate position and UV indices. Version 1 uses packed primitive
ranges. Match UV ranges to their own counts; do not assume every layer has the
same storage just because a preview uses only the first layer. A V-axis flip
for Maya is a scene conversion, not an on-disk requirement.

## ReferenceToData

Version 0 contains one TString, `referencedObjectName`. This is a reference to
another object's data, not an embedded copy of its geometry.

## MaterialList

Version 0:

```text
TString textureDirectories
TInt materialCount
Material chunks[materialCount]
```

The directory string may contain semicolon-separated paths. Relative texture
lookup depends on the model's directory and the caller's resource context.
It must not always start from the level directory. Texture chunks contain
filenames; they do not contain embedded image bytes.

## Material

Versions 0, 1 and 2 share this prefix, in this exact order:

```text
TString name
TBool twoSided, fogging, diffuseCombined, invisibleGeometry, vertexAlphaEnabled
TInt diffuseType, specularType, reflectionType
TFloat ambientR, ambientG, ambientB, ambientA
TFloat diffuseR, diffuseG, diffuseB, diffuseA
TFloat specularR, specularG, specularB, specularA
TFloat vertexAlpha, specularExponent
TInt diffuseCombine, reflectionCombine
TFloat embossFactor
TBool hasDiffuseTexture
if hasDiffuseTexture: Texture chunk
TBool hasReflectionTexture
if hasReflectionTexture: Texture chunk
TBool hasBumpTexture
if hasBumpTexture: Texture chunk
TBool hasOpacityTexture
if hasOpacityTexture: Texture chunk
```

Version 1 adds:

```text
TBool hasGlossTexture
if hasGlossTexture: Texture chunk
TInt glossType
TBool reflectionLit
```

Version 2 also adds:

```text
TBool alphaTestEnabled
TBool alphaTestBlendAllowed
TInt alphaReferenceStored
```

The older Python API calls the gloss slot `mask_texture` and keeps several
legacy names. These names do not add a sixth texture or change the byte order.
Opacity uses its own presence flag, independently of bump.

The second version-2 bool permits a blend path during alpha testing; it does
not guarantee that blending is enabled for every combination of other fields.
The rendering consumer uses the low eight bits of `alphaReferenceStored`.
Keep the stored TInt unchanged when reading or writing; do not replace it with
a TUChar or clamp it to 0 through 255. The full alpha comparison rule and every
material enum value are not specified here.

Colors are stored as floats. Values such as 255.0 occur in existing assets.
Do not normalize them to 0 through 1 as part of storage decoding. Version 1
is also used by MP1 assets; it is not a reliable game-version marker.

## Texture

Version 1:

```text
TString name
TInt mipMapCount
TInt filterMode
TInt mapCount
TString mapFilenames[mapCount]
if mapCount > 1:
    TBool automaticStart
    TBool randomStartFrame
    TInt startFrame
    TInt playbackFps
    TInt endCondition
```

The animation fields are absent for zero or one filename. The name and each
filename are separate fields. Image decoding is described in [IMAGES.MD](IMAGES.MD).

## Animation and KeyframeAnimation

Animation version 0 is an inner header:

```text
TString objectName
TInt frameRate
TBool looping
```

KeyframeAnimation versions 0 through 5 contain:

```text
Animation chunk
TString parentName
TBool loopInterpolation
TUInt storedTotalFrameCount
TUInt keyframeCount
repeat keyframeCount:
    TUInt frameId
    TMatrix4x3f transform
if version >= 1:
    TUInt visibilityFrameCount
    repeat visibilityFrameCount:
        TUInt frameId
        TFloat visibility
if version >= 2: TUInt loopToFrame
if version >= 3: TInt interpolationMethod
if version >= 4: TBool maintainMatrixScaling
```

For versions below 5, the game loader adds one to the stored total frame count.
That is a load-time conversion, not an extra field. Preserve the stored value
when round-tripping. The total frame count and the number of stored keys are
different values.

Frame IDs belong to the source track's frame rate. Copying them directly to a
Maya timeline with a different frame rate changes the timing. Parent animation,
looping, visibility, scale and interpolation must be handled explicitly.
The observed MP1 evaluator interpolates matrix coefficients; it must
not be replaced with quaternion interpolation merely because the data describes
object motion. Some coefficient modes can make a basis singular. Preserve the
method and matrix-scaling flag even if a preview supports only a subset.

An animation file can have several tracks. A constructed game object can use
its first track's clock while other consumers retain per-track metadata.
Do not infer one universal timing rule for every resource role. External script
definitions also select animation names, intervals and callbacks; these are not
additional KF2 fields. MP1 and MP2 graphic-novel consumers use different fade
and activation rules even when they load related KF2 structures.

## Camera and Environment

Camera version 0:

```text
Node chunk
TFloat fieldOfView
TFloat frontClipPlane
TFloat backClipPlane
```

The Camera version is the enclosing chunk's version, not the Node version.
The observed camera evaluator can use the matrix basis length during projection.
Do not assume that all camera keys are rigid transforms with unit scale.

Environment version 0 contains eight TUChar values: ambient R/G/B/A followed
by clearing-color R/G/B/A. Do not insert a Node or a field count into that payload.
Light, light-animation and Helper payloads are not fully specified on this page.

## Validation and import limits

Check chunk sizes, count bounds, index domains, primitive ranges, parent names
and texture references separately. Valid storage does not prove correct
animation or skinning in Maya. The current SDK corpus covers 3094 KF2/KFS files;
legacy animation versions use constructed tests where original examples are
not available. Keep unsupported semantics explicit rather than changing bytes
to make a preview appear to work.
