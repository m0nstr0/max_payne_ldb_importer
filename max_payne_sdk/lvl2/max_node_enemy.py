from max_payne_sdk.lvl2.max_chunk import MaxChunk
from max_payne_sdk.lvl2.max_fsm_script import MaxFSMScript, MaxFSMEvent
from max_payne_sdk.lvl2.max_node import MaxNode
from max_payne_sdk.lvl2.max_pack import packDouble, packString, packBool


class MaxNodeEnemy(MaxNode):
    def __init__(self, id, name):
        super().__init__(id, name)
        self.node_type = 110
        self.radius = 0.05
        self.node_gameplay_critical = True
        self.enemy_skin = ''
        self.enemy_group = ''
        self.activator_use_animation = ''
        self.has_fsm = True
        self.fsm = MaxFSMScript()
        self.fsm.events = [MaxFSMEvent('OnActivate'),
                           MaxFSMEvent('OnDeath'),
                           MaxFSMEvent('OnLowHealth'),
                           MaxFSMEvent('OnPlayerAttack'),
                           MaxFSMEvent('OnUse'),
                           MaxFSMEvent('Startup')]
    def getChildData(self):
        data_common = [packString(self.enemy_skin), packDouble(self.radius)]
        data_additional = [packString(self.enemy_group), packString(self.activator_use_animation)]

        max_chunk_common = MaxChunk(0, 1)
        max_chunk_additional = MaxChunk(0, 2)

        return max_chunk_common.getBytes(data_common) + max_chunk_additional.getBytes(data_additional)

    def getBytes(self):
        self.calcAABBWithRadius()
        return super().getBytes()