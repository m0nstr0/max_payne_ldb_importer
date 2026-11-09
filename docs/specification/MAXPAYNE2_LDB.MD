# Max Payne 2 LDB version 34

This is the compiled runtime level format, often called LDB2. It differs from
[MP1 LDB](MAXPAYNE_LDB.MD) and the editable [LV2 format](MAXPAYNE2_LV2.MD).
All multi-byte values are little-endian. Use [DATA_TYPES.MD](DATA_TYPES.MD)
for tagged values. There are no LV2 chunk headers around the sections below.

## Notation and file order

`Records(T)` means a nonnegative tagged count followed by that many T records.
Counts are commonly TInt, but some short geometry counts use TUShort.
`Offset` means a signed tagged offset into the initial shared pool. Preserve
each field's original tag; equal numeric values do not make different tag
families interchangeable.

```text
raw char magic[4] = "LDB2"
TInt version = 34
TInt poolByteCount
raw u8 sharedPool[poolByteCount]
TFloat physicalWorldSize
Records(Texture) diffuseTextures
TBool lightmapsAreDds
Records(Lightmap) lightmaps
Records(Texture) detailTextures
Records(Texture) reflectionTextures
Records(Texture) glossTextures
Records(Material) materials
Records(Room) rooms
Records(DynamicPointLight) dynamicPointLights
Records(Flare) flares
Records(LevelItem) levelItems
Records(Portal) portals
Records(NamedMarker) jumpPoints
Records(AiMarker) aiMarkers
raw u8 mapMarker = 1f
Records(EnemyGroup) enemyGroups
Records(Character) characters
Records(Fsm) fsms
Records(Trigger) triggers
Records(DynamicMesh) dynamicMeshes
Records(Mirror) mirrors
EOF
```

The shared pool contains both text and packed message structures. There is no
compiled-FSM tail to find after the mirrors. A file-size check must follow the
last mirror record.

## Shared pool

A text Offset identifies the first byte of a NUL-terminated narrow string.
The NUL must lie inside the pool. -1 means an absent reference where permitted.
Other negative offsets or offsets beyond the pool are invalid. Do not decode
packed message blocks as ordinary strings or search them for tagged values.

## Images and materials

```text
Texture:
    TInt imageFormat
    TInt imageByteCount
    Offset path
    raw u8 imageBytes[imageByteCount]

Lightmap:
    TInt imageByteCount
    raw u8 imageBytes[imageByteCount]

Material:
    TUShort blendMode
    TUShort diffuseFrameFirst, diffuseFrameLast
    TUShort lightmapTextureId, detailTextureId
    TUShort reflectionTextureId, glossTextureId
    TUChar alphaCompareReference, sortPriority, detailOffset
    TBool dualSided, writesZBuffer
    TUChar frameRate, visibleFrame
```

The diffuse frame interval is inclusive. Other texture IDs address their own
texture groups, not the diffuse table. Preserve absent-ID sentinels and check
visibleFrame against the selected frame sequence. Lightmap encoding is selected
by the file's `lightmapsAreDds` bool. Do not infer it from a texture filename.

The runtime blendMode and editable LV2 material blendType are different enums.
For example, a smooth LV2 type 2 material without reflection exports as runtime
mode 4. Do not copy enum numbers between the formats. An image with alpha does
not by itself select a particular blend or depth-writing mode.

## Room and render meshes

```text
Room:
    TString name
    TMatrix4x3f localTransform
    Offset soundEnvironmentName
    TVector3f boundsMin, boundsMax, meshMidpoint
    Records(RenderMesh) renderMeshes
    Records(CollisionShape) collisionShapes
    Records(VolumeLight) volumeLights

RenderMesh:
    TUShort materialId
    TBool hasLightmapUvs, hasDetailUvs
    TUShort triangleCount, vertexCount
    raw float32 positions[vertexCount][3]
    raw float32 normals[vertexCount][3]
    raw float32 primaryUvs[vertexCount][2]
    if hasLightmapUvs: raw float32 lightmapUvs[vertexCount][2]
    if hasDetailUvs: raw float32 detailUvs[vertexCount][2]
    raw uint16 triangleIndices[triangleCount][3]
```

The raw triangle indices are unsigned 16-bit. Values above 32767 are not negative
vertices. Positions, normals and UVs are separate arrays. The two UV flags
control whether bytes are present, not just how the mesh should be displayed.
The third room vector is a mesh midpoint, not another bounding-box corner.
The sound-environment field is a pool offset, not a mass value.

## Collision shapes

```text
CollisionShape:
    Count vertexCount, triangleCount
    raw float32 positions[vertexCount][3]
    raw uint16 triangleIndices[triangleCount][3]
    raw uint8 surfaceMaterialIndices[triangleCount]
    TBool convex
    Count collisionMask
    raw float32 moppOrigin[3]
    raw uint32 unknownMoppWord
    raw uint32 moppByteCount
    raw u8 havokMoppCode[moppByteCount]
```

`Count` above denotes a nonnegative tagged integer with its stored tag.
MOPP byte count is raw u32, unlike those tagged counts. Keep the unknown word.
Editing vertices does not rebuild MOPP code; that is a separate physics-build
operation. Do not reinterpret the blob as another sequence of tagged records.

Per-triangle surfaceMaterialIndices refer to category definition order in the
loaded `materials.txt`. They are not alphabetically sorted names or material
IDs from the render table. A custom database must supply its own category order.

Collision masks have distinct stored layouts:

| Channel | Static shapes | Dynamic shapes |
| --- | --- | --- |
| Player | `0002` | `0080` |
| Enemy | `0004` | `0100` |
| Small OR big projectile | `0008` | `0200` |
| Camera | `0010` | `0400` |
| Line of sight | `0020` | `0800` |
| Small AND big projectile | `2000` | `4000` |
| Generic | `8000` | `10000` |

Trigger shapes use `1000` in the observed export path. The OR/AND projectile
bits do not identify two independent projectile sizes. For example, `0008`
alone does not reveal which size was enabled. Physics-filter masks created at
load time are another layout; they must not be written back as stored masks.

Keep separate convex source bodies separate. Merging disconnected shapes or
changing triangle winding can invalidate a hull. `convex=true` is not a repair
operation for arbitrary triangle data. A successful parser or exporter also
does not prove that a hull passes the game's size and validity checks.

## Volume lighting

```text
VolumeLight:
    Count gridWidth, gridHeight, gridDepth
    TVector3f boundsMin, boundsMax
    raw u8 cells[gridWidth * gridHeight * gridDepth * 12]
```

Each runtime cell occupies 12 bytes:

| Byte offset | Raw field |
| ---: | --- |
| 0,1,2 | u8 mapped ambient R,G,B |
| 3 | u8 directional hue |
| 4 | u8 directional saturation |
| 5,6,7 | u8 directional X,Y,Z |
| 8 | float32 mapped directional intensity |

It is not the 25-byte editable LV2 cell. Preserve packed channels and respect the X-first cell ordering
`((z*height+y)*width+x)`. Converting these runtime cells back to editor HDR
lighting requires explicit reconstruction choices; it is not lossless recovery
of every original editor value.

## Lights, objects and navigation markers

| Record | Fields in stored order |
| --- | --- |
| DynamicPointLight | TMatrix4x3f transform; TInt roomId; TFloat R,G,B,A,falloff |
| Flare | Offset name; TMatrix4x3f transform; TInt roomId |
| LevelItem | Offset name,className; TMatrix4x3f transform; TInt roomId |
| NamedMarker | TString name; TMatrix4x3f transform; TInt roomId |
| AiMarker | TString name; TMatrix4x3f transform; TInt roomId; Offset adjacencyList |
| EnemyGroup | TString name; tagged integer id |
| Character | Offset name,className; TMatrix4x3f transform; TInt roomId,enemyGroupId; TString activatorAnimation |

AI marker adjacency is a raw pool structure: u16 neighborCount followed by
u16 neighbor indices. Validate the whole span and every neighbor index against
the runtime marker table. This is not the dense MP1 `.ai` grid. Editable
Waypoints and AINodes can both contribute runtime markers.

A character definition, a player definition and a level item have different
runtime roles. Recognizing a class name or loading the room geometry does not
establish that the required player/startpoint setup is complete.

## Portals

```text
Portal:
    TString name
    TVector3f normal
    TUShort pairedPortalIndex
    TUShort destinationRoomIndex
    TUShort vertexCount
    TVector3f vertices[vertexCount]
```

Portal pairs refer to other portal records and rooms. These indices are not
serialized LV2 polygon IDs. A runtime room is not guaranteed to list its portals
as the first N polygons of its render geometry. Preserve directed pairing and
normal orientation when reconstructing an editor level.

## FSM records

```text
Fsm:
    Offset name
    TMatrix4x3f transform
    TInt parentFsmId
    TMatrix4x3f localTransform
    tagged integer roomId
    Offset defaultState
    raw u8 vectorMarker = 1c
    TInt stateCount
    TString states[stateCount]
    Offset onInitMessages, sendMessages, switchMessages, otherMessages
    Records(Timer) timers

Timer:
    Offset name
    TBool realTime
    TFloat duration
    Offset onStartMessages, onEndMessages
```

States are inline strings. FSM names, default-state names, timer names and
message blocks use pool references. Declared states and named switch handlers
are separate tables. A newly generated stateful FSM needs a switch entry for
each switchable state, including entries with no actions. A reader must still
preserve the original two structures independently.

## Packed message grammar

All fields in this section are raw, with no tagged scalar headers:

```text
MessageVector:
    uint16 count
    repeat count: NUL-terminated commandText

Handler:
    MessageVector before
    MessageVector after
    uint16 stateHandlerCount
    repeat stateHandlerCount:
        uint16 stateIndex
        MessageVector messages

NamedHandlers:
    uint16 count
    repeat count:
        NUL-terminated name
        Handler handler
```

A stateIndex addresses the enclosing FSM's inline state table. `onInitMessages`
points to the Startup Handler. Send/switch offsets point to NamedHandlers
keyed by the event argument. Other handlers use full event names. Timer start
and end offsets point to Handler records. An absent block uses -1.

The runtime executes Before, the section matching its current state, then
After. An empty condition name is not an unconditional wildcard. Before/After
order in execution differs from where the conditional data appears in the
packed record; retain the actual byte order above.

## Dynamic animation

```text
Animation:
    Offset name
    TFloat duration
    TMatrix4x3f startTransform, endTransform
    Graph116 translation
    Graph116 rotation
    Offset leavingFirstFrameMessages
    Offset returningFirstFrameMessages
    Offset reachingSecondFrameMessages

Graph116:
    TInt marker = 116
    TInt version = 1
    TInt interpolationMode
    TInt channelCount
    TInt pointCount
    raw float32 times[pointCount]
    raw float32 values[channelCount][pointCount]
```

Values are channel-major. These are control points, not uniformly spaced
samples. `pointCount` is not a sample rate. The graph is different from the
compressed marker 114/115 graphs in LV2. Animation callback offsets point
directly to MessageVector, without a Handler wrapper.

The FSM transform is a world-space default pose. Its localTransform and the
animation endpoints are relative to the nearest parent with an FSM; -1 means
world space. In row-vector notation:

```text
keyWorld = storedKey * parentFsmWorld
keyAuthoringLocal = keyWorld * inverse(immediateEditorParentWorld)
```

Do not apply the parent again to an already-world-space default transform.
Source key names, editor graph settings and all cached editor samples cannot
be recovered uniquely from these compiled fields.

## Dynamic meshes and prefab sharing

```text
DynamicMesh:
    TInt fsmId
    TBool useLightmaps, pointLightsAffect, continuousUpdate
    TBool bulletCollision, characterCollision, blockExplosions, noDecals, elevator
    tagged integer physicalMaterial
    TInt prefabId
    TBool uniqueRenderFlag
    TVector3f boundsMin, boundsMax, meshMidpoint
    if prefabId < 0 or this is its first occurrence:
        Records(RenderMesh) renderMeshes
        Records(CollisionShape) collisionShapes
    else if uniqueRenderFlag:
        Records(RenderMesh) renderMeshes
    Records(Animation) animations
```

For a repeated prefab, collisions always come from the first occurrence.
The final bool controls unique render data. `useLightmaps` does not control
this grammar. The original authoring name of that bool is unknown; the Python
API's historical `share_collision` name must not be taken literally.
The bounds and midpoint are still stored for the current instance.

`physicalMaterial` is an index into physical-material definitions, not a text
pool offset. Compiled dynamic vertices are centered relative to the stored
midpoint. Restoring editable vertices can require adding the instance midpoint
while keeping the editor pivot and animation frame separate.

## Triggers

```text
Trigger:
    TInt fsmId
    TFloat radius
    TBool activationPlayer, activationUse, activationEnemy
    TBool activationBullet, activationLookAt, activationVisibility
    TString activatorAnimation
    TBool hasCollisionShape
    if hasCollisionShape:
        TInt collisionTemplateId
        if collisionTemplateId == -1:
            Records(CollisionShape) collisionShapes
```

An inline shape set registers a new collision template. A nonnegative ID refers
to an earlier registered template, not necessarily an earlier trigger's record
index. A true hasCollisionShape with an empty resolved shape set is storage-
decodable but unsafe in the tested game's trigger-volume constructor.

## Mirrors

```text
Mirror:
    TVector3f planeNormal, planePoint
    TFloat boundingSphereRadius
    TVector3f boundsMin, boundsMax
    TBool fresnel
    Records(MirrorTriangle) triangles
    tagged integer roomId

MirrorTriangle:
    tagged integer materialId
    TVector3f vertex0, vertex1, vertex2
    TVector2f uv0, uv1, uv2
```

Mirrors are the last section. Their triangles have primary UVs but no separate
lightmap UV fields in this record.

## Validation and recovery limits

Validate signature/version, counts, raw byte lengths, pool offsets, terminated
strings, vertex indices, texture groups, prefab/template references and EOF.
Keep unknown words and MOPP bytes intact. Reconstructing LV2 requires authoring
names, object IDs, polygon structure and editor-only defaults that LDB does not
fully store. Parsing or reproducing binary layout is not a claim of complete
gameplay, lighting or physical equivalence.
