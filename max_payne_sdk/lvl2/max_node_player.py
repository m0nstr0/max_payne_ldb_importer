from max_payne_sdk.lvl2.max_chunk import MaxChunk
from max_payne_sdk.lvl2.max_fsm_script import MaxFSMScript, MaxFSMEvent
from max_payne_sdk.lvl2.max_node import MaxNode
from max_payne_sdk.lvl2.max_pack import packString


class MaxNodePlayer(MaxNode):
    def __init__(self, id, name):
        super().__init__(id, name)
        self.node_type = 116
        self.has_fsm = True
        self.fsm = MaxFSMScript()
        self.fsm.events = [MaxFSMEvent('OnActivate'),
                           MaxFSMEvent('OnDeath'),
                           MaxFSMEvent('OnLowHealth'),
                           MaxFSMEvent('Startup')]

    def getChildData(self):
        data = [packString('PLAYER_GROUP')]

        max_chunk = MaxChunk(0, 1)
        return max_chunk.getBytes(data)