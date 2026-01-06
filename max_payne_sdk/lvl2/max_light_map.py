import struct

from max_payne_sdk.lvl2.max_chunk import MaxChunk
from max_payne_sdk.lvl2.max_pack import packULong, packUInt


class MaxLightMap:
    def __init__(self):
        self.id = 0
        self.width = 0
        self.height = 0
        self.pass_through = False
        self.data = []

    def getBytes(self):
        data = [packUInt(self.width), packUInt(self.height)]
        for i in self.data:
            data.append(struct.pack('<f', i))

        max_chunk = MaxChunk(0, 2)
        return [packULong(self.id)] + max_chunk.getBytes(data)
