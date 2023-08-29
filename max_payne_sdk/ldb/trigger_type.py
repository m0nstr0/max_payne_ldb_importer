from __future__ import annotations

from max_payne_sdk.ldb.entity_properties_type import EntityProperties


class Trigger:
    def __init__(self, shared_name: str, properties: EntityProperties, radius: float, type: int) -> None:
        self.shared_name: str = shared_name
        self.properties: EntityProperties = properties
        self.radius: float = radius
        self.type: int = type


class TriggerContainer:
    def __init__(self) -> None:
        self.triggers: list[Trigger] = []

    def add(self, trigger: Trigger):
        self.triggers.append(trigger)
