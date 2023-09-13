from dataclasses import dataclass


@dataclass
class Flare:
    flare_name: str
    transform: []
    room_id: int


class FlareContainer:
    def __init__(self) -> None:
        self.flares: list[Flare] = []

    def __getitem__(self, key):
        return self.flares[key]

    def __setitem__(self, key, value):
        self.flares[key] = value

    def __len__(self):
        return len(self.flares)

    def add(self, flare: Flare):
        self.flares.append(flare)
