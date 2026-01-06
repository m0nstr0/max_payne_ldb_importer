from max_payne_sdk.lvl2.max_chunk import MaxChunk
from max_payne_sdk.lvl2.max_pack import packUInt


class MaxTexturesAndMaterials:
    def __init__(self):
        self.textures = []
        self.categories = []

    def getBytes(self):
        tex_data = [packUInt(len(self.textures))]
        for i in self.textures:
            tex_data = tex_data + i.getBytes()

        data = [packUInt(len(self.categories))]
        for i in self.categories:
            data = data + i.getBytes()

        max_chunk = MaxChunk(0, 1)
        return max_chunk.getBytes(tex_data) + data