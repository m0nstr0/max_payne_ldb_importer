from dataclasses import dataclass


@dataclass
class WayPoint:
    name: str
    transform: []
    room_id: int
    unk: int


class WayPointContainer:
    def __init__(self) -> None:
        self.way_points: list[WayPoint] = []

    def __getitem__(self, key):
        return self.way_points[key]

    def __setitem__(self, key, value):
        self.way_points[key] = value

    def __len__(self):
        return len(self.way_points)

    def add(self, way_point: WayPoint):
        self.way_points.append(way_point)