# Max Payne 1 *.LDB file specification (Game Levels)

## Table of contents

* [File Structure](#file-structure)
  * [BSP](#bsp)
  * [File Version](#file-version)
  * [Materials](#materials)
  * [Exits](#exits)
  * [Texture Vertices Pool](#texture-vertices-pool)
  * [Static Meshes](#static-meshes)
  * [Dynamic Lights](#dynamic-lights)
  * [Waypoints](#waypoints)
  * [FSM](#fsm)
  * [Characters](#characters)
  * [triggers](#triggers)
  * [Dynamic Meshes](#dynamic-meshes)
  * [Items](#items)
  * [Point Lights](#point-lights)
  * [Rooms](#rooms)
  
## File Structure

> This document uses a pseudocode to describe the file structure.  
> Please read ["Max Payne data types"](./DATA_TYPES.MD) document to get to know about Max Payne types.

The file has the following structure:

```
    [BSP]
    [File Version]
    [Materials]
    [Exits]
    [Texture Vertices Pool]
    [Static Meshes]
    [Dynamic Lights]
    [Waypoints]
    [FSM]
    [Characters]
    [Triggers]
    [Dynamic Meshes]
    [Items]
    [Point Lights]
    [Rooms]
```

### BSP

Max Payne uses BSP algorithm to divide the level and check for collisions. 
BSP block contains vertices, polygons, left half space, right half space etc.

1. BSP Vertices:

```c
struct {
  unsigned byte type_tag; //0x1C - This is Max Payne's custom implementation of the std::vector container 
  M_Int number_of_vertices;
  M_Vector3 vertices[number_of_vertices];
} BSPVertices;
```

2. BSP Polygons:

```c
struct {
  unsigned byte type_tag; //0x1C - This is Max Payne's custom implementation of the std::vector container 
  M_Int number_of_polygons;
  struct {
    M_Int start_bsp_vertex_indx;
    M_Int number_of_vertices_in_polygon;
    M_Int polygon_id_within_group;
    M_Int group_id;
    M_Vector3 polygon_normal;
    M_Vector3 polygon_pivot;
  } Polygon[number_of_polygons];
} BSPPolygons;
```
3. BSP Nodes

```c
struct {
  unsigned byte type_tag; //0x1C - This is Max Payne's custom implementation of the std::vector container 
  M_Int number_of_nodes;
  struct {
    M_Vector3 node_transform_or_orientation;
    M_Vector3 node_position;
    struct {
      M_Int start_indx_in_bsp_polygon_indx;
      M_Int num_polygons_in_space;
      M_Int next_bsp_node;
    } half_space_1;
    struct {
      M_Int start_indx_in_bsp_polygon_indx;
      M_Int num_polygons_in_space;
      M_Int next_bsp_node;
    } half_space_2;
  } BSPNode[number_of_nodes];
} BSPNodes;
```

4. BSP Polygons Indices

```c
struct {
  unsigned byte type_tag; //0x1C - This is Max Payne's custom implementation of the std::vector container 
  M_Int number_of_polygon_indices;
  M_Int indices[number_of_polygon_indices];
} BSPPolygonIndex;
```

### File Version

1. File Version

```c
  M_Int file_version;
```

### Materials

1. Textures List

```c
  struct {
      M_Int number_of_textures;
      struct {
          M_String sorce_file_name;
          M_Unsigned_Int file_type; //0x00 - TGA, 0x02 - SCX, 0x03 - PCX, 0x04 - JPG, 0x05 - DDS
          M_Int file_size;
          unsigned byte texture_file_data[file_size];
      } Texture[number_of_textures];
  } Textures;
```

2. Material Categories

```c
  struct {
     unsigned byte type_tag; //0x1F - This is Max Payne's custom implementation of the std::map container 
     M_Int number_of_categories;
     struct {
          M_Int category_id;
          unsigned byte type_tag; //0x25 - This is Max Payne's custom implementation of the std::pair container 
          M_String category_name;
          M_String material_name;
     } material_category[number_of_categories];
  } MaterialCategories;    
```
3. Material Categories Sorted

```c
    struct {
       unsigned byte type_tag; //0x1F - This is Max Payne's custom implementation of the std::map container 
       M_Int number_of_categories;
       struct {
            unsigned byte type_tag; //0x25 - This is Max Payne's custom implementation of the std::pair container 
            M_String category_name;
            M_String material_name;
            M_Int material_id;
       } Categories[number_of_categories];
    } SortedMaterialCategories;
```
4. Material Properties

```c
  struct {
    M_Int number_of_material_properties;
      struct {
        M_String category_name;
        M_Int number_of_materials_in_category;
        struct {
          M_String material_name;
          M_String diffuse_texture_source_file_name;
          M_String alpha_texture_source_file_name;
          M_Bool has_alpha_test;
          M_Bool has_adult_content;
        } Material[number_of_materials_in_category];
    } MaterailProperty[number_of_material_properties];
  } MaterailProperties;
```

5. Light Maps

```c
  struct {
    M_Int number_of_light_maps;
    struct {
      M_Int light_map_id;
      M_Unsigned_Int file_type; //0x00 - TGA, 0x02 - SCX, 0x03 - PCX, 0x04 - JPG, 0x05 - DDS
      M_Int file_size;
      unsigned byte texture_file_data[file_size];
    } LightMap[number_of_light_maps];
  } LightMaps;
```

### Exits (Portals)

1. Exits

```c
  struct {
    M_Int number_of_exits;
    struct {
      M_String exit_name;
      M_Unsigned_Int number_of_vertices;
      M_Vector3 vertices[number_of_vertices];
      M_Vector3 normal;
      M_Matrix4x3 transform;
      M_Int parent_room_id;
      M_Int destination_room_id;
      M_String destination_exit_name;
      struct {
        unsigned byte type_tag; //0x1C - This is Max Payne's custom implementation of the std::vector container
        M_Int number_of_convex_regions;
        struct {
          unsigned byte type_tag; //0x1C - This is Max Payne's custom implementation of the std::vector container
          M_Int number_of_points;
          M_Int points[number_of_points];
        } ConvexRegions[number_of_convex_regions];
      }
    } Exit[number_of_exits];
  } Exits;
```
### Texture Vertices Pool

1. Texture Vertices Pool

```c
    struct {
        unsigned byte type_tag; //0x1C - This is Max Payne's custom implementation of the std::vector container 
        M_Int number_of_texture_vertices;
        struct {
           M_Int vertex_index;
           M_Vector2 uv;
           M_Vector2 light_map_uv;
           M_Unsigned_Int flags;
           M_Bool is_smooth;
        } TextureVertex[number_of_texture_vertices]
    } TextureVertices;
```

> **vertex_index** points to the vertex from the static mesh or dynamic mesh vertices pool

> **flags** and **is_smooth** fields are using by Max Payne engine to do runtime tesselation of the geometry

>  **isCrease** 
> ```c
>  function IsCrease() -> bool {
>    return flags >> 0x17 & 0x01
>  }
> ```

>  **GetNeighbor** 
> ```c
>  function GetNeighbor() -> unsigned int {
>    return flags == 0xffffffff ? flags : flags & 0x7fffff
>  }
> ```

>  **GetNeighborEdge** 
> ```c
>  function GetNeighborEdge() -> unsigned int {
>    return flags == 0xffffffff ? flags : flags >> 0x18
>  }
> ```

### Static Meshes

1. Static Meshes

### Dynamic Lights

1. Dynamic Lights

### Waypoints
### FSM
### Characters
### Triggers
### Dynamic Meshes
### Items
### Point Lights
### Rooms