from max_payne_sdk.lvl2.max_node import MaxNode
from max_payne_sdk.lvl2.max_node_player import MaxNodePlayer


class MaxNodeWorldGroup(MaxNode):
    def __init__(self):
        super().__init__()
        self.node_type = 103
        self.node_name = 'World_Group'
        self.children = [] # [MaxNodePlayer()]

    def getChildData(self):
        return []
