from max_payne_sdk.lvl2.max_chunk import MaxChunk
from max_payne_sdk.lvl2.max_fsm_script import MaxFSMScript, MaxFSMEvent
from max_payne_sdk.lvl2.max_node import MaxNode
from max_payne_sdk.lvl2.max_pack import packDouble, packString, packBool


class MaxNodeLevelItem(MaxNode):
    def __init__(self, id, name):
        super().__init__(id, name)
        self.node_type = 109
        self.radius = 0.05
        self.node_gameplay_critical = True
        self.item_type = ''

    def getChildData(self):
        data = [packString(self.item_type), packDouble(self.radius)]
        max_chunk = MaxChunk(0, 1)
        return max_chunk.getBytes(data)

    def getBytes(self):
        self.calcAABBWithRadius()
        return super().getBytes()