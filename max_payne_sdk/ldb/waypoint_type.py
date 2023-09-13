from __future__ import annotations

from max_payne_sdk.ldb.entity_properties_type import EntityProperties


class Waypoint:
    def __init__(self, shared_name: str, object_properties: EntityProperties, type: int) -> None:
        self.shared_name: str = shared_name
        self.object_properties: EntityProperties = object_properties
        self.type: int = type #0 - waypoint 1 - startpoint


class WaypointContainer:
    def __init__(self) -> None:
        self.waypoints: list[Waypoint] = []

    def add(self, waypoint: Waypoint):
        self.waypoints.append(waypoint)
