from __future__ import annotations

from max_payne_sdk.ldb.entity_properties_type import EntityProperties


class PointLight:
    def __init__(self, id: int, object_properties: EntityProperties, r: float, g: float, b: float, a: float, falloff: float, intensity: float) -> None:
        self.id: int = id
        self.object_properties: EntityProperties = object_properties
        self.r: str = r
        self.g: str = g
        self.b: str = b
        self.a: str = a
        self.falloff: str = falloff
        self.intensity: str = intensity


class PointLightContainer:
    def __init__(self) -> None:
        self.pointlights: list[PointLight] = []

    def add(self, pointlight: PointLight):
        self.pointlights.append(pointlight)
