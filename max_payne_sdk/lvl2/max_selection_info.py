import struct

from max_payne_sdk.lvl2.max_chunk import MaxChunk
from max_payne_sdk.lvl2.max_pack import packUChar, packInt, packUInt


class MaxSelectionInfo:
    def __init__(self):
        self.version = 2
        self.has_selection = 0
        self.auto_select_children = 1
        self.selected_nodes = []

    def getBytes(self):
        data = [packUChar(self.has_selection)]
        if self.has_selection == 1:
            data.append(struct.pack('<c', b'\x1C'))
            data.append(packInt(len(self.selected_nodes)))
            for i in self.selected_nodes:
                data.append(packUInt(i))
        data.append(packUChar(self.auto_select_children))

        max_chunk = MaxChunk(0, 1)
        return [packUChar(self.version)] + max_chunk.getBytes(data)