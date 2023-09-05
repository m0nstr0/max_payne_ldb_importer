from dataclasses import dataclass


@dataclass
class LevelItem:
    entity_name: str
    item_name: str
    transform: []
    room_id: int


class LevelItemContainer:
    def __init__(self) -> None:
        self.level_items: list[LevelItem] = []

    def __getitem__(self, key):
        return self.level_items[key]

    def __setitem__(self, key, value):
        self.level_items[key] = value

    def __len__(self):
        return len(self.level_items)

    def add(self, flare: LevelItem):
        self.level_items.append(flare)
