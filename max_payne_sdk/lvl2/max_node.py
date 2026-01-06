from max_payne_sdk.lvl2.max_chunk import MaxChunk
from max_payne_sdk.lvl2.max_fsm_script import MaxFSMScript
from max_payne_sdk.lvl2.max_pack import packInt, packULong, packDouble, packBool, packString, packUInt


class MaxNode:
    def __init__(self):
        self.node_type = 103
        self.node_id = 0
        self.node_translate = [0.0, 0.0, 0.0]
        self.node_matrix33 = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
        self.aabb_min = [0.0, 0.0, 0.0]
        self.aabb_max = [0.0, 0.0, 0.0]
        self.radius = 0.0
        self.node_is_visible = True
        self.node_exclude_from_game = False
        self.node_exclude_from_lighting = False
        self.node_enable_export_regrouping = False
        self.node_gameplay_critical = True
        self.node_name = ''
        self.has_fsm = False
        self.children = []
        self.fsm = MaxFSMScript()
        self.node_data = []

    def getChildData(self):
        return []

    def getBytes(self):
        data = [packULong(self.node_id),
                packDouble(self.node_translate[0]),
                packDouble(self.node_translate[1]),
                packDouble(self.node_translate[2]),
                packDouble(self.node_matrix33[0][0]),
                packDouble(self.node_matrix33[0][1]),
                packDouble(self.node_matrix33[0][2]),
                packDouble(self.node_matrix33[1][0]),
                packDouble(self.node_matrix33[1][1]),
                packDouble(self.node_matrix33[1][2]),
                packDouble(self.node_matrix33[2][0]),
                packDouble(self.node_matrix33[2][1]),
                packDouble(self.node_matrix33[2][2]),
                packDouble(self.aabb_min[0]),
                packDouble(self.aabb_min[1]),
                packDouble(self.aabb_min[2]),
                packDouble(self.aabb_max[0]),
                packDouble(self.aabb_max[1]),
                packDouble(self.aabb_max[2]),
                packDouble(self.radius),
                packBool(self.node_is_visible),
                packBool(self.node_exclude_from_game),
                packBool(self.node_exclude_from_lighting),
                packBool(self.node_enable_export_regrouping),
                packBool(self.node_gameplay_critical),
                packString(self.node_name),
                packBool(self.has_fsm)
                ]

        if self.has_fsm:
            data = data + self.fsm.getBytes()

        max_chunk = MaxChunk(0, 4)
        data = [packInt(self.node_type)] + max_chunk.getBytes(data) + self.getChildData() + [packUInt(len(self.children))]

        for i in self.children:
            data = data + i.getBytes()

        return data

