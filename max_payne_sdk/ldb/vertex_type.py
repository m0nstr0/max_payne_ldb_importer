from __future__ import annotations


class Vertex:
    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z


class VertexContainer:
    def __init__(self) -> None:
        self.vertices: list[Vertex] = []

    def __getitem__(self, key):
        return self.vertices[key]

    def add(self, vertex: Vertex) -> None:
        self.vertices.append(vertex)


class VertexUV:
    def __init__(self, u: float, v: float) -> None:
        self.u: float = u
        self.v: float = v
