from __future__ import annotations


class EntityProperties:
    def __init__(self, name: str, object_to_room_transform, object_to_parent_transform, room_id : int, parent_dynamic_mesh_name: str) -> None:
        self.name: str = name
        self.object_to_room_transform = object_to_room_transform
        self.object_to_parent_transform = object_to_parent_transform
        self.room_id : int = room_id
        self.parent_dynamic_mesh_name: str = parent_dynamic_mesh_name
