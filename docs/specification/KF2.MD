# Max Payne 1 and Max Payne 2 *.KF2 file specification (Models, Camera paths, Light animations, Animations etc.)

## Table of contents

* [File Structure](#file-structure)
* [Chunks](#chunks)
  * [Chunk Format](#chunk-format)
  * [Top Level Chunks](#top-level-chunks)
  * [Sub-Chunks](#sub-chunks)
* [Material List](#material-list)
* [Node](#node)
* [Mesh](#mesh)
* [Skin](#skin)
* [Keyframe Animation](#keyframe-animation)
* [Camera](#camera)
* [PointLight](#point-light)
* [Directional Light](#directional-light)
* [SpotLight](#spot-light)
* [Environment](#environment)
* [Helper](#helper)
* [PointLight Animation](#pointlight-animation)
* [Directional Light Animation](#directional-light-animation)
* [SpotLight Animation](#spotlight-animation)
  
## File Structure

This file contains different blocks of data (chunks) like mesh, animation, etc. 
Each block has header contains unique ID. This ID points to the specific data type that the blocks containing. 
The algorithm of reading this file is simple:
1. Read the first 13 bytes from the input file this is the block header (chunk)
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

| Chunk id    | Data              |
|-------------|-------------------|
| 0x0010010   | Material          |
| 0x00010011  | Texture           |
| 0x00010000  | Node              |
| 0x00010006  | Geometry          |
| 0x00010007  | Polygons          |
| 0x00010008  | Polygon           |
| 0x0001000C  | Polygon Material  |
| 0x0001000e  | UV Mapping        |
| 0x0001001A  | Reference to Data |
| 0x0001000B  | Smoothing         |
| 0x00010013  | Animation         |

## Material List

## Node

## Mesh

## Skin

## Keyframe Animation

## Camera

## Point Light

## Directional Light

## Spot Light

## Environment

## Helper

## PointLight Animation

## Directional Light Animation

## SpotLight Animation