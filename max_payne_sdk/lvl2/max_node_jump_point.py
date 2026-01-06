from max_payne_sdk.lvl2.max_node import MaxNode


class MaxNodeJumpPoint(MaxNode):
    def __init__(self, id, name):
        super().__init__(id, name)
        self.node_type = 108
        self.radius = 0.5
        self.node_gameplay_critical = True

    def getChildData(self):
        return []

    def getBytes(self):
        self.calcAABBWithRadius()
        return super().getBytes()