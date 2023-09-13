from __future__ import annotations

from max_payne_sdk.ldb.entity_properties_type import EntityProperties
from max_payne_sdk.ldb.texture_type import TextureContainer
from max_payne_sdk.ldb.texture_vertex_type import TextureVertexContainer
from max_payne_sdk.ldb.vertex_type import VertexContainer, Vertex, VertexUV
from max_payne_sdk.ldb.polygon_type import PolygonContainer, Geometry
from max_payne_sdk.ldb.animation_type import AnimationContainer


class DynamicMeshConfig:
    def __init__(self, dynamic_collisions: int, bullet_collisions: int, light_mapped: int, cont_update: int, pointlight_affected: int, block_explosions: int) -> None:
        self.dynamic_collisions: int = dynamic_collisions
        self.bullet_collisions: int = bullet_collisions
        self.light_mapped: int = light_mapped
        self.cont_update: int = cont_update
        self.pointlight_affected: int = pointlight_affected
        self.block_explosions: int = block_explosions


class DynamicMesh:
    def __init__(self, shared_name: str, properties: EntityProperties, vertices: VertexContainer, normals: VertexContainer, transform, polygons: PolygonContainer, animations: AnimationContainer, config: DynamicMeshConfig) -> None:
        self.shared_name: str = shared_name
        self.properties: EntityProperties = properties
        self.vertices: VertexContainer = vertices
        self.normals: VertexContainer = normals
        self.transform = transform
        self.polygons: PolygonContainer = polygons
        self.animations: AnimationContainer = animations
        self.config: DynamicMeshConfig = config
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


class DynamicMeshContainer:
    def __init__(self) -> None:
        self.texture_vertices: TextureVertexContainer = TextureVertexContainer()
        self.dynamic_meshes: list[DynamicMesh] = []

    def addDynamicMesh(self, dynamic_mesh: DynamicMesh):
        dynamic_mesh.texture_vertices = self.texture_vertices
        self.dynamic_meshes.append(dynamic_mesh)

    def getTextureVertices(self) -> TextureVertexContainer:
        return self.texture_vertices

    def getBySharedName(self, name: str) -> DynamicMesh:
        for dynamic_mesh in self.dynamic_meshes:
            if dynamic_mesh.shared_name == name:
                return dynamic_mesh
        raise Exception("Dynamic Mesh not found with name %s" % name)
