from max_payne_sdk.lvl2.max_chunk import MaxChunk
from max_payne_sdk.lvl2.max_pack import packInt, packFloat


class MaxLightMaps:
    def __init__(self):
        self.light_maps = []
        self.curve_middle_gray = 128.0
        self.curve_output_minimum = 0.0
        self.curve_output_maximum = 255.0
        self.equalization_percent = 0.0

    def getBytes(self):
        light_maps_chunk = MaxChunk(0, 1)
        map_data = [packInt(len(self.light_maps))]
        for i in self.light_maps:
            map_data = map_data + i.getBytes()

        curve_chunk = MaxChunk(0, 1)
        curve_data = [packFloat(self.curve_middle_gray),
                      packFloat(self.curve_output_minimum),
                      packFloat(self.curve_output_maximum),
                      packFloat(self.equalization_percent)]

        return light_maps_chunk.getBytes(map_data + curve_chunk.getBytes(curve_data))

