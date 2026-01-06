from max_payne_sdk.lvl2.max_chunk import MaxChunk
from max_payne_sdk.lvl2.max_node import MaxNode
from max_payne_sdk.lvl2.max_pack import packFloat, packString, packDouble


class MaxNodeDynamicPointLight(MaxNode):
    def __init__(self, id, name):
        super().__init__(id, name)
        self.node_type = 111
        self.radius = 0.5
        self.node_gameplay_critical = True
        #not used in pointlight
        self.shared_db_name = 'Pointlight'
        self.color = [255.0, 255.0, 255.0]
        self.intensity = 1.0
        self.falloff = 10.0

    def getChildData(self):
        data_ui = [packString(self.shared_db_name), packDouble(self.radius)]
        data_properties = [packFloat(self.color[0]),
                           packFloat(self.color[1]),
                           packFloat(self.color[2]),
                           packFloat(255.0),
                           packFloat(self.intensity),
                           packFloat(self.falloff),
                           ]

        max_chunk_ui = MaxChunk(0, 1)
        max_chunk_properties = MaxChunk(0, 3)
        return max_chunk_ui.getBytes(data_ui) + max_chunk_properties.getBytes(data_properties)

    def getBytes(self):
        self.calcAABBWithRadius()
        return super().getBytes()