from __future__ import annotations


class Room:
    def __init__(self, id: int, name: str, static_meshes: list[int], dynamic_lights: list[str], exits: list[str], start_points: list[str], fsms: list[str], characters: list[str], triggers: list[str], dynamic_meshes: list[str], level_items: list[str], point_lights: list[int]) -> None:
        self.id: int = id
        self.name: str = name
        self.static_meshes: list[int] = static_meshes
        self.dynamic_lights: list[str] = dynamic_lights
        self.exits: list[str] = exits
        self.start_points: list[str] = start_points
        self.fsms: list[str] = fsms
        self.characters: list[str] = characters
        self.triggers: list[str] = triggers
        self.dynamic_meshes: list[str] = dynamic_meshes
        self.level_items: list[str] = level_items
        self.point_lights: list[int] = point_lights


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
