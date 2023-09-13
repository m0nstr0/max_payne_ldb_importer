from dataclasses import dataclass

from max_payne_sdk.ldb2.aabb_type import AABB
from max_payne_sdk.ldb2.collision_shape_type import CollisionShape
from max_payne_sdk.ldb2.static_mesh_type import StaticMeshContainer
from max_payne_sdk.ldb2.volume_light_type import VolumeLight


@dataclass
class Room:
    name: str
    transform: []
    aabb: AABB
    static_mesh: StaticMeshContainer
    collisions: [CollisionShape]
    volume_lights: [VolumeLight]
    dynamic_meshes = []


class RoomContainer:
    def __init__(self) -> None:
        self.rooms: list[Room] = []

    def __getitem__(self, key):
        return self.rooms[key]

    def __setitem__(self, key, value):
        self.rooms[key] = value

    def __len__(self):
        return len(self.rooms)

    def add(self, room: Room):
        self.rooms.append(room)
