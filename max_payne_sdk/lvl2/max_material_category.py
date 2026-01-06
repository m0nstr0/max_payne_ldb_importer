from max_payne_sdk.lvl2.max_chunk import MaxChunk
from max_payne_sdk.lvl2.max_pack import packUInt, packString


class MaxMaterialCategory:
    def __init__(self):
        self.category_name = ''
        self.materials = []

    def getBytes(self):
        chunk_data = [packUInt(len(self.materials)),
                      packString(self.category_name)]

        data = []
        for i in self.materials:
            data = data + i.getBytes()

        max_chunk = MaxChunk(0, 1)
        return max_chunk.getBytes(chunk_data) + data
