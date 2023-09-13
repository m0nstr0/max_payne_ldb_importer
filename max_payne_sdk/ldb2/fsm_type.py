from dataclasses import dataclass


@dataclass
class FSMCode:
    event_name: str
    on_before: [str]
    on_after: [str]


@dataclass
class FSMState:
    id: int
    messages: [str]


@dataclass
class FSMCode2:
    on_before: [str]
    on_after: [str]
    states: [FSMState]


@dataclass
class FSMCode3:
    pass


@dataclass
class FSMCustomState:
    name: str


@dataclass
class FSMTimer:
    pass


@dataclass
class FSM:
    name: str
    transform: []
    parent: int
    local_transform: []
    room_id: int
    # default_state: str
    # custom_states: [FSMCustomState]
    # on_startup: [FSMCode2]
    # on_custom_event: [FSMCode3]
    # on_state: [FSMCode3]
    # on_entity_event: [FSMCode3]
    # timer: [FSMTimer]


class FSMContainer:
    def __init__(self) -> None:
        self.fsms: list[FSM] = []

    def __getitem__(self, key):
        return self.fsms[key]

    def __setitem__(self, key, value):
        self.fsms[key] = value

    def __len__(self):
        return len(self.flares)

    def add(self, fsm: FSM):
        self.fsms.append(fsm)
