from __future__ import annotations

from max_payne_sdk.ldb.entity_properties_type import EntityProperties


class DynamicLight:
    def __init__(self, shared_name: str, object_properties: EntityProperties, transform, unk1: float, unk2: float, unk3: float, unk4: float, unk5: float, unk6: float, unk7: float, unk8: float, unk9: float, unk10: float) -> None:
        self.shared_name: str = shared_name
        self.object_properties: EntityProperties = object_properties
        self.transform = transform
        self.unk1: float = unk1
        self.unk2: float = unk2
        self.unk3: float = unk3
        self.unk4: float = unk4
        self.unk5: float = unk5
        self.unk6: float = unk6
        self.unk7: float = unk7
        self.unk8: float = unk8
        self.unk9: float = unk9
        self.unk10: float = unk10


class DynamicLightContainer:
    def __init__(self) -> None:
        self.lights: list[DynamicLight] = []

    def add(self, light: DynamicLight):
        self.lights.append(light)
