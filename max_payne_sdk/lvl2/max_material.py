from max_payne_sdk.lvl2.max_chunk import MaxChunk
from max_payne_sdk.lvl2.max_pack import packString, packUInt, packInt, packDouble, packBool


class MaxMaterial:
    def __init__(self) -> None:
        self.material_name = ''
        self.num_frames = 1
        self.diffuse_textures = []
        self.light_layer_texture = ''
        self.detail_texture = ''
        self.diffuse_default_width = 2.0
        self.diffuse_default_height = 2.0
        self.light_layer_default_width = 1.0
        self.light_layer_default_height = 1.0
        self.detail_texture_default_scale = 1.0
        self.dual_sided = False
        self.alpha_reference_value = 240
        self.adult_content = False
        # 3 - Additive, 4 - With Detail Texture, 0 - Normal, 1 - Alpha Compare, 2 - Alpha Blend
        self.mode = 0
        self.alpha_compare_edge_blend = 0
        self.has_reflection_texture = 0
        self.has_gloss_texture = 0
        self.reflection_texture = ''
        self.gloss_texture = ''
        self.active_frame = 0
        self.framerate = 1

    def getBytes(self):
        data = [packString(self.material_name), packUInt(self.num_frames)]
        for i in self.diffuse_textures:
            data.append(packString(i))
        data = data + [packString(self.light_layer_texture),
                       packString(self.detail_texture),
                       packDouble(self.diffuse_default_width),
                       packDouble(self.diffuse_default_height),
                       packDouble(self.light_layer_default_width),
                       packDouble(self.light_layer_default_height),
                       packDouble(self.detail_texture_default_scale),
                       packBool(self.dual_sided),
                       packUInt(self.alpha_reference_value),
                       packBool(self.adult_content),
                       packInt(self.mode),
                       packBool(self.alpha_compare_edge_blend),
                       packBool(self.has_reflection_texture),
                       packBool(self.has_gloss_texture),
                       packString(self.reflection_texture),
                       packString(self.gloss_texture),
                       packInt(self.active_frame),
                       packInt(self.framerate)]
        max_chunk = MaxChunk(0, 5)
        return max_chunk.getBytes(data)
