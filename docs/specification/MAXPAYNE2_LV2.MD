# Max Payne 2 / MaxED2 LV2

LV2 stores editable MP2 levels. The current profile uses document format 3,
CommonEntity 4, Mesh 9, Material 5 and Preferences 6. These are independent
versions. LV2 is not compiled [MP2 LDB](MAXPAYNE2_LDB.MD), MP1
[LVL](MAXPAYNE_LVL.MD), or a KF2 model.

This page describes known storage layouts and explicit limits. Unknown field
names remain neutral. Do not infer that a field is absent just because its
meaning is unknown, or change stored bytes to match a loader's in-memory defaults.

## Tagged values and chunks

Use [DATA_TYPES.MD](DATA_TYPES.MD). `Chunk(id,version)` means raw byte 0c followed
by little-endian u32 id, version and totalSize. The size includes the 13-byte
header. All following fields belong inside that payload unless stated otherwise.
Children must fit inside their parent.

ID 0 has many meanings, selected by its position and containing structure.
ID 1 is used by the Mesh wrapper. A generic sequence of tags cannot identify
all raw image, lighting and graph data. Keep unknown payloads bounded by size.

## Document order

```text
DocumentVersion Chunk(0,1)
TextureList Chunk(0,1)
TUInt categoryCount
repeat categoryCount:
    CategoryHeader Chunk(0,1)
    Material chunks[materialCount]    # siblings of the category header
LightmapPool Chunk(0,1)
DocumentPreferences Chunk(0,6)
TInt rootEntityType
EntityBody(rootEntityType)
Selection
Camera
optional FinalStringSet Chunk(0,1)
EOF
```

DocumentVersion contains TString sentinel=`MAXED1.1`, TInt documentFormatVersion=3
and TString createdWithBuild. The sentinel still says MAXED1.1 in MP2.
The build string, document format and chunk version are not interchangeable.
An old-level import can produce a separate unchunked version prefix; detect it
explicitly instead of reading it as the normal current header. Full support
for all older document prefixes is not specified here.

FinalStringSet contains TUInt count followed by TString values. Its complete
application meaning is unknown; the name PlayerGroups in older descriptions
must not be treated as a proved new entity table.

## Textures and materials

```text
TextureList Chunk(0,1):
    TUInt textureCount
    Texture chunks[textureCount]

Texture Chunk(0,1):
    TUInt imageFormat
    TInt imageByteCount
    TString nameOrSourcePath
    raw u8 imageBytes[imageByteCount]

CategoryHeader Chunk(0,1):
    TUInt materialCount
    TString categoryName
```

The category's Material chunks follow outside its header payload. A texture
can retain an unavailable absolute source path and still contain its full image.
Format 5 is DDS in the inspected examples. Keep the stored format field and
image bytes; the source filename does not determine the layout.

Material version 5, in stored order:

```text
TString name
TUInt diffuseFrameCount
TString diffuseTextureNames[diffuseFrameCount]
TString lightLayerTextureName,detailTextureName
TDouble diffuseDefaultWidth,diffuseDefaultHeight
TDouble lightLayerDefaultWidth,lightLayerDefaultHeight
TDouble detailScale
TBool doubleSided
TUInt alphaTestValue
TBool adultContent
TInt blendType
TBool alphaCompareEdgeBlend,usesReflection,usesGloss
TString reflectionTextureName,glossTextureName
TInt visibleFrame,frameRate
```

Texture names resolve against TextureList. Default widths and heights describe
texture repetition, not embedded image dimensions. Light-layer and diffuse
settings are separate. The observed loader replaces alphaTestValue 0 with 240;
a storage reader should still preserve the original value.

BlendType 1 enables alpha testing; type 2 selects a smooth alpha path in the
observed exporter. Reflection/gloss and edge blending also affect the compiled
mode. Do not copy this enum to the runtime LDB blendMode field.
Older Material versions have additional branches: detailScale from 3,
reflection/gloss fields from 4, frame arrays and visible-frame data from 5.
The version 5 layout must not be used unchanged for earlier versions.

## Lightmaps

```text
LightmapPool Chunk(0,1):
    TInt lightmapCount
    repeat lightmapCount:
        TULong lightmapId
        Lightmap chunk
    LightmapCurve chunk

Lightmap Chunk(0,2):
    TUInt width,height
    raw float32 rgb[width * height][3]
    TBool passThrough

LightmapCurve Chunk(0,1):
    TFloat middleGray,outputMinimum,outputMaximum,equalizationPercent
```

The four curve names describe the known settings; this page does not fully
define their lighting formula. Lightmap version 1 omits passThrough. A separate
older unchunked lightmap form uses 16 raw bytes per pixel and is not the 12-byte
chunked RGB layout.

A lightmap ID is an object reference, not necessarily its array position.
Unreferenced lightmaps can exist in compiled source data and can produce editor
warnings after reconstruction. Retaining them losslessly and generating a clean
new authoring document are different operations.

## Document preferences

Preferences version 6 contains:

```text
TUInt unknownPreferencesWord
TDouble backClipPlane,frontClipPlane,fieldOfView
TBool exitAcceleration
TInt renderingMode
TUInt connectedRooms
TDouble angleSnap
TString angleSnapStepsText,gridScaleStepsText
TUInt defaultUvScale
TDouble lightmapResolution
TBool averageLightmapBorders
TUInt radiosityViewportSize
TDouble globalLightmapResolution
TULong defaultLightColorPacked
TFloat defaultLightIntensity,gisMaxEnergyPerShoot,gisStopAtEnergy
TBool gisIgnorePortals
TString exportParametersText
TUChar backgroundRed,backgroundGreen,backgroundBlue,backgroundAlpha
```

The first word is not a field count. MP2 renderingMode values are 0 diffuse,
1 lightmap,2 diffuse multiplied by lightmap and 3 light layer. They differ from
MP1 texture_display. Keep packed color storage separate from component order.
Earlier preference versions have conditional fields and are not covered by
this fixed version 6 schema.

## Entity tree

```text
EntityBody(type):
    CommonEntity chunk
    TypeSpecificData(type)
    TUInt childCount
    repeat childCount:
        TInt childType
        EntityBody(childType)
```

There is no mandatory outer chunk around an entire entity and its descendants.
Skipping CommonEntity alone does not safely skip an unknown entity type.

| Type | Entity |
| ---: | --- |
| 100 | Mesh; room status depends on context |
| 103 | World |
| 104 | Prefab parent |
| 105 | FSM object |
| 106 | Trigger |
| 107 | Waypoint |
| 108 | Jump point |
| 109 | Level item |
| 110 | Enemy/character |
| 111 | Dynamic point light |
| 112 | Polygon group |
| 113 | Radiosity light |
| 114 | Portal |
| 115 | Prefab content |
| 116 | Player |
| 117 | Triangle mesh |
| 118 | AI node |
| 119 | Flare |
| 120 | Volume-lighting box |

Types 101/102 are not described by this profile. Item, enemy/flare construction
can require external database definitions even when their stored bytes are valid.

## CommonEntity

Version 4, Chunk(0,4):

```text
TULong serializedObjectId
TDouble positionX,positionY,positionZ
TDouble rotation00,rotation01,rotation02
TDouble rotation10,rotation11,rotation12
TDouble rotation20,rotation21,rotation22
TDouble boundsMinX,boundsMinY,boundsMinZ
TDouble boundsMaxX,boundsMaxY,boundsMaxZ
TDouble boundingRadius
TBool visible,excludedFromGame,excludedFromLighting
TBool exportRegroupingEnabled,storedGameplayCritical
TString name
TBool hasFsm
if hasFsm:
    TUInt fsmArchiveByteCount
    raw u8 fsmArchive[fsmArchiveByteCount]
```

The object ID comes before the 19 separately tagged doubles. It is a serialized
reference key, not an address to dereference. Position and rotation are
parent-relative. Bounds/radius are caches; do not assume every MP1 bounds rule
also applies to MP2. Stored gameplay criticality can be combined with entity
and hierarchy rules at load time. None of these bools is an established
Outliner-expanded flag.

## FSM archive

The current FSM form is Chunk(0,1). Version 0 and an older unchunked form also
exist. Vector, Set and Map use markers 1c, 1d and 1f plus TInt count.

```text
Set(TString) declaredStates
TString initialState
Set(TString) customEvents
Map(TString eventName, Handler) eventHandlers
TBool storedCanAddStates,storedCanAddCustomStrings
if fsmVersion >= 1:
    Map(TString timerName, TimerDefinition) timers

Handler:
    Vector(Message) before
    Map(TString stateName, Vector(Message)) stateHandlers
    Vector(Message) after

TimerDefinition Chunk(0,1):
    TBool usesRealTime
    TFloat duration
```

Preserve collection order, names, empty records and unknown values. A lossless
reader does not apply editor migrations or force the two stored capability
bools to their loaded values.

Event conditions use an exact case-insensitive current-state lookup between
Before and After. An empty condition is not an unconditional section. Declared
states and named FSM_Switch handlers are distinct. Newly authored stateful
objects need an explicit valid default and switch entries for their states.
Generated attached FSMs also need Startup, even if it has no commands. Dynamic
objects can require their standard DO callback entries. These are authoring
requirements, not extra fields or permission to insert records during a no-op
read/save.

## Messages and object references

Current Message Chunk(0,1):

```text
TString sourceText,functionName,receiverName
Vector(TString) parameterStrings
TBool storedMessageFlag94
TUInt receiverObjectId
Vector(TUInt) parameterObjectIds
```

Version 0 and the older unchunked Message form omit the final ID fields.
Mixed older and newer Message forms occur inside an FSM version 1 envelope.
The number of parameter IDs need not match the number of parameter strings.
An old cache can survive editing, so raw text and cache arrays must be kept.

Object IDs refer to serialized CommonEntity IDs. They are not pointers,
selection indices or guaranteed persistent GUIDs. A quoted empty string needs
ID 0; it must not bind to a root object that happens to have an empty name.
The meaning of storedMessageFlag94 is not fully named; it affects receiver
lookup/rewrite and is not simply an isComment flag.

Relative receivers such as this and child paths depend on the FSM owner.
Compiled AI receivers can acquire an `.AI` suffix that was absent from their
editor object path. Authoring and compiled names are therefore not always
identical. Rebinding must keep sourceText and caches consistent; it must not
strip arbitrary suffixes by analogy.

## Mesh wrapper and Mesh data

Current Mesh 100 specific data:

```text
MeshWrapper Chunk(1,0):
    Mesh Chunk(0,9)
    TBool hasVolumeLighting
    if hasVolumeLighting: VolumeLighting chunk
```

Some older files store the Mesh chunk directly, without the ID 1 wrapper.
Mesh version 9:

```text
TBool storedFlippedFlag
TUInt vertexCount
Vertex chunks[vertexCount]
TUInt polygonCount
Polygon chunks[polygonCount]
TBool hasAnimation
if hasAnimation: Animation chunk
MeshProperties chunk
TBool hasTrigger
if hasTrigger: TriggerProperties chunk
```

Vertex Chunk(0,1) contains TDouble x,y,z. Preserve original edge and fragment
structures instead of replacing every polygon with a single guessed contour.
Older Mesh versions need their own guards and are not the same fixed layout.

## Polygon and planar mapping

Polygon Chunk(0,3), in order:

```text
TUInt polygonId
TInt edgeCount
TDouble planeNormal[3]
TDouble secondaryNormal[3]
TDouble legacyMatrix[9]
PlanarMapping primaryMapping
TDouble pointOnPlane[3]
TInt unknownPolygonWord
PlanarMapping lightmapMapping
TFloat lightmapResolution
TBool lightmapValid
TULong lightmapId
TUInt polygonTypeOrFlags
TInt pairedPolygonId
TString materialCategoryName,materialName
repeat edgeCount: TInt fromVertex,toVertex
TInt triangleCount
repeat triangleCount:
    TDouble normal[3]
    TInt indexCount
    TInt meshVertexIndices[indexCount]
AdditionalUvMappings if enabled by polygon features
```

Each bracketed double group is a fixed number of separately tagged scalars,
without an array header. The legacy matrix is stored even when a writer emits
identity. unknownPolygonWord is not proven to be another lightmap ID.

PlanarMapping contains 17 separate TDouble values: normal cache[3], origin[3],
basis U/V/N[9], offsetU and offsetV. Projection subtracts origin, applies the
inverse basis and adds offsets. The normal cache can be derived from the basis,
but the stored bytes still belong to the record. Keep scale in the basis.

Feature bit 4000 enables additional mappings. Bit 20000 selects sparse keyed
mappings: a stored count includes the primary slot, then each extra entry has
a TInt slotId and PlanarMapping. The other observed variant stores TInt 3 and
two mappings for slots 1/2 without explicit IDs. Do not apply one count/ID rule
to every feature combination.

A polygon's edges can form multiple cycles or a weakly simple boundary with
repeated outgoing vertices. The saved triangle fragments are a separate source
of tessellation. Building one from-to dictionary can lose holes or edges.
The pairedPolygonId is a serialized polygon ID; it is not the Portal entity's
parent-local polygon ordinal.

## MeshProperties

Version 6, Chunk(0,6), in order:

```text
TBool characterCollisions,useLightmaps,pointLightsAffect,continuousUpdate
TBool bulletCollisions,castNoShadow,physicsCollisionsEnabled,blockExplosions
TBool doNotRender,noDecals
TString soundEnvironment
TBool generateConvexHull
TBool rayTracing
TString physicalMaterial
TBool elevator
TBool generateBoundingBoxHull
```

Later fields first appear in earlier chunk versions as follows: convex hull
from 2, ray tracing from 3, physical material from 4, elevator from 5, bounding-box
hull from 6. The current property names do not prove identical MP1 behavior.
`physicalMaterial` names a physical definition, not a visual material.

Convex-hull and bounding-box-hull generation are different compile operations.
The latter can create geometry not stored as ordinary editor faces. Runtime
collision masks also depend on per-face categories and independent gates.
A no-draw material and doNotRender are not interchangeable.

## Triangle mesh

Entity 117 uses TriMesh Chunk(0,3), without the ordinary Mesh wrapper:

```text
MeshProperties chunk
TString sourceFile,sourceName
TBool hasAnimation
if hasAnimation: Animation chunk
TUInt vertexCount
TMVertex chunks[vertexCount]
TUInt triangleCount
TMTriangle chunks[triangleCount]
TULong lightmapId
```

TMVertex Chunk(0,1): TDouble position[3], TDouble normal[3], TUChar R,G,B,
then TDouble u,v. These u/v values are primary UVs.

TMTriangle Chunk(0,2): TInt vertexIndex0/1/2, TVector2f lightmapUv0/1/2,
TString materialCategory/materialName, then TInt storedTriangleWord2c.
Earlier triangle versions have six additional TInt fields before the UVs.
The three corner UVs are lightmap UVs, not primary UVs. The current TriMesh
layout has no independent stored detail-UV channel.

The observed TriMesh exporter writes a lightmap UV channel even when a source
render path had none. An ordinary Mesh polygon can be needed to preserve an
unlit/additive render path. Storage acceptance alone does not make the two
representations interchangeable.

## Other entity payloads

World 103, Waypoint 107, JumpPoint 108, PrefabContent 115 and AINode 118 have no
additional payload in the inspected forms. Other current forms include:

| Entity | Specific payload |
| --- | --- |
| FSM (105) | Chunk(0,1): TDouble displayRadius |
| Prefab 104 | Chunk(0,3): TString sourcePath; TBool unknownFlag; TDouble displayRadius |
| Item (109) | UISphere Chunk(0,1): TString className; TDouble radius |
| Player (116) | Chunk(0,1): TString defaultPlayerGroup |
| Trigger (106) | UISphere, then TriggerProperties |
| Enemy (110) | UISphere, then a chunk containing TString enemyGroup and TString activatorAnimation |
| DynamicPointLight (111) | UISphere, then chunk with TFloat R,G,B,A,intensity,falloff |
| PolygonGroup (112) | Chunk(0,2): TUInt count, TUInt parentPolygonOrdinals[count], TBool smoothLightmaps,smoothGeometry, TFloat maxAngle,maxEdge, TBool freezeLightmaps,rayTracing |
| RadiosityLight (113) | Chunk(0,1): TUChar R,G,B,A; TFloat intensity,hotspotAngle,falloffAngle; TUInt polygonId |
| Portal (114) | Chunk(0,3): TUInt parentPolygonIndex; TBool ignoreGisLighting,alwaysClosed |
| Flare (119) | UISphere, then an empty Chunk(0,1) in inspected examples |
| VolumeLightingBox (120) | Chunk(0,1): TDouble sizeX,sizeY,sizeZ; TInt resolution |

Portal parentPolygonIndex and PolygonGroup membership use ordinals in their
parent mesh, not document-wide polygon IDs. Portal pairedPolygonId uses the
other domain. Resolve each reference after the parent's actual polygon order
is known. Prefab 104's unknown bool must be kept; it is not a UISphere record.
For Portal versions below 2/3, the later bools are absent. PolygonGroup version 1
omits its final rayTracing bool.

TriggerProperties Chunk(0,3) stores six TBool values in order: player,use,enemy,
bullet,lookAt,visibility, followed by TString activatorAnimation. The string
appears from version 2 and the visibility bool from version 3. It is not a raw
integer activation mask.

## Volume lighting

VolumeLighting Chunk(0,1):

```text
TUInt gridCount
repeat gridCount:
    TInt cellsX,cellsY,cellsZ
    TVector3f boundsMin,boundsMax
    raw u8 cells[cellsX * cellsY * cellsZ * 25]
```

Version 0 omits gridCount and implies one grid. Each 25-byte cell is packed:

| Byte offset | Raw field |
| ---: | --- |
| 0,4,8 | float32 ambient R,G,B |
| 12 | float32 ambient alpha |
| 16 | u8 directional hue |
| 17 | u8 directional saturation |
| 18,19,20 | u8 directional X,Y,Z |
| 21 | Unaligned float32 directional intensity |

The cell index is `((z*cellsY+y)*cellsX+x)`. The directional bytes decode as
hue*360/255 degrees, saturation/255 and `(component-128)/128`. Ambient sampling
uses the stored RGB divided by 255. These bytes are not unused padding.
Runtime LDB cells have a different 12-byte representation.

## Animation archive

Animation Chunk(0,1):

```text
TUInt animationArchiveByteCount
raw u8 archive[animationArchiveByteCount]
TString activeKeyframe,defaultKeyframe,lightingKeyframe
```

The archive contains TInt keyframeCount; each key has TString name and twelve
separate TDouble matrix fields. Then TInt transitionCount; each transition has
TString name and a MeshAnimation Chunk(0,1):

```text
TMatrix4x3f startMatrix,endMatrix
CompressedGraph positionSamples
CompressedGraph rotationSamples
TDouble duration
TString startKeyframeName,endKeyframeName
EditorGraph positionEditorGraph
EditorGraph rotationEditorGraph
```

Keyframe matrices and cached float endpoint matrices have different encodings.
Keep their frames and names separate. The enclosing Mesh or TriMesh determines
where this archive appears; an animation is not a separate top-level document
section.

## Compressed graph

```text
TInt marker = 114
TInt version = 1
TInt channelCount
TInt sampleCount
repeat channelCount:
    TInt layerMarker = 115
    TInt layerVersion = 1
    TInt byteCount
    TFloat minValue
    TFloat quantizationStep
    raw u8 samples[byteCount]
```

Decode a sample as `minValue + samples[i]*quantizationStep`. The second float
is a step, not a maximum. Normalized sampling uses coordinate
`t*(sampleCount-1)` with linear interpolation between decoded neighbors.
The stored byteCount controls reading; do not replace it with sampleCount.
An extra wrap/guard byte created by the loader is not stored in the file.
The older marker 113/version 3 float-sample form is a separate layout.

## Editor graph

EditorGraph is a tagged inline structure, not a chunk:

```text
TInt marker = 113
TInt version                         # 1..3
TString labelX,labelY
TInt channelCount,sortOption,selectedCurveIndex
if version >= 2: TInt selectedPointIndex
TInt showCoordinates,fillPoints,gridScale
TFloat xMin,xMax,yMin,yMax
TULong curveColor1,curveColor2,curveColor3
TInt interpolationMode,unknownWord44
if version >= 2: TInt unknownWord48
if version >= 3: TInt sampleCount
TUInt pointCount
repeat pointCount:
    TInt pointMarker = 112
    TInt pointVersion = 1
    TFloat x,y1,y2,y3
TUInt trailingWord84
```

Every point stores three Y values, and every graph stores three colors,
regardless of channelCount. The trailing TUInt is one value, not a new count.
Keep the unknown words. Mode 0 uses a cubic Hermite-like curve based on nearby
secants; mode 1 uses a Catmull-Rom-like form adjusted for X spacing. The observed
MP2 animation loader can change these modes in memory; preserve source values
when writing unchanged data.

This stored structure also appears in MP1 LVL dynamic-data blobs. Shared
storage does not imply identical load-time conversion in both editors.
It is distinct from the simpler marker 113 SampleGraph in MP1 LDB.

## Selection and editor camera

Selection starts with TUChar selectionVersion. Version 0 has no selection
payload. Version 1 has Vector(TUInt) selected traversal indices followed by
TUChar autoSelectChildren. Version 2 wraps selection data in a chunk, beginning
with TUChar hasSelection and ending with TUChar autoSelectChildren. Its complete
collection semantics are not specified for arbitrary legacy inputs; preserve
unknown bounded content. Selection indices follow entity traversal, not
serializedObjectId values.

The editor Camera is not a chunk:

```text
TDouble positionX,positionY,positionZ
TVector3f angles
TDouble movementSpeed
```

Do not confuse this viewport camera with a KF2 Camera resource.

## Validation and supported scope

Check chunk ends, collection counts, embedded byte counts, image/grid sizes,
entity types, object IDs, polygon ordinals and editor/runtime frame differences.
No-op writing should preserve unknown fields, source tags and opaque blocks.
An imported old-level prefix, unknown entity type or unrecognized feature
combination needs explicit handling rather than tag scanning.

The Maya importer documents LV2 but does not currently import it. Reading and
writing this editable format, compiling it to LDB and running the compiled
level are separate tasks. Lossless storage does not reconstruct missing editor
information from an LDB or guarantee complete gameplay equivalence.
