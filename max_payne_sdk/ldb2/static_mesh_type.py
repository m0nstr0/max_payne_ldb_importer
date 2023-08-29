from dataclasses import dataclass

from max_payne_sdk.ldb.vertex_type import Vertex, VertexUV

@dataclass
class StaticMesh:
    vertices: [Vertex]
    normals: [Vertex]
    indices: [int]
    material_id: int
    uvs: [VertexUV]
    lightmap_uvs: [VertexUV]
    detail_texture_uvs: [VertexUV]

class StaticMeshContainer:
    def __init__(self):
        self.static_meshes: list[StaticMesh] = []

    def __getitem__(self, key):
        return self.static_meshes[key]

    def __len__(self):
        return len(self.static_meshes)

    def add(self, static_mesh: StaticMesh):
        self.static_meshes.append(static_mesh)