from __future__ import annotations

from max_payne_sdk.ldb.vertex_type import VertexContainer, Vertex


class Exit:
    def __init__(self, exit_name: str, vertices: VertexContainer, normal: Vertex, transform, room_id: int, parent_room_id: int, parent_room_name: str) -> None:
        self.exit_name = exit_name
        self.vertices: VertexContainer = vertices
        self.normal: Vertex = normal
        self.transform = transform
        self.room_id: int = room_id
        self.parent_room_id: int = parent_room_id
        self.parent_room_name: str = parent_room_name


class ExitContainer:
    def __init__(self) -> None:
        self.exits: list[Exit] = []

    def add(self, exit: Exit) -> None:
        self.exits.append(exit)
