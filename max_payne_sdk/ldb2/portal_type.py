from dataclasses import dataclass

from max_payne_sdk.ldb.vertex_type import Vertex


@dataclass
class Portal:
    name: str
    normal: Vertex
    unk1: int
    unk2: int
    points: [Vertex]


class PortalContainer:
    def __init__(self) -> None:
        self.portals: list[Portal] = []

    def __getitem__(self, key):
        return self.portals[key]

    def __setitem__(self, key, value):
        self.portals[key] = value

    def __len__(self):
        return len(self.portals)

    def add(self, portal: Portal):
        self.portals.append(portal)
