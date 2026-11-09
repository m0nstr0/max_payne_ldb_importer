# Max Payne 1 LDB version 32

LDB is the compiled game-level format. It differs from the editable
[LVL format](MAXPAYNE_LVL.MD) and from [MP2 LDB](MAXPAYNE2_LDB.MD).
This page describes revision 32. Use [DATA_TYPES.MD](DATA_TYPES.MD) for tagged
values. There is no `LDB1` magic before the first section.

## Notation and section order

`Vector(T)` means raw marker `1c`, TInt count, then that many T records.
`Entries(K,V)` means TInt count followed by that many key/value pairs; it has
no map marker unless one is shown. `Map(K,V)` adds a raw `1f` marker before
Entries. Keys are stored values, not implicit array positions.

```text
Vector(TVector3f) bspVertices
Vector(BspPolygon) bspPolygons
Vector(BspNode) bspNodes
Vector(TInt) bspPolygonIndices
TInt version = 32
Entries(TString, Image) materialTextures
MaterialReferences
MaterialAliases
Entries(TString, MaterialCategory) materialCategories
Entries(TInt, Image) lightmaps
Entries(TString, Exit) exits
Vector(TextureVertex) staticTextureVertices
Entries(TInt, StaticMesh) staticMeshes
Entries(TString, StaticLight) staticLights
Entries(TString, Startpoint) startpoints
Entries(TString, Fsm) fsms
Entries(TString, Character) characters
Entries(TString, Trigger) triggers
Vector(TextureVertex) dynamicTextureVertices
Entries(TString, DynamicMesh) dynamicMeshes
Entries(TString, LevelItem) levelItems
Entries(TInt, PointLight) pointLights
Entries(TInt, Room) rooms
EOF
```

Do not move the version before the BSP pools or the room table before the
object tables. A count-based section is not a KF2-style size-bounded chunk.

## BSP records and index domains

```text
BspPolygon:
    TInt vertexStart, vertexCount
    TInt polygonId, meshId
    TVector3f normal
    TVector3f pointOnPlane

BspNode:
    TVector3f planeNormal
    TVector3f pointOnPlane
    Halfspace front
    Halfspace back

Halfspace:
    TInt polygonIndexStart
    TInt polygonIndexCount
    TInt childNode

BspSpan:
    TInt firstPolygon, polygonCount
    TInt firstNode, nodeCount
```

A room or dynamic mesh owns one BspSpan. Its root is local node 0, stored at
`bspNodes[firstNode]`. `childNode` is local to that owner's node span; -1 means
no child. A halfspace's polygon-index span addresses the global index pool.
Each value in that span is a local polygon ordinal:

```text
polygon = bspPolygons[firstPolygon + bspPolygonIndices[slot]]
node = bspNodes[firstNode + localNode]
vertex = bspVertices[polygon.vertexStart + corner]
```

Check each index in its own domain. A nonempty body needs a valid root; do not
silently replace a missing tree with a flat scan. The two vectors in a node
are a plane normal and a point on that plane, not bounding-box corners.
The polygon normal and point define its own oriented collision plane.

## How BSP collision works

The tree narrows the search to finite collision polygons. It is not simply a
set of solid and empty leaves. A leaf holds polygon references; no separate
solid/empty flag is established by these records. A closed visual mesh alone
therefore does not define the result of every physical query.

### 1. Prepare the query

Bring the moving shape into the collision body's local coordinate system.
Use a sphere with center `C` and radius `r`, or a symmetric capsule with axis
endpoints `C-A` and `C+A`, where A is the half-axis vector. Keep the query's
collision-channel mask. Rendering visibility, material drawing and physical
collision channels are separate controls.

### 2. Walk the tree

At a node, compute signed distance `d = dot(C-P, N)`. A negative distance
selects the back side; zero selects the front side. Visit the near side first.
A sphere reaches a split plane by its radius. A capsule also reaches it by
`abs(dot(N,A))`. When the shape or its requested motion reaches both sides,
visit the required polygon spans and the far child as well.

The observed capsule sweep uses a node reach of
`1.002 * (r + abs(dot(N,A)))`. Stationary contact collection has separate
query margins: its broad search uses `r + length(A) + 0.02`, and its node
plane test uses `r + 0.04`. These are algorithm tolerances, not extra LDB fields.
Do not reuse a tolerance from one query type as a universal collision radius.

Polygon-list order matters. Keep the stored order of spans, polygons, edges
and vertices. Later sweep tests can receive an endpoint already shortened by
an earlier test. Sorting all candidate triangle hits by distance changes this
behavior.

### 3. Apply the polygon gates

Resolve the polygon's source mesh/polygon identity to its material category.
The game builds a collision mask from category properties, including character,
projectile, camera and AI channels. The material-derived mask is runtime data;
it is not another stored field in BspPolygon. A query must intersect that mask.

For the observed stationary capsule contact path, the center must be strictly
in front of the polygon: `dot(C-polygonPoint, polygonNormal) > 0`. A shell can
fully contain a capsule without this path reporting overlap when the center is
behind every outward-facing polygon. Do not replace this rule with AABB
containment or odd/even ray counting.

### 4. Test the finite features

Testing the infinite plane is not enough. The contact path first clips the
capsule axis against the finite convex face, then checks finite edge cylinders,
then vertex spheres. It emits at most one contact per admitted polygon, using
the first admitted edge or vertex in source order. A boundary-only clipped
axis falls through to the feature tests.

The capsule contact envelope is `r + 0.02`, but contact separation is computed
from the actual feature distance minus the original radius. Negative means
overlap, zero means tangency and positive means a nearby separated contact.
Exact tangency is allowed by the observed inside-object contact check.
A sphere has its own face-projection and edge tests; treating it as a capsule
with a zero-length axis does not reproduce every boundary case.

### 5. Sweep and return a result

A moving query starts with the requested endpoint. Candidate polygons also
require a front-facing start, motion toward the plane, a source vertex ahead
along the motion and an intersecting material mask. The sweep tests the finite
face and analytic edge/vertex features, shortening the endpoint as it goes.
It does not sample a capsule axis with a fixed set of spheres.

| Result | Meaning |
| ---: | --- |
| 0 | This query did not block the requested motion |
| 1 | A collision retained a shortened endpoint and contact information |
| 2 | The attempted move is rejected at its original start; propagate immediately |

Initial overlap in a feature test can produce result 2. It does not imply a
new, automatically calculated push-out point. Capsule and sphere sweeps also
have different internal comparison details; do not assume one universal
nearest-hit metric for both.

### 6. Apply the caller's response

Sliding, contact margins, gravity, moving-object transport and room changes
belong to the caller. They are not stored in the BSP record. Physical room
traversal clips a move against the current room's BSP before portal traversal.
An editor's room-selection BSP is a different structure and must not replace
this runtime collision tree.

A geometric ray is also distinct from the game's physical PointObject, whose
observed sphere-query radius is 0.04 metres. Changing serialized vertices to
bake that radius or a character contact margin into the level changes geometry.
These notes describe the observed MP1 query paths, not every physics behavior
or exact floating-point result on every game build.

## Images and materials

```text
Image:
    TUInt imageFormat
    TInt byteCount
    raw u8 imageBytes[byteCount]

MaterialReferences:
    raw u8 marker = 1f
    TInt count
    repeat count:
        TInt materialId
        raw u8 pairMarker = 25
        TString categoryName, materialName

MaterialAliases:
    raw u8 marker = 1f
    TInt count
    repeat count:
        raw u8 pairMarker = 25
        TString categoryName, materialName
        TInt materialId

MaterialCategory:
    Entries(TString, Material) materials

Material:
    TString diffuseTextureName
    TString alphaTextureName
    TBool alphaTest
    TBool adultContent
```

Known image codes include 0 TGA, 2 SCX, 3 PCX, 4 JPEG and 5 DDS. The image has
its own encoded structure; it is not a raw RGB array. See [IMAGES.MD](IMAGES.MD).
Material and lightmap IDs are keys. -1 can mark an absent lightmap. An alpha
image is separate from both the diffuse image and lightmap data. Category
collision and drawing rules also come from the external `materials.txt`.

## Portals

```text
Exit:
    TUInt vertexCount
    TVector3f vertices[vertexCount]
    TVector3f normal
    TMatrix4x3f transform
    TInt parentRoomId, destinationRoomId
    TString destinationExitName
    Vector(Vector(TInt)) convexRegions
```

Convex-region indices address this exit's vertex array. The destination exit
name identifies the reverse exit. Preserve both room IDs and this name instead
of guessing a pair from geometry alone.

## Render geometry

```text
TextureVertex:
    TInt vertexIndex
    TVector2f uv, lightmapUv
    TUInt neighborFlags
    TBool smooth

StaticMesh:
    TUInt vertexCount
    TVector3f positions[vertexCount]
    Vector(TVector3f) normals
    TMatrix4x3f transform
    Entries(TInt, RenderPolygon) polygons
    Map(TInt, TVector3f) initialRadiosity

RenderPolygon:
    TInt textureVertexStart, vertexCount
    TVector3f normal
    TUInt engineMaterialType
    TInt materialId, lightmapId
    TFloat maxEdgeLength, maxAngle
    TInt smoothingGroup
```

For each polygon corner, read a TextureVertex from the matching static or
dynamic corner pool. Its `vertexIndex` addresses the owning mesh's positions
and normals; its UVs belong to that corner. Do not index positions directly
with a corner-pool offset. Polygon IDs, material IDs and lightmap IDs are keys.
Stored polygons do not have an independent triangle-index array.

In neighborFlags, low 23 bits identify the neighbor polygon, bit 23 is crease
and high eight bits identify the neighbor edge. `ffffffff` means no neighbor.
`smooth` is not vertex alpha. `maxAngle` is in radians. `smoothingGroup` is an
opaque equality token; do not assume it is the KF2 smoothing-mask format.
Initial-radiosity values are emitted RGB keyed by polygon ID, not normals.

## Common level-object record

```text
LevelObject:
    TString name
    TMatrix4x3f objectToRoom
    TMatrix4x3f objectToParent
    TInt roomId
    TString parentDynamicMeshName
```

The outer Entries key and the embedded name are independent. Either can be
empty or different; preserve both. The two matrices have different frames.
For row-vector math, `pointWorld = pointLocal * objectToRoom * roomWorld`.
Parent-relative transforms must use the actual dynamic-parent chain.

## Lights, startpoints, characters and items

| Record | Fields after LevelObject, in order |
| --- | --- |
| StaticLight | TMatrix3x3f roomRotation; ten TFloat: R,G,B,A,area,intensity,hotspotAngle,falloffAngle,falloffRange,colorMultiplier |
| Startpoint | TInt type: observed 1 waypoint, 2 jump/player startpoint |
| Character | TString className; four Vector(TString): startup, death, activate, special |
| Trigger | TFloat radius; TInt type: 0 action, 1 player, 2 projectile, 3 character, 4 look-at |
| LevelItem | TString className |
| PointLight | Six TFloat: R,G,B,A,falloffRange,colorMultiplier |

Point-light table keys are integers. The last two point-light values have the
opposite order from the editable LVL point-light tail. Character message lists
are direct callbacks, not a replacement for the separate FSM table.

## FSM

```text
Fsm:
    LevelObject
    Vector(TString) states
    TString initialState
    Handler startup
    Map(TString, Handler) switchHandlers
    Map(TString, Handler) customHandlers
    Map(TString, Handler) entityHandlers

Handler:
    Vector(TString) before
    Map(TString, Vector(TString)) stateHandlers
    Vector(TString) after
```

The game executes Before, the matching current-state section, then After.
An empty state key is not a wildcard. State conditions and named switch/custom
events are different structures. Keep command strings and handler order.
A storage reader must not silently move commands between these lists.

## Dynamic meshes and animation

```text
DynamicMesh:
    StaticMesh
    LevelObject
    Entries(TString, Animation) animations
    TBool collisionsEnabled, bulletCollisionsEnabled, lightmapped
    TBool needsContinuousUpdate, pointLightsAffect, blocksExplosions
    BspSpan

Animation:
    TFloat durationSeconds
    TMatrix4x3f startTransform, endTransform
    Vector(TString) leavingFirstFrameMessages
    Vector(TString) returningFirstFrameMessages
    Vector(TString) reachingSecondFrameMessages
    SampleGraph translation
    SampleGraph rotation

SampleGraph:
    TInt marker = 113
    TInt version = 3
    TInt channelCount
    TInt frameCount
    repeat frameCount:
        TFloat samples[channelCount]
```

The stored graph is frame-major. `frameCount` is not a sample-rate value.
Translation values represent travel distance; rotation values parameterize
orientation interpolation. Do not clamp all graph values to 0 through 1.
Endpoint time checks are separate from interior interpolation.

A dynamic collision BSP can use vertices centered on the arithmetic mean of
all stored mesh vertices. Its runtime collision transform then restores the
center. In row-vector form, the observed relationship is:

```text
collisionVertex = modelVertex - meshVertexMean
collisionPosition = meshVertexMean * animationMatrix * parentToRoom
```

The hierarchy's origin matrix is separate from that centered collision frame.
Do not add the mean to stored animation endpoints to compensate a second time.
Hidden state and authored collision-channel flags are also separate controls.

## Rooms

```text
Room:
    Vector(TInt) staticMeshIds
    Vector(TString) staticLightNames
    Vector(TString) exitNames
    Vector(TString) startpointNames
    Vector(TString) fsmNames
    Vector(TString) characterNames
    Vector(TString) triggerNames
    Vector(TString) dynamicMeshNames
    Vector(TString) levelItemNames
    Vector(TInt) pointLightIds
    TString name
    TFloat aiNetDensity
    BspSpan
```

Rooms are serialized last. Their BSP spans select runtime collision data.
The external `.ai` navigation grid is not an extra LDB section. Reading an
LDB successfully does not prove that regenerating AI, compiling an editable
level or replaying all gameplay will succeed.
