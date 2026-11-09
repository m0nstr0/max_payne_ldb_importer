# Max Payne KFS files

KFS normally stores skin geometry used by the character pipeline. It uses the
same chunk header, IDs and field types as [KF2](KF2.MD); there is no separate
KFS magic or wrapper.

MP1 KFS commonly uses Mesh version 1 with Geometry, Polygons and UVMapping
version 0. Mesh version 0 also occurs. Some KFS files contain animation tracks
rather than a complete mesh. Read the chunks that are present instead of
selecting a fixed layout from the filename extension.

A skin requires matching geometry, [SKD weights](SKD.MD), a skeleton hierarchy
and its transforms. Reading KFS alone does not recover the complete character.
Separate position and UV indices must be kept until any DCC vertex splitting
has a corresponding weight remap. Units, handedness and winding conversion
belong to the importer and must be applied consistently to meshes and bones.
