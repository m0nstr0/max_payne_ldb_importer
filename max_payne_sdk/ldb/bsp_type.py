from __future__ import annotations

from max_payne_sdk.ldb.vertex_type import Vertex


class BSPVertex(Vertex):
    pass


class BSPPolygon:
    def __init__(self, vertex_idx: int, num_vertices: int, polygon_id: int, static_mesh_id: int, normal: Vertex, pivot: Vertex) -> None:
        self.vertex_idx : int = vertex_idx
        self.num_vertices : int = num_vertices
        self.polygon_id : int = polygon_id
        self.static_mesh_id : int = static_mesh_id
        self.normal : Vertex = normal
        self.pivot : Vertex = pivot


class BSPNode:
    def __init__(self, normal: Vertex, pivot: Vertex, unk1: int, unk2 : int, unk3 : int, unk4 : int, unk5 : int, unk6: int) -> None:
        self.normal : Vertex = normal
        self.pivot : Vertex = pivot
        self.unk1 : int = unk1
        self.unk2 : int = unk2
        self.unk3 : int = unk3
        self.unk4 : int = unk4
        self.unk5 : int = unk5
        self.unk6 : int = unk6


class BSPPolygonIndex:
    def __init__(self, polygon_id: int) -> None:
        self.polygon_id: int = polygon_id


class BSPVertexContainer:
    def __init__(self) -> None:
        self.vertices: list[BSPVertex] = []

    def add(self, vertex: BSPVertex) -> None:
        self.vertices.append(vertex)


class BSPPolygonsContainer:
    def __init__(self) -> None:
        self.polygons: list[BSPPolygon] = []

    def add(self, polygon: BSPPolygon) -> None:
        self.polygons.append(polygon)


class BSPNodesContainer:
    def __init__(self) -> None:
        self.nodes: list[BSPNode] = []

    def add(self, node: BSPNode) -> None:
        self.nodes.append(node)


class BSPPolygonIndicesContainer:
    def __init__(self) -> None:
        self.indices: list[BSPPolygonIndex] = []

    def add(self, index: BSPPolygonIndex) -> None:
        self.indices.append(index)


class BSPContainer:
    def __init__(self) -> None:
        self.vertices: BSPVertexContainer = BSPVertexContainer()
        self.polygons: BSPPolygonsContainer = BSPPolygonsContainer()
        self.nodes: BSPNodesContainer = BSPNodesContainer()
        self.indices: BSPPolygonIndicesContainer = BSPPolygonIndicesContainer()

    def getVertices(self) -> BSPVertexContainer:
        return self.vertices

    def getPolygons(self) -> BSPPolygonsContainer:
        return self.polygons

    def getNodes(self) -> BSPNodesContainer:
        return self.nodes

    def getIndices(self) -> BSPPolygonIndicesContainer:
        return self.indices
