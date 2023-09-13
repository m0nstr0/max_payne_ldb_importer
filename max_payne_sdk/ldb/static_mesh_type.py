from __future__ import annotations

from max_payne_sdk.ldb.texture_type import TextureContainer
from max_payne_sdk.ldb.texture_vertex_type import TextureVertexContainer
from max_payne_sdk.ldb.vertex_type import VertexContainer, Vertex, VertexUV
from max_payne_sdk.ldb.polygon_type import PolygonContainer, Geometry


class StaticMesh:
    def __init__(self, static_mesh_id: int, vertices: VertexContainer, normals: VertexContainer, transform, polygons: PolygonContainer) -> None:
        self.static_mesh_id: int = static_mesh_id
        self.vertices: VertexContainer = vertices
        self.normals: VertexContainer = normals
        self.transform = transform
        self.polygons: PolygonContainer = polygons
        self.texture_vertices: TextureVertexContainer = None

    def numPolygons(self):
        return len(self.polygons.polygons)

    def constructPolygon(self, id: int) -> Geometry:
        polygon = self.polygons.polygons[id]
        vertices: list[Vertex] = []
        normals: list[Vertex] = []
        uv: list[VertexUV] = []

        for i in range(polygon.num_vertices):
            texture_vertex = self.texture_vertices.texture_vertices[polygon.texture_vertex_idx + i]
            vertices.append(self.vertices.vertices[texture_vertex.vertex_idx])
            normals.append(self.normals.vertices[texture_vertex.vertex_idx])
            uv.append(texture_vertex.uv)

        return Geometry(vertices, normals, uv, polygon.material)


class StaticMeshContainer:
    def __init__(self) -> None:
        self.texture_vertices: TextureVertexContainer = TextureVertexContainer()
        self.static_meshes: list[StaticMesh] = []

    def __setitem__(self, key, value):
        self.static_meshes[key] = value

    def __getitem__(self, key):
        return self.static_meshes[key]

    def __len__(self):
        return len(self.static_meshes)

    def getById(self, static_mesh_id: int) -> StaticMesh:
        for static_mesh in self.static_meshes:
            if static_mesh.static_mesh_id == static_mesh_id:
                return static_mesh
        raise Exception("Static Mesh not found with id %i" % static_mesh_id)

    def getTextureVertices(self) -> TextureVertexContainer:
        return self.texture_vertices

    def getNum(self) -> int:
        return len(self.static_meshes)

    def add(self, static_mesh: StaticMesh) -> None:
        static_mesh.texture_vertices = self.texture_vertices
        self.static_meshes.append(static_mesh)
