from max_payne_sdk.lvl2.max_node import MaxNode


class MaxNodeWayPoint(MaxNode):
    def __init__(self, id, name):
        super().__init__(id, name)
        self.node_type = 107

    def getChildData(self):
        return []

    def getBytes(self):
        self.calcAABBWithRadius()
        return super().getBytes()