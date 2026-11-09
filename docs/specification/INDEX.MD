# Max Payne file specifications

These pages describe the known formats in plain English. A layout describes
stored bytes; it does not by itself promise Maya support or complete game
behavior. Read the shared notation before implementing a reader or writer.

| Page | Game / role | Maya importer scope |
| --- | --- | --- |
| [Data types](DATA_TYPES.MD) | Shared tagged values and chunk headers | Used by SDK readers |
| [MP1 LDB](MAXPAYNE_LDB.MD) | Compiled Max Payne 1 level, revision 32 | LDB import; includes BSP collision notes |
| [MP2 LDB](MAXPAYNE2_LDB.MD) | Compiled Max Payne 2 level, revision 34 | LDB import |
| [MP1 LVL](MAXPAYNE_LVL.MD) | Editable MaxED level, version 20 | Format reference; no LVL Maya reader |
| [MP2 LV2](MAXPAYNE2_LV2.MD) | Editable MaxED2 level, document format 3 | Format reference; no LV2 Maya reader |
| [KF2](KF2.MD) | Models, materials, camera and animation data | Supported components only |
| [KFS](KFS.MD) | KF2-family skin geometry and related data | Uses the KF2 reader |
| [SKD](SKD.MD) | Bone weights, versions 0 and 1 | Matching mesh and skeleton required |
| [Images](IMAGES.MD) | PCX, SCX/RIX3 and TGA output | Dependency-free conversion |

[Revision notes](REVIEW_CORRECTIONS.MD) summarize the corrected descriptions.
Unknown layouts and unsupported versions are identified on each page. Do not
substitute a related game's layout, infer a field from a filename, or scan raw
payloads for bytes that happen to resemble tags.
