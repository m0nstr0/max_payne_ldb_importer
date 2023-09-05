from dataclasses import dataclass


@dataclass
class CharacterEnemyGroup:
    name: str
    id: int


@dataclass
class Character:
    entity_name: str
    character_name: str
    transform: []
    room_id: int
    enemy_group_id: int
    activator_use_animation: str


class CharacterEnemyGroupContainer:
    def __init__(self) -> None:
        self.enemy_groups: list[CharacterEnemyGroup] = []

    def __getitem__(self, key):
        return self.enemy_groups[key]

    def __setitem__(self, key, value):
        self.enemy_groups[key] = value

    def __len__(self):
        return len(self.enemy_groups)

    def add(self, enemy_group: CharacterEnemyGroup):
        self.enemy_groups.append(enemy_group)


class CharacterContainer:
    def __init__(self) -> None:
        self.characters: list[Character] = []

    def __getitem__(self, key):
        return self.characters[key]

    def __setitem__(self, key, value):
        self.characters[key] = value

    def __len__(self):
        return len(self.characters)

    def add(self, character: Character):
        self.characters.append(character)
