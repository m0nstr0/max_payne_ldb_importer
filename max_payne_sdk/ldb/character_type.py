from __future__ import annotations

from max_payne_sdk.ldb.entity_properties_type import EntityProperties
from max_payne_sdk.ldb.fsm_type import FSMMessageContainer


class Character:
    def __init__(self, shared_name: str, properties: EntityProperties, character_name: str, startup_before: FSMMessageContainer, on_death_before: FSMMessageContainer, on_activate_before: FSMMessageContainer, on_special_before: FSMMessageContainer) -> None:
        self.shared_name: str = shared_name
        self.properties: EntityProperties = properties
        self.character_name: str = character_name
        self.startup_before: FSMMessageContainer = startup_before
        self.on_death_before: FSMMessageContainer = on_death_before
        self.on_activate_before: FSMMessageContainer = on_activate_before
        self.on_special_before: FSMMessageContainer = on_special_before


class CharacterContainer:
    def __init__(self) -> None:
        self.characters: list[Character] = []

    def add(self, character: Character):
        self.characters.append(character)
