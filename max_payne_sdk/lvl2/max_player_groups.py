from max_payne_sdk.lvl2.max_chunk import MaxChunk
from max_payne_sdk.lvl2.max_pack import packUInt, packString


class MaxPlayerGroups:
    def __init__(self):
        self.player_groups = ['', 'PLAYER_GROUP']

    def getBytes(self):
        data = [packUInt(len(self.player_groups))]
        for i in self.player_groups:
            data.append(packString(i))

        max_chunk = MaxChunk(0, 1)
        return max_chunk.getBytes(data)
