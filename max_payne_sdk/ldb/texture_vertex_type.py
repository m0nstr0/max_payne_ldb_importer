from __future__ import annotations

from max_payne_sdk.ldb.vertex_type import VertexUV


class TextureVertex:
    def __init__(self, vertex_idx: int, uv: VertexUV, lightmap_uv: VertexUV, flags: uint, is_hidden: int) -> None:
        self.vertex_idx: int = vertex_idx
        self.uv: VertexUV = uv
        self.lightmap_uv: VertexUV = lightmap_uv
        self.flags: uint = flags
        self.is_hidden: int = is_hidden


class TextureVertexContainer:
    def __init__(self) -> None:
        self.texture_vertices: list[TextureVertex] = []

    def __setitem__(self, key, value):
        self.texture_vertices[key] = value

    def __getitem__(self, key):
        return self.texture_vertices[key]

    def __len__(self):
        return len(self.texture_vertices)
    def add(self, texture_vertex: TextureVertex) -> None:
        self.texture_vertices.append(texture_vertex)
