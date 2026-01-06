from max_payne_sdk.lvl2.max_chunk import MaxChunk
from max_payne_sdk.lvl2.max_fsm_script import MaxFSMScript, MaxFSMEvent
from max_payne_sdk.lvl2.max_node import MaxNode
from max_payne_sdk.lvl2.max_pack import packDouble, packString, packBool


class MaxNodeTrigger(MaxNode):
    def __init__(self, id, name):
        super().__init__(id, name)
        self.node_type = 106
        self.radius = 0.5
        self.node_gameplay_critical = True
        self.has_fsm = True
        self.fsm = MaxFSMScript()
        self.fsm.events = [MaxFSMEvent('Startup'),
                           MaxFSMEvent('T_Activate')
                           ]
        #not used in trigger
        self.shared_db_name = ''
        self.activator_player = False
        self.activator_use = False
        self.activator_enemy = False
        self.activator_bullet = False
        self.activator_look_at = False
        self.activator_visibility = False
        self.activator_use_animation = ''

    def getChildData(self):
        data_common = [packString(self.shared_db_name), packDouble(self.radius)]
        data_activator = [packBool(self.activator_player),
                           packBool(self.activator_use),
                           packBool(self.activator_enemy),
                           packBool(self.activator_bullet),
                           packBool(self.activator_look_at),
                           packBool(self.activator_visibility),
                           packString(self.activator_use_animation)
                           ]

        max_chunk_common = MaxChunk(0, 1)
        max_chunk_activator = MaxChunk(0, 3)
        return max_chunk_common.getBytes(data_common) + max_chunk_activator.getBytes(data_activator)

    def getBytes(self):
        self.calcAABBWithRadius()
        return super().getBytes()