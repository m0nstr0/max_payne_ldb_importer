import struct

from max_payne_sdk.lvl2.max_chunk import MaxChunk
from max_payne_sdk.lvl2.max_pack import packUInt, packInt, packString


class MaxTexture:
    def __init__(self) -> None:
        self.type = 5
        self.name = ""
        self.size = 0
        self.data = []

    # data have to be bytes array
    def fillFromMemory(self, type, name, data):
        self.type = type
        self.name = name
        self.data = data

    def getBytes(self) -> []:
        max_chunk = MaxChunk(0, 1)
        return max_chunk.getBytes([packUInt(self.type), packInt(self.size), packString(self.name), self.data])


