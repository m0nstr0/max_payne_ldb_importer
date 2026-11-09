# Max Payne / MaxED LVL version 20

LVL is the editable Max Payne 1 level format. This page covers document
version 20 and object format 2. It is not the compiled [LDB format](MAXPAYNE_LDB.MD)
or the MP2 [LV2 format](MAXPAYNE2_LV2.MD). Other document versions and legacy
branches must not be assumed to use the layouts below.

## Two kinds of serialization

The outer stream uses fixed-size little-endian values and MFC CString lengths.
Some length-prefixed blobs contain a separate tagged stream. Use
[DATA_TYPES.MD](DATA_TYPES.MD) only inside those tagged records, not for the
entire outer file. No C/C++ alignment padding is added.

| Notation | Stored form |
| --- | --- |
| u8 / bool8 | One raw byte; write bool as 0/1 |
| u16 / u32 / i32 | Raw integer of the stated width |
| f32 / f64 | Raw IEEE 754 floating-point value |
| DVec3 | Three raw f64 values |
| Blob | Raw u32 byteCount, then exactly byteCount raw bytes |
| CString | Length prefix below, then bytes without a NUL |

CString length:

```text
u8 first
if first < ff: length = first
else:
    u16 extended
    if extended == ffff: u32 length
    else if extended == fffe: separate Unicode-string branch
    else: length = extended
raw bytes[length]
```

The described ANSI profile stores narrow bytes. Preserve their encoding.
The Unicode marker requires a separate length/UTF-16 path; it must not be
mistaken for an ANSI length of 65534. Lengths 65534/65535 need the long prefix
because those u16 values are reserved. A CString is not a tagged TString.

## File structure

F is the file mask, P the polygon-feature mask and M the mesh-feature mask.
Mask values in the tables are hexadecimal. A mask bit usually controls whether bytes exist; it is not the value of the
bool that follows it.

```text
u32 fileFlags                         # F
if F & 0x0008: u32 version             # 20
if F & 0x0002: TextureTable
if F & 0x0004: MaterialTable
if F & 0x0001:
    if F & 0x1000: Blob settings
    else: legacy settings             # not specified here
u32 polygonFeatures                   # P
u32 meshFeatures                      # M
u32 objectFormat = 2
NodeBody(type=2)                       # World; no extra root type word
if F & 0x0010:
    u32 count
    u32 values[count]                 # meaning unknown
if F & 0x8000: Blob editorTrailer
EOF
```

A common complete profile uses F=`0000ffef`, P=`0003ffff` and M=`0001ffff`.
An LDB-to-LVL reconstruction may clear P bit 0x0200 because the compiled level
does not retain the original editor HDR buffers. These are known writing
profiles, not universal constants of every LVL file.

| F bit | Stored feature |
| --- | --- |
| 0001 | Document settings |
| 0002 | Texture table |
| 0004 | Material table |
| 0008 | Version |
| 0010 | Trailing u32 array |
| 0020 | Embedded image-format field |
| 0040 | Optional events blob in each common object record |
| 0080 | Two trailing bools in events blobs |
| 0200 | First extra material bool |
| 0800 | Material alpha-test bool |
| 1000 | Settings use a length-prefixed blob |
| 2000 | Startpoint type word |
| 4000 | Material adult-content bool |
| 8000 | Opaque editor trailer |

The separate meanings of F bits 0100/0400 are not established. Keep them.
P and M apply across the scene; changing one affects every relevant record.

## Textures and materials

```text
TextureTable:
    u32 textureCount
    repeat textureCount:
        if F & 0x0020: u32 imageFormat
        u32 imageByteCount
        CString name
        raw u8 imageBytes[imageByteCount]

MaterialTable:
    u32 categoryCount
    repeat categoryCount:
        u32 materialCount
        CString categoryName
        repeat materialCount:
            CString materialName, textureName
            u32 materialFlags
            if materialFlags & 1: CString alphaTextureName
            if materialFlags & 2:
                CString reflectionTextureName
                f64 reflectionAmount
            if materialFlags & 4: CString bumpTextureName
            i32 parameter1, parameter2
            f64 width, height
            if F & 0x0200: bool8 unknownFlag1
            if F & 0x0800: bool8 alphaTest
            if F & 0x4000: bool8 adultContent
```

Image length appears before the name; the image bytes appear after it.
Observed LVL image formats include 0 TGA, 3 PCX and 4 JPEG. Preserve other
stored format codes; see [IMAGES.MD](IMAGES.MD) for the common image family. Do not infer an image's format solely from
its name. Preserve the two material integers and the unknown bool. Category
properties such as collision channels also come from an external database.

## Settings blob

This is a tagged stream: TInt fieldCount, followed by that many fields from
the table in order. There are 44 known fields. A shorter count leaves later
settings at the editor's defaults; those defaults are not all specified here.
A zero-field payload is `14 00`, which differs from a zero-byte blob.
Preserve an unrecognized longer payload instead of guessing new settings.

| Index | Tagged type | Field |
| ---: | --- | --- |
| 0 | `TFloat` | `angle_snap` |
| 1 | `TFloat` | `back_clip_plane` |
| 2 | `TFloat` | `front_clip_plane` |
| 3 | `TFloat` | `unknown_float1` |
| 4 | `TFloat` | `unknown_float2` |
| 5 | `TFloat` | `uv_scale_metres_uvu` |
| 6 | `TFloat` | `unknown_float3` |
| 7 | `TInt` | `select_culled_polygons` |
| 8 | `TInt` | `clear_render_screen_on_f2_press` |
| 9 | `TInt` | `unknown_int2` |
| 10 | `TInt` | `unknown_int3` |
| 11 | `TInt` | `flip_faces_after_mesh_creation` |
| 12 | `TFloat` | `texture_increment` |
| 13 | `TInt` | `save_load_triangle_data` |
| 14 | `TInt` | `vertex_ticks` |
| 15 | `TInt` | `unknown_int4` |
| 16 | `TDouble` | `lightmap_res_txl_m` |
| 17 | `TUInt` | `radiosity_viewport_size` |
| 18 | `TUInt` | `radiosity_passes` |
| 19 | `TFloat` | `radiosity_boost` |
| 20 | `TFloat` | `radiosity_backplane` |
| 21 | `TInt` | `apply_paste_displacement` |
| 22 | `TInt` | `unknown_int5` |
| 23 | `TInt` | `average_lightmap_borders` |
| 24 | `TFloat` | `kbd_t_tlt_angle` |
| 25 | `TInt` | `new_grid_units` |
| 26 | `TInt` | `display_exits` |
| 27 | `TInt` | `display_keypoints` |
| 28 | `TInt` | `hide_other_objects_selrend` |
| 29 | `TInt` | `use_exits_in_radiosity_calcs` |
| 30 | `TInt` | `unknown_int6` |
| 31 | `TInt` | `connected_rooms` |
| 32 | `TInt` | `display_non_visible_rooms_bbs` |
| 33 | `TInt` | `exit_acceleration` |
| 34 | `TUChar` | `default_light_r` |
| 35 | `TUChar` | `default_light_g` |
| 36 | `TUChar` | `default_light_b` |
| 37 | `TUChar` | `default_light_a` |
| 38 | `TUInt` | `texture_display` |
| 39 | `TBool` | `unknown_bool1` |
| 40 | `TBool` | `unknown_bool2` |
| 41 | `TBool` | `unknown_bool3` |
| 42 | `TUInt` | `unknown_int7` |
| 43 | `TBool` | `unknown_bool4` |

Names containing `unknown` remain unknown. Integer switches must not be
rewritten as TBool. `texture_display` values are 0 diffuse,1 diffuse/lightmap,
2 lightmap only and 4 light layer only; this is not the MP2 rendering-mode enum.

## Objects and hierarchy

```text
NodeBody(type):
    TypePrefix(type)
    f64 position[3]
    f64 rotation[9]                  # rows00..22
    f64 cachedBoundsMin[3]
    f64 cachedBoundsMax[3]
    f64 cachedRadius
    u32 visibilityState
    CString name
    if F & 0x0040:
        bool8 hasEvents
        if hasEvents: Blob events
    if type == 1: MeshBody
    u32 childCount
    repeat childCount:
        u32 childType
        NodeBody(childType)
    if type == 1 and M & 0x0010: PolygonGroups
    if type == 10: f32 R,G,B,A,colorMultiplier,falloffRange
```

The 19 doubles are fixed fields, without an array count. Translation precedes
rotation on disk. Pose is parent-relative. For row-vector math:
`world = local * parentWorld`. Bounds are cached data; their space and update
rules should be handled separately from vertex coordinates.

| Type | Object | Prefix before the common record |
| ---: | --- | --- |
| 1 | Mesh, including room geometry | None |
| 2 | World | None |
| 3 | Startpoint | u32 startpointType if F&2000 |
| 4 | Trigger | CString className; f64 radius |
| 5 | Character | CString className; f64 radius |
| 6 | Level item | CString className; f64 radius |
| 7 | Sound entity | CString className; f64 radius |
| 8 | Unknown | Not specified |
| 9 | FSM/logical object | None |
| 10 | Point light | CString className; f64 radius |

World is special; do not use type 2 for an arbitrary nested logical group.
An unknown entity cannot safely be skipped: a node and its children have no
single enclosing byte length. Point-light values and mesh polygon groups come
AFTER children, not inside their earlier object body.

## MeshBody and options

```text
if M & 0x0001: u32 meshParameter
if M & 0x0002: u32 roomType
u32 vertexCount
DVec3 positions[vertexCount]
u32 polygonCount
Polygon polygons[polygonCount]
if M & 0x0004:
    bool8 dynamic
    if dynamic:
        Blob dynamicData
        CString dynamicName, dynamicScript
MeshOptions
```

Read MeshOptions in the following order, not in numeric bit order:

| Order | M bit | Fields |
| ---: | --- | --- |
| 1 | 0008 | bool8 exportGeometry,exportLights |
| 2 | 0020 | bool8 collisionsEnabled |
| 3 | 0040 | bool8 lightmapped |
| 4 | 8000 | bool8 pointLightsAffect |
| 5 | 0080 | bool8 needsContinuousUpdate |
| 6 | 0100 | bool8 hasEditorBsp; if true Blob editorBsp |
| 7 | 0200 | bool8 bulletCollisionsEnabled |
| 8 | 0400 | f32 aiNetDensity |
| 9 | 2000 | bool8 castNoShadows |
| 10 | 4000 | bool8 insertIntoCollisionBsp |
| 11 | 10000 | bool8 blocksExplosions |

`meshParameter` and the complete roomType enum are not established. The saved
editor BSP is not the compiled LDB BSP. Preserve its blob. AI density stores
float bits, including the observed FLT_MAX sentinel; it is not a numeric u32.

PolygonGroups, after children:

```text
u32 groupCount
repeat groupCount:
    CString name
    bool8 selected
    u32 polygonIndexCount
    u32 polygonIndices[polygonIndexCount]
    if M & 0x0800:
        bool8 tessellationEnabled
        f32 maxEdgeLength, maxAngleDegrees
    if M & 0x1000: bool8 unknownFlag2
```

Group indices are local polygon ordinals. Selection and tessellation are
separate. Group angles are stored in degrees; compiled LDB angles use radians.

## Polygon record

```text
u32 edgeCount
f64 parameters[35]                  # fixed fields, table below
if P & 0x0010: u32 polygonFlags
if P & 0x0004: u8 R,G,B,A
if P & 0x0020: f64 emissionIntensity
if P & 0x0040: f64 lightmapScale
if P & 0x0100: u32 geometryType
if P & 0x0400: u32 exitId
if P & 0x0800: CString exitName
if P & 0x0001: CString categoryName, materialName
if P & 0x0008:
    repeat edgeCount: u32 fromVertex,toVertex
else:
    legacy edge data                # not specified here
if P & 0x0002:
    u32 fragmentCount
    repeat fragmentCount:
        if not (P & 0x1000): raw u8 legacyPlaneCache[24]
        if P & 0x2000: u32 indexCount
        else: indexCount = 3         # no count stored
        u32 meshVertexIndices[indexCount]
if P & 0x0080: LightmapRecord
if P & 0x4000: AdditionalUvMappings
if P & 0x10000: f32 hotspotAngle,falloffAngle,falloffRange,colorMultiplier
```

| Parameter indices | Meaning |
| --- | --- |
| 0..2 | Polygon normal |
| 3..5 | Secondary stored normal |
| 6..8 | Temporary vector discarded by the observed loader |
| 9..14 | Two legacy vectors; full meaning unknown |
| 15..17 | UV plane-normal cache |
| 18..20 | UV origin |
| 21..29 | UV basis U,V,N |
| 30..31 | U,V offsets |
| 32..34 | Point on the polygon plane |

The field called alpha in an older model is emissionIntensity, not material
opacity. RGBA bytes and emission intensity are separate. Preserve unknown
polygonFlags. Geometry type 0 is ordinary, 4 is an exit, and types 1/2 export as
special LDB material modes 2/3. Type 3 is not a safe substitute for an unknown
runtime material mode.

Edges and fragments both use the owning mesh's vertex array. Preserve their
order and stored tessellation. A portal exitId refers to the destination
polygon in scene-wide polygon order, not a room ID or a local polygon index.
The ordinary absent value is ffffffff. Reordering nodes or polygons can require
rebinding portal IDs.

## Planar mapping and additional UVs

A PlanarMapping is 17 raw f64 values: normal cache[3], origin[3], basis[9],
offsetU and offsetV. No count or tagged matrix is inserted. Project a point by
subtracting the origin, applying the inverse basis and adding UV offsets.
The basis includes scale; normalizing it changes the mapping.

```text
AdditionalUvMappings:
    u32 mappingCountIncludingPrimary
    repeat max(mappingCountIncludingPrimary - 1, 0):
        if P & 0x20000:
            u32 mappingId
            PlanarMapping mapping
        else:
            legacy mapping data      # not specified here
```

The primary mapping is already in parameters 15..31. Additional mappings have
their own bases. A mappingId is not automatically a texture or material ID.

## Lightmaps and HDR

```text
LightmapRecord:
    PlanarMapping mapping
    f64 minU,minV,maxU,maxV
    u32 width,height
    f64 texelStepU,texelStepV
    Blob primaryImage
    if primaryImage.byteCount != 0 and P & 0x0200: Blob hdrData
    if P & 0x8000: Blob secondaryImage
```

The fixed prefix before primaryImage's length is 192 bytes. The secondary
blob can exist even when the primary image is empty. Empty image data does not
remove the mapping record. Keep a valid mapping basis for an authored empty
lightmap; all-zero bases can make editor operations invalid.

Observed HDR payloads have TInt width, TInt height and raw pixels. One layout
uses 6 bytes per RGB pixel, another 16 bytes per RGBA-float pixel. The packed
16-bit component is not IEEE binary16:

```text
value = 0                                                     if h == 0
value = ldexp(((h & 0x7ff) | 0x800) / 4096, (h >> 11) - 16)    otherwise
```

Pixels are row-major. Do not invent HDR data from an LDR lightmap. The exact
editor initialization requirements for some HDR payloads remain unknown;
merely matching a buffer's dimensions and byte count does not prove load safety.
An explicit export that omits HDR must remove the conditional blob and clear
its feature bit together, while keeping the original source separately.

## Events blob

All values below are tagged. Vector uses marker 1c, Set 1d and Map 1f; each
marker is followed by TInt count. Collection elements follow their own schema.

```text
Set(TString) declaredStates
TString initialState
Set(TString) customEvents
Map(TString eventName, EventHandler) handlers
if F & 0x0080: TBool storedFlag1,storedFlag2

EventHandler:
    Vector(Command) before
    Map(TString stateName, Vector(Command)) stateHandlers
    Vector(Command) after

Command:
    TString sourceText,functionName,receiverName
    Vector(TString) arguments
    TBool raw
```

The second declared-name set contains custom events, not more states.
Keep raw command text and parsed fields. Ordinary state conditions use a
current-state lookup; an empty key is not a wildcard. Animation(name) handlers
have a special use for Leave1st/Enter1st/Enter2nd callback channels; those names
are not ordinary declared states. The meaning of both trailing bools is not
fully established. A reader should preserve rather than normalize them.

## Dynamic-data blob

```text
TInt keyframeCount
repeat keyframeCount:
    TString name
    TDouble matrixValues[12]         # twelve separate tags
TInt transitionCount
repeat transitionCount:
    TString name
    RuntimeAnimation animation
    TDouble storedParameter
    TString firstKeyframeName,secondKeyframeName
    EditorCurve translationCurve
    EditorCurve rotationCurve
EOF blob

RuntimeAnimation:
    TFloat durationSeconds
    TMatrix4x3f start,end
    Vector(TString) leavingFirstFrameMessages
    Vector(TString) returningFirstFrameMessages
    Vector(TString) reachingSecondFrameMessages
    SampleGraph translation
    SampleGraph rotation
```

SampleGraph is the marker 113/version 3 frame-major graph described in
[MP1 LDB](MAXPAYNE_LDB.MD#dynamic-meshes-and-animation). Named key matrices use
separate TDouble fields, unlike the single float-matrix tag in RuntimeAnimation.
Endpoints are in their parent frame, not already world space.

EditorCurve has the marker 113/version 1..3 layout described as EditorGraph in
[LV2](MAXPAYNE2_LV2.MD#editor-graph). Its fixed parameter counts and point records
are the same stored structure. It is not a SampleGraph despite sharing marker 113.
The older unnamed parameters should be kept when their UI meaning is unknown.
Editing a curve and regenerating samples is separate from preserving a source
file's two possibly different representations.

## Validation and limits

Check flags before reading optional fields. Keep raw and tagged streams
separate, validate blob lengths and index domains, and require the expected
end of every supported record. Unknown node types and unsupported legacy
branches cannot be skipped by guessing. Compiled LDB does not retain all
editor bounds, curves, HDR buffers, group names or authoring choices, so an
LDB-to-LVL reconstruction must state its defaults and approximations.
