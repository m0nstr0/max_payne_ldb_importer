from max_payne_sdk.lvl2.max_chunk import MaxChunk
from max_payne_sdk.lvl2.max_node import MaxNode
from max_payne_sdk.lvl2.max_pack import packDouble, packString


class MaxNodeFlare(MaxNode):
    def __init__(self, id, name):
        super().__init__(id, name)
        self.node_type = 119
        self.radius = 0.25
        self.node_gameplay_critical = True
        self.flare_name = ''

    def getChildData(self):
        data = [packString(self.flare_name), packDouble(self.radius)]
        max_chunk = MaxChunk(0, 1)
        return max_chunk.getBytes(data) + max_chunk.getBytes([])

    def getBytes(self):
        self.calcAABBWithRadius()
        return super().getBytes()