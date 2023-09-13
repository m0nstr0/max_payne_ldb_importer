from dataclasses import dataclass


@dataclass
class JumpPoint:
    name: str
    transform: []
    room_id: int


class JumpPointContainer:
    def __init__(self) -> None:
        self.jump_points: list[JumpPoint] = []

    def __getitem__(self, key):
        return self.jump_points[key]

    def __setitem__(self, key, value):
        self.jump_points[key] = value

    def __len__(self):
        return len(self.jump_points)

    def add(self, jump_point: JumpPoint):
        self.jump_points.append(jump_point)
