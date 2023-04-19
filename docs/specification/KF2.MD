# Max Payne 1 and Max Payne 2 *.KF2 file specification (Models, Camera paths, Light animations, Animations etc.)

## Table of contents

* [File Structure](#file-structure)
* [Chunks](#chunks)
  * [Chunk Format](#chunk-format)
  * [Top Level Chunks](#top-level-chunks)
  * [Sub-Chunks](#sub-chunks)
* [Top Level Chunks](#top-level-chunks-1)
  * [Material List](#material-list)
    * [Material List version 0](#material-list---version-0)
  * [Mesh](#mesh)
    * [Mesh version 1](#mesh---version-1)
    * [Mesh version 2](#mesh---version-2)
  * [Skin](#skin)
    * [Skin version 0]()
    * [Skin version 1]()
  * [Keyframe Animation](#keyframe-animation)
    * [Keyframe Animation version 0](#keyframe-animation---version-0)
    * [Keyframe Animation version 1](#keyframe-animation---version-1)
    * [Keyframe Animation version 2](#keyframe-animation---version-2)
    * [Keyframe Animation version 3](#keyframe-animation---version-3)
    * [Keyframe Animation version 4](#keyframe-animation---version-4)
    * [Keyframe Animation version 5](#keyframe-animation---version-5)
  * [Camera](#camera)
    * [Camera version 0](#camera---version-0)
  * [Environment](#environment)
    * [Environment version 0](#environment---version-0)
  * [PointLight](#point-light)
  * [Directional Light](#directional-light)
  * [SpotLight](#spot-light)
  * [Helper](#helper)
  * [PointLight Animation](#pointlight-animation)
  * [Directional Light Animation](#directional-light-animation)
  * [SpotLight Animation](#spotlight-animation)
* [Sub-Chunks](#sub-chunks-1)
  * [Material](#sub-chunk-material)
    * [Material version 0](#sub-chunk-material---version-0)
    * [Material version 1](#sub-chunk-material---version-1)
    * [Material version 2](#sub-chunk-material---version-2)
  * [Texture](#sub-chunk-texture)
    * [Texture version 1](#sub-chunk-texture---version-1)
  * [Node](#sub-chunk-node)
    * [Node version 0](#sub-chunk-node---version-0)
    * [Node version 1](#sub-chunk-node---version-1)
  * [Geometry](#sub-chunk-geometry)
    * [Geometry version 0](#sub-chunk-geometry---version-0)
    * [Geometry version 1](#sub-chunk-geometry---version-1)
  * [Polygons](#sub-chunk-polygons)
    * [Polygons version 0](#sub-chunk-polygons---version-0)
    * [Polygons version 1](#sub-chunk-polygons---version-1)
  * [Polygon](#sub-chunk-polygon)
    * [Polygon version 0](#sub-chunk-polygon---version-0)
  * [Smoothing](#sub-chunk-smoothing)
    * [Smoothing version 0](#sub-chunk-smoothing---version-0)
  * [Polygon Material](#sub-chunk-polygon-material)
    * [Polygon Material version 0](#sub-chunk-polygon-material---version-0)
    * [Polygon Material version 1](#sub-chunk-polygon-material---version-1)
  * [UV Mapping](#sub-chunk-uv-mapping)
    * [UV Mapping version 0](#sub-chunk-uv-mapping---version-0)
    * [UV Mapping version 1](#sub-chunk-uv-mapping---version-1)
  * [Animation](#sub-chunk-animation)
    * [Animation version 0](#sub-chunk-animation---version-0)
  * [Reference To Data](#sub-chunk-reference-to-data)
    * [Reference To Data version 0](#sub-chunk-reference-to-data---version-0)
    
## File Structure

The file contains different blocks of data (chunks) like mesh, animation, etc. 
Each of the block has a header that contains a unique ID. This ID points to the specific data type that the blocks containing. 
The algorithm of reading this file is simple:
1. Read the first 13 bytes from the input file it is the block header (chunk)
2. Compare chunk ID with the table below to figure out what kind of data the block contains 
3. Go to the specific section of this file to continue reading the input file 

## Chunks

### Chunk format

```c
  struct {
    byte chunk_tag;
    unsigned int chunk_id;
    unsigned int chunk_version;
    unsigned int chunk_size;
  }
```
* **{chunk_tag}** - constant **0x0C**
* **{chunk_id}** - type of the data that this chunk contains
* **{chunk_version}** - version of the data
* **{chunk_size}** - size in bytes of the data

### Top Level Chunks

| Chunk id   | Data                        |
|------------|-----------------------------|
| 0x0001000F | Material List               |
| 0x00010005 | Mesh                        |
| 0x00010014 | Skin                        |
| 0x00010012 | Keyframe Animation          |
| 0x00010001 | Camera                      |
| 0x00010002 | Point Light                 |
| 0x00010003 | Directional Light           |
| 0x00010004 | Spot Light                  |
| 0x00010015 | Environment                 |
| 0x00010016 | Helper                      |
| 0x00010017 | Point Light Animation       |
| 0x00010018 | Directional Light Animation |
| 0x00010019 | Spot Light Animation        |

### Sub-Chunks

| Chunk id    | Data              | Alias                    |
|-------------|-------------------|--------------------------|
| 0x0010010   | Material          | SubChunk_Material        |
| 0x00010011  | Texture           | SubChunk_Texture         |
| 0x00010000  | Node              | SubChunk_Node            |
| 0x00010006  | Geometry          | SubChunk_Geometry        |
| 0x00010007  | Polygons          | SubChunk_Polygons        |
| 0x00010008  | Polygon           | SubChunk_Polygon         |
| 0x0001000C  | Polygon Material  | SubChunk_PolygonMaterial |
| 0x0001000e  | UV Mapping        | SubChunk_UVMapping       |
| 0x0001001A  | Reference to Data | SubChunk_ReferenceToData |
| 0x0001000B  | Smoothing         | SubChunk_Smoothing       |
| 0x00010013  | Animation         | SubChunk_Animation       |

## Top Level Chunks

### Material List

This chunk contains list of directories with [**textures**](#sub-chunk-texture) and [**material sub-chunk**](#sub-chunk-material)

#### Material List - version 0

```c
  struct {
    M_String texture_dirs; // semicolon separated string with list of texture directories
    M_Int number_of_materials;
    SubChunk_Material material_sub_chunk[number_of_materials];
  } Chunk_MaterialListV0;
```

### Mesh

This chunks contains mesh data like polygons, uv, materials etc. 

> **IMPORTANT:** Sub-chunks in this chunk may or may not be missing you have to check it by yourself

> **IMPORTANT:** Sub-chunks in this chunk may be in different order

> **IMPORTANT:** You can treat this chunk as the skeleton of the mesh, just use [**node sub-chunks**](#sub-chunk-node) as bones

#### Mesh - version 1

```c
  struct {
    SubChunk_Node node;
    SubChunk_Geometry geometry;
    SubChunk_Polygons polygons;
    SubChunk_Smoothing smoothing;
    SubChunk_PolygonMaterial polygon_material;
    SubChunk_UVMapping uv_mapping;
    SubChunk_ReferenceToData reference_to_data;
  } Chunk_MeshV1;
```

#### Mesh - version 2

```c
  struct {
    SubChunk_Node node;
    SubChunk_Geometry geometry;
    SubChunk_Polygons polygons;
    SubChunk_PolygonMaterial polygon_material;
    SubChunk_UVMapping uv_mapping;
    SubChunk_ReferenceToData reference_to_data;    
  } Chunk_MeshV2;
```

### Skin

#### Skin - version 0

```c
  struct {
    struct {
      M_Int number_of_vertices;
      struct {
        M_Int vertex_Index;
        M_Int bone_Index;
        M_Float weight;
      } SkinData[number_of_vertices];
    } SkinData1;
    struct {
      M_Int number_of_vertices;
      struct {
        M_Int vertex_Index;
        M_Int bone_Index;
        M_Float weight;
      } SkinData[number_of_vertices];
    } SkinData2;
    struct {
      M_Int number_of_vertices;
      struct {
        M_Int vertex_Index;
        M_Int bone_Index;
        M_Float weight;
      } SkinData[number_of_vertices];
    } SkinData3;
    M_Int number_of_skin_objects;
    M_String skin_objects[number_of_skin_objects];
    M_Int number_of_skeleton_objects;
    M_String skeleton_objects[number_of_skeleton_objects];
    M_Int number_of_unknown;
    M_Vector3 unknown[number_of_unknown];    
  } Chunk_SkinV0;
```

#### Skin - version 1

```c
  struct {
    unsigned byte type_tag;
    M_Int number_of_skin_objects;
    M_String skin_objects[number_of_skin_objects];
    unsigned byte type_tag;
    M_Int number_of_skeleton_objects;
    M_String skeleton_objects[number_of_skeleton_objects];
    unsigned byte type_tag;
    M_Int number_of_vertex_indices;
    M_Int vertex_indices[number_of_vertex_indices];
    unsigned byte type_tag;
    M_Int number_of_bones_per_vertex;
    M_Int bones_per_vertex[number_of_bones_per_vertex];
    unsigned byte type_tag;
    M_Int number_of_list_per_vertex;
    M_Int bones_list_per_vertex[number_of_list_per_vertex];   
    unsigned byte type_tag;
    M_Int number_of_weights;
    TypeFloat weights[number_of_weights];   
    unsigned byte type_tag;
    M_Int number_of_primitives;
    M_Unsigned_Int vertex_num_per_primitive[number_of_primitives];
    unsigned byte type_tag;
    M_Int number_of_start_vertices_per_primitive;
    M_Unsigned_Int vertex_start_index_per_primitive[number_of_start_vertices_per_primitive];
  } Chunk_SkinV1;
```

### Keyframe Animation

#### Keyframe Animation - version 0

```c
  struct {
    SubChunk_Animation animation;
    M_String parent_name;
    M_Bool use_loop_interpolation;
    M_Unsigned_Int num_total_keyframes;
    M_Unsigned_Int num_key_frames;
    struct {
      M_Unsigned_Int frame_id;
      M_Matrix4x3 transform;
    } KeyFrames[num_key_frames];
  } Chunk_KeyframeAnimationV0;
```

> **Note:** Increase num_total_keyframes by 1

#### Keyframe Animation - version 1

```c
  struct: inherits_from Chunk_KeyframeAnimationV0 {
    M_Unsigned_Int num_visibility_frames;
    struct {
      M_Unsigned_Int frame_id;
      M_Float visibility;
    } VisibilityFrames[num_visibility_frames];            
  } Chunk_KeyframeAnimationV1;
```

> **Note:** Increase num_total_keyframes by 1

#### Keyframe Animation - version 2

```c
  struct: inherits_from Chunk_KeyframeAnimationV1 {
    M_Unsigned_Int loop_to_frame;       
  } Chunk_KeyframeAnimationV2;
```

> **Note:** Increase num_total_keyframes by 1

#### Keyframe Animation - version 3

```c
  struct: inherits_from Chunk_KeyframeAnimationV2 {
    M_Int frame_to_frame_interpolation_method;         
  } Chunk_KeyframeAnimationV3;
```

> **Note:** Increase num_total_keyframes by 1

#### Keyframe Animation - version 4

```c
  struct: inherits_from Chunk_KeyframeAnimationV3 {
    M_Bool maintain_matrix_scaling
  } Chunk_KeyframeAnimationV4;
```

> **Note:** Increase num_total_keyframes by 1

#### Keyframe Animation - version 5

```c
  struct: inherits_from Chunk_KeyframeAnimationV4 {
  } Chunk_KeyframeAnimationV5;
```

> **Note:** Keep num_total_keyframes as is

### Camera

This chunk contains [**node sub-chunk**](#sub-chunk-node) and camera properties 

#### Camera - version 0

```c
  struct {
    SubChunk_Node node;
    M_Float fov;
    M_Float front_plane;
    M_Float back_plane;
  } Chunk_CameraV0;
```

### Environment

This chunk contains level environment properties

#### Environment - version 0

```c
  struct {
    M_Unsigned_Char ambient_light_color_r;
    M_Unsigned_Char ambient_light_color_g;
    M_Unsigned_Char ambient_light_color_b;
    M_Unsigned_Char ambient_light_color_a;
    M_Unsigned_Char clearing_color_r;
    M_Unsigned_Char clearing_color_g;
    M_Unsigned_Char clearing_color_b;
    M_Unsigned_Char clearing_color_a;
  } Chunk_EnvironmentV0;
```

### Point Light

### Directional Light

### Spot Light

### Helper

### PointLight Animation

### Directional Light Animation

### SpotLight Animation

## Sub-Chunks

### Sub-Chunk Material

This sub-chunk contains material properties and [**texture sub-chunks**](#sub-chunk-texture)

#### Sub-Chunk Material - version 0

```c
  struct {
    M_String material_name;
    M_Bool is_two_sided;
    M_Bool is_fogging;
    M_Bool is_diffuse_combined;
    M_Bool is_invisible_geometry;
    M_Bool has_vertex_alpha;
    M_Int diffuse_color_type; //0x00 None 0x01 Color 0x02 Gourand
    M_Int specular_color_type; //0x00 None 0x01 Gourand
    M_Int lit_type; //0x00 Phong 0x01 Environment 0x02 UVW2
    M_Float ambient_color_r;
    M_Float ambient_color_g;
    M_Float ambient_color_b;
    M_Float ambient_color_a;
    M_Float diffuse_color_r;
    M_Float diffuse_color_g;
    M_Float diffuse_color_b;
    M_Float diffuse_color_a;
    M_Float specular_color_r;
    M_Float specular_color_g;
    M_Float specular_color_b;
    M_Float specular_color_a;
    M_Float vertex_alpha;
    M_Float specular_exponent;
    M_Int diffuse_texture_type; //0x00 Copy 0x01 Additive 0x02 Multiplicative
    M_Int reflection_texture_type; //0x00 Copy 0x01 Additive 0x02 Multiplicative
    M_Float emboss_factor;
    
    M_Bool has_diffuse_texture;
    if (has_diffuse_texture) {
      SubChunk_Texture diffuse_texture_sub_chunk;
    }
    
    M_Bool has_reflection_texture
    if (has_reflection_texture) {
      SubChunk_Texture reflection_texture_sub_chunk;
    }
    
    M_Bool has_bump_texture
    if (has_bump_texture) {
      SubChunk_Texture bump_texture_sub_chunk;
    }
    
    M_Bool has_opacity_texture
    if (has_opacity_texture) {
      SubChunk_Texture opacity_texture_sub_chunk;
    }
  } MaterialSubChunkV0;
```

#### Sub-Chunk Material - version 1

```c
  struct: inherits_from MaterialSubChunkV0 {
    M_Bool has_mask_texture;
    if (has_mask_texture) {
      SubChunk_Texture mask_texture_sub_chunk;
    }
    M_Int mask_texture_type; //0x00 UVW1 0x01 UVW2
    M_Bool has_lit;
  } MaterialSubChunkV1;
```

#### Sub-Chunk Material - version 2

```c
  struct: inherits_from MaterialSubChunkV1 {
    M_Bool unknown1;
    M_Bool unknown2;
    M_Int unknown3;
  } MaterialSubChunkV2;
```

### Sub-Chunk Texture

#### Sub-Chunk Texture - version 1

```c
  struct {
    M_String texture_name;
    M_Int number_of_mip_maps; //0x00 - Auoto; > 0x00 - number of mip maps
    M_Int filtering; //0x00 None; 0x01 Billinear; 0x02 Auto; 0x03 Trilinear; 0x04 Anisotropic
    M_Int number_of_textures;
    M_String texture_file_name[number_of_textures];
    if (number_of_textures > 0) {
        M_Bool is_automatic_start;
        M_Bool is_random_start_frame;
        M_Int start_frame;
        M_Int playback_fps;
        M_Int end_condition; //0x00 - Loop; 0x01 - PingPong; 0x02 - Hold
    }
  } TextureSubChunkV1;
```

### Sub-Chunk Node

#### Sub-Chunk Node - Version 0

```c
  struct {
    M_String object_name;
    M_String parent_object_name;
    M_Matrix4x3 object_to_parent;
    M_Bool has_parent;
  } NodeSubChunkV0;
```
#### Sub-Chunk Node - Version 1

```c
  struct: inherits_from NodeSubChunkV0 {
    M_String user_defined_string;
  } NodeSubChunkV1;
```

### Sub-Chunk Geometry

#### Sub-Chunk Geometry - version 0

```c
  struct {
    M_Int number_of_vertices;
    M_Vector3 vertices[number_of_vertices];
  } GeometrySubChunkV0;
```

#### Sub-Chunk Geometry - version 1

```c
  struct {
    M_Unsigned_Int number_of_vertices;
    struct {
      float x;
      float y;
      float z;
    } vertices[number_of_vertices];
    struct {
      float x;
      float y;
      float z;
    } normals[number_of_vertices];
    M_Unsigned_Int number_of_primitives;
    M_Unsigned_Int number_vertices_per_primitive[number_of_primitives];
  } GeometrySubChunkV1;
```

### Sub-Chunk Polygons

#### Sub-Chunk Polygons - version 0

```c
  struct {
    TypeInt number_of_polygons;
    SubChunk_Polygon polygons_indices[number_of_polygons];
    M_Int unknown1;
    M_Int unknown2;
  } PolygonsSubChunkV0;
```

#### Sub-Chunk Polygons - version 1

```c
  struct { 
    M_Unsigned_Int number_of_polygons;
    unsigned short polygons_indices[number_of_polygons];
    M_Unsigned_Int number_of_primitives;
    M_Unsigned_Int polygons_per_primitive[number_of_primitives];
  } PolygonsSubChunkV1;
```

### Sub-Chunk Polygon

#### Sub-Chunk Polygon - version 0

```c
  struct {
    M_Int number_of_vertices;
    M_Int vertex_indices[number_of_vertices];
  } PolygonSubChunkV0;
```

### Sub-Chunk Smoothing

#### Sub-Chunk Smoothing - version 0

```c
  struct {
    M_Int number_of_smoothing_groups;
    M_Unsigned_Int smoothing_group[number_of_smoothing_groups];   
  } SmoothingSubChunkV0;
```

### Sub-Chunk Polygon Material

#### Sub-Chunk Polygon Material - version 0

```c
  struct {
    M_Int number_of_materials;
    M_String material_name[number_of_materials];   
    M_Int number_of_polygons;
    M_Int material_index_for_polygon[number_of_polygons];
  } PolygonMaterialSubChunkV0;
```

#### Sub-Chunk Polygon Material - version 1

```c
  struct {
    M_Int number_of_materials;
    M_String material_name[number_of_materials]
  } PolygonMaterialSubChunkV1;
```

### Sub-Chunk UV Mapping

#### Sub-Chunk UV Mapping - version 0

```c
  struct {
    M_Int layer;
    M_Int number_of_polygons;
    SubChunk_Polygon polygons_indices[number_of_polygons];
    M_Int reserved1;
    M_Int reserved2;
    M_Int number_of_coordinates;
    M_Vector3 texture_coordinates_uvw[number_of_coordinates];   
  } UVMappingSubChunkV0;
```

#### Sub-Chunk UV Mapping - version 1

```c
  struct {
    M_Unsigned_Int layer;
    M_Unsigned_Int number_of_coordinates;
    struct {
        float u;
        float v;
        float w;
    } texture_coordinates_uvw[number_of_coordinates];
    M_Unsigned_Int number_of_primitives;
    M_Unsigned_Int coordinates_per_primitive[number_of_primitives];
  } UVMappingSubChunkV1;
```

### Sub-Chunk Reference To Data

#### Sub-Chunk Reference To Data - version 0

```c
  struct {
    M_String referenced_object_name;
  } ReferenceToDataSubChunkV0;
```

### Sub-Chunk Animation

#### Sub-Chunk Animation - version 0

```c
  struct {
    M_String object_name;
    M_Int fps;
    M_Bool is_looping;
  } AnimationSubChunkV0;
```