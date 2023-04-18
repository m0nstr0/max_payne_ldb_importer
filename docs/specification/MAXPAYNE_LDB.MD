# Max Payne 1 *.LDB file specification (Game Levels)

## Table of contents

* [File Structure](#file-structure)
  * [BSP](#bsp)
  * [File Version](#file-version)
  * [Materials](#materials)
  * [Exits](#exits)
  * [Static Meshes](#static-meshes)
  * [Dynamic Lights](#dynamic-lights)
  * [Waypoints](#waypoints)
  * [FSM](#fsm)
  * [Characters](#characters)
  * [Triggers](#triggers)
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
          M_Int material_id;
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

> **How to connect material with texture?**
>```c
>  function GetTextureIDBySourceFileName(string source_file_name) -> int {
>    for(i = 0; i != length(Texture); i++) {
>      if (Texture[i].source_file_name == source_file_name) {
>        return i;
>      } 
>    }
>  }
> 
>  forEach(MaterialProperty in MaterialProperties) {
>    diffuse_texture_id = GetTextureIDBySourceFileName(MaterialProperty.diffuse_texture_source_file_name);
>    alpha_texture_id = GetTextureIDBySourceFileName(MaterialProperty.alpha_texture_source_file_name);
>  }
>```

> **How to connect material with properties?**
> ```c
>   function GetMaterialCategoryForMaterialProperty(MaterialProperty) -> MaterialCategory {
>     forEach(MaterialCategory in MaterialCategories) {
>       if (MaterialCategory.category_name == MaterialProperty.category_name && 
>             MaterialCategory.material_name == MaterialProperty.material_name) 
>       {
>         return MaterialCategory;
>       }
>     }
>   }
> 
>  function GetMaterialPropertyForMaterialCategory(MaterialCategory) -> MaterialProperty {
>     forEach(MaterialProperty in MaterialProperties) {
>       if (MaterialCategory.category_name == MaterialProperty.category_name && 
>             MaterialCategory.material_name == MaterialProperty.material_name) 
>       {
>         return MaterialProperty;
>       }
>     }
>   }
> ```

> **How to get material ID for Static Meshes and Dynamic Meshes?**
> ```c
>   function GetMaterialCategoryByMaterialID(material_id) -> MaterialCategory {
>     forEach(MaterialCategory in MaterialCategories) {
>       if (MaterialCategory.material_id == material_id) {
>         return material_category;
>       }
>     }
>   }
>```

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

### Static Meshes

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
    } StaticMeshTextureVertices;
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

2. Static Meshes

```c
  struct {
    M_Int number_of_static_meshes;
    struct {
      M_Int group_id;           
      
      struct {
        M_Unsigned_Int number_of_vertices;
        M_Vector3 vertices[number_of_vertices];
      } VerticesPool;
      
      struct {
        unsigned byte type_tag; //0x1C - This is Max Payne's custom implementation of the std::vector container 
        M_Int number_of_normals;
        M_Vector3 normals[number_of_normals];
      } NormalsPool;
      
      M_Matrix4x3 Transform;
      
      struct {
        M_Int number_of_polygons;
        struct {
            M_Int polygon_id;
            M_Int texture_vertex_start_indx;
            M_Int number_of_vertices_in_polygon;
            M_Vector3 polygon_normal;
            M_Unsigned_Int engine_material_type;
            M_Int material_id;
            M_Int light_map_id;
            M_Float max_edge_length;    
            M_Float max_angle;
            M_Int smooting_group;
        } Polygon[number_of_polygons];
      } Polygons;
      
      struct {
        unsigned byte type_tag; //0x1F - This is Max Payne's custom implementation of the std::map container 
        M_Int number_of_elements;
        struct {
          M_Int key;
          M_Vector3 value;
        } InitialRadiosity[number_of_elements]
      }
    } StaticMesh[number_of_static_meshes]
  } StaticMeshes;
```

> **How build the polygons?**
> ```c
>   forEach(Polygon in Polygons) {
>     vertices = []
>     normals = []
>     uv = []
>     light_map_uv = []
>     tex_vertex = Polygon.texture_vertex_start_indx
>     for (i = 0; i != Polygon.number_of_vertices_in_polygon; i++) {
>       texture_vertices = StaticMeshTextureVertices[tex_vertex + i];
>       vertices.append(Polygon.VerticesPool[texture_vertices.vertex_index])
>       normals.append(Polygon.NormalsPool[texture_vertices.vertex_index])
>       uv.append(texture_vertices.uv);
>       light_map_uv.append(texture_vertices.light_map_uv);
>     }
>   }
>```
> To find material by **Polygon.material_id** look at [Materials Section](#materials)
> 
> To find light map use **LightMaps[Polygon.light_map_id]**
> 
> The polygon doesn't have a triangle index array so just connect vertices in order they are defined

### Dynamic Lights

1. Dynamic Lights

### Waypoints

1. Waypoints

### FSM

1. FSM

### Characters

2. Characters

### Triggers

3. Triggers

### Dynamic Meshes

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
    } DynamicMeshTextureVertices;
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

2. Dynamic Meshes

```c
  struct {
    M_Int number_of_dynamic_meshes;
    struct {
      M_String dynamic_mesh_name;
      
      struct {
        M_Unsigned_Int number_of_vertices;
        M_Vector3 vertices[number_of_vertices];
      } VerticesPool;
      
      struct {
        unsigned byte type_tag; //0x1C - This is Max Payne's custom implementation of the std::vector container 
        M_Int number_of_normals;
        M_Vector3 normals[number_of_normals];
      } NormalsPool;
      
      M_Matrix4x3 Transform;
      
      struct {
        M_Int number_of_polygons;
        struct {
            M_Int polygon_id;
            M_Int texture_vertex_start_indx;
            M_Int number_of_vertices_in_polygon;
            M_Vector3 polygon_normal;
            M_Unsigned_Int engine_material_type;
            M_Int material_id;
            M_Int light_map_id;
            M_Float max_edge_length;    
            M_Float max_angle;
            M_Int smooting_group;
        } Polygon[number_of_polygons];
      } Polygons;
      
      struct {
        unsigned byte type_tag; //0x1F - This is Max Payne's custom implementation of the std::map container 
        M_Int number_of_elements;
        struct {
          M_Int key;
          M_Vector3 value;
        } InitialRadiosity[number_of_elements]
      }

      struct {
         M_String name;
         M_Matrix4x3 object_to_room_transform;
         M_Matrix4x3 oject_to_parent_transform;
         M_Int room_id;
         M_String parent_dynamic_mesh_name;
      } Entity;
      
      struct {
        M_Int number_of_animations;

        struct {
          M_String animation_name;
          M_Float animation_length_in_seconds;
          M_Matrix4x3 start_transform;
          M_Matrix4x3 end_transform;

          struct {
            struct {
              unsigned byte type_tag;
              M_Int number_of_messages;
              M_String messages[number_of_messages];
            } OnLeavingFirstKeyFrameEvent;
  
            struct {
              unsigned byte type_tag;
              M_Int number_of_messages;
              M_String messages[number_of_messages];
            } OnReturningFirstKeyFrameEvent;
  
            struct {
              unsigned byte type_tag;
              M_Int number_of_messages;
              M_String messages[number_of_messages];
            } OnReachingSecondKeyFrameEvent;
          } FSM;

          struct {
            struct {
              M_Int header; //113
              M_Int major_version; //3 Major version
              M_Int minor_version; //1 Minor version
              M_Int sample_rate;
              M_Float curve_control_point[sample_rate];
            } TranslationGraph;
            struct {
              M_Int header; //113
              M_Int major_version; //3 Major version
              M_Int minor_version; //1 Minor version
              M_Int sample_rate;
              M_Float curve_control_point[sample_rate];
            } RotationGraph;
          } AnimationGraphs;
    
        } Animation[number_of_animations];
      } Animations;

      struct {
        M_Bool dynamic_collisions;
        M_Bool bullet_collisions;
        M_Bool light_mapped;
        M_Bool cont_update;
        M_Bool point_light_affected;
        M_Bool block_explosions;
      } Properties;

      struct {
        M_Int unknown1;
        M_Int unknown2;
        M_Int unknown3;    
        M_Int unknown4; 
      } BSP;
      
    } DynamicMesh[number_of_dynamic_meshes];
  } DynamicMeshes;
```

> Look at [Static Mesh Notes](#static-meshes) to figure out how to build the polygons

### Items

5. Items

### Point Lights

7. Point Lights

### Rooms

8. Rooms