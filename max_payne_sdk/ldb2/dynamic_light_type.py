from dataclasses import dataclass


@dataclass
class DynamicLightColor:
    R: float
    G: float
    B: float
    A: float


@dataclass
class DynamicLight:
    transform: []
    room_id: int
    color: DynamicLightColor
    Falloff: float


class DynamicLightContainer:
    def __init__(self) -> None:
        self.dynamic_lights: list[DynamicLight] = []

    def __getitem__(self, key):
        return self.dynamic_lights[key]

    def __setitem__(self, key, value):
        self.dynamic_lights[key] = value

    def __len__(self):
        return len(self.dynamic_lights)

    def add(self, dynamic_light: DynamicLight):
        self.dynamic_lights.append(dynamic_light)
