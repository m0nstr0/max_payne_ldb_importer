from __future__ import annotations

from max_payne_sdk.ldb.entity_properties_type import EntityProperties


class Item:
    def __init__(self, shared_name: str, object_properties: EntityProperties, item_name: str) -> None:
        self.shared_name: str = shared_name
        self.object_properties: EntityProperties = object_properties
        self.item_name: str = item_name


class ItemContainer:
    def __init__(self) -> None:
        self.items: list[Item] = []

    def add(self, item: Item):
        self.items.append(item)
