# Max Payne 1 *.LDB file specification (Game Levels)

## Table of contents

* [File Structure](#file-structure)
  * [BSP](#bsp)
  * [Materials](#materials)
  * [Exits](#exits)
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
  int8_t type_tag; //0x1C - This is Max Payne's custom implementation of the std::vector container 
  M_Int number_of_vertices;
  M_Vector3 vertices[number_of_vertices];
} BSPVertices;
```

2. BSP Polygons:

```c
struct {
  int8_t type_tag; //0x1C - This is Max Payne's custom implementation of the std::vector container 
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
  int8_t type_tag; //0x1C - This is Max Payne's custom implementation of the std::vector container 
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
  int8_t type_tag; //0x1C - This is Max Payne's custom implementation of the std::vector container 
  M_Int number_of_polygon_indices;
  M_Int indices[number_of_polygon_indices];
} BSPPolygonIndex;
```

### Materials
### Exits
### Static Meshes
### Dynamic Lights
### Waypoints
### FSM
### Characters
### Triggers
### Dynamic Meshes
### Items
### Point Lights
### Rooms