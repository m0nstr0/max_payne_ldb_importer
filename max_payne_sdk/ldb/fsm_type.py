from __future__ import annotations

from max_payne_sdk.ldb.entity_properties_type import EntityProperties


class FSMMessageContainer:
    def __init__(self) -> None:
        self.messages: list[str] = []

    def add(self, message: str):
        self.messages.append(message)


class FSMStateSpecificMessage:
    def __init__(self, state_name: str, messages: FSMMessageContainer) -> None:
        self.state_name: str = state_name
        self.messages: FSMMessageContainer = messages


class FSMStateSpecificMessageContainer:
    def __init__(self) -> None:
        self.messages: list[FSMStateSpecificMessage] = []

    def add(self, message: FSMStateSpecificMessage) -> None:
        self.messages.append(message)


class FSMEvent:
    def __init__(self, state_name: str, before: FSMMessageContainer, state_specific: FSMStateSpecificMessageContainer, after: FSMMessageContainer) -> None:
        self.state_name: str = state_name
        self.before: FSMMessageContainer = before
        self.state_specific: FSMStateSpecificMessageContainer = state_specific
        self.after : FSMMessageContainer = after


class FSMEventContainer:
    def __init__(self) -> None:
        self.events: list[FSMEvent] = []

    def add(self, event: FSMEvent) -> None:
        self.events.append(event)


class FSMStateContainer:
    def __init__(self) -> None:
        self.states: list[str] = []
        self.default: str = ""

    def setDefault(self, name: str):
        self.default = name

    def add(self, name: str):
        self.states.append(name)


class FSM:
    def __init__(self, shared_name: str, properties: EntityProperties, states: FSMStateContainer, startup_before: FSMMessageContainer, startup_after: FSMMessageContainer, state_switch: FSMEventContainer, string_specific: FSMEventContainer, entity_specific: FSMEventContainer) -> None:
        self.shared_name: str = shared_name
        self.properties: EntityProperties = properties
        self.states: FSMStateContainer = states
        self.startup_before: FSMMessageContainer = startup_before
        self.startup_after: FSMMessageContainer = startup_after
        self.state_switch: FSMEventContainer = state_switch
        self.string_specific: FSMEventContainer = string_specific
        self.entity_specific: FSMEventContainer = entity_specific


class FSMContainer:
    def __init__(self) -> None:
        self.fsms: list[FSM] = []

    def add(self, fsm: FSM):
        self.fsms.append(fsm)
