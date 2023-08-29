from __future__ import annotations

from max_payne_sdk.ldb.light_map_texture_type import LightMapTexture
from max_payne_sdk.ldb.material_type import Material
from max_payne_sdk.ldb.vertex_type import Vertex, VertexUV


class Polygon:
    def __init__(self, id: int, texture_vertex_idx: int, num_vertices: int, normal: int, type: uint, material: Material, lightmap: LightMapTexture, max_edge_length: float, max_angle: float, smoothing_group: int) -> None:
        self.id: int = id
        self.texture_vertex_idx: int = texture_vertex_idx
        self.num_vertices: int = num_vertices
        self.normal: int = normal
        self.type: uint = type
        self.material: Material = material
        self.lightmap: LightMapTexture = lightmap
        self.max_edge_length: float = max_edge_length
        self.max_angle: float = max_angle
        self.smoothing_group: int = smoothing_group


class PolygonContainer:
    def __init__(self) -> None:
        self.polygons: list[Polygon] = []

    def __getitem__(self, key):
        return self.polygons[key]

    def add(self, polygon: Polygon):
        self.polygons.append(polygon)


class Geometry:
    def __init__(self, vertices: list[Vertex], normals: list[Vertex], uv: list[VertexUV], material: Material) -> None:
        self.vertices: list[Vertex] = vertices
        self.normals: list[Vertex] = normals
        self.uv: list[VertexUV] = uv
        self.material: Material = material
