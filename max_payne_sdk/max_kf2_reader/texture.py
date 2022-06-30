import max_payne_sdk.max_type as max_type
import max_payne_sdk.max_kf2_type as kf2_type

class TextureChunkReaderV1:
    def parse(self, f):
        name = max_type.parseType(f)
        mip_maps_num = max_type.parseType(f)
        filtering_type = max_type.parseType(f)
        num_textures = max_type.parseType(f)
        textures = []
        for i in range(num_textures):
            textures.append(max_type.parseType(f))
        if num_textures > 1:
            is_automatic_start = max_type.parseType(f)
            is_random_start_frame = max_type.parseType(f)
            start_frame = max_type.parseType(f)
            playback_fps = max_type.parseType(f)
            end_condition = max_type.parseType(f)
        animation_info = kf2_type.TextureAnimationInfo(is_automatic_start, is_random_start_frame, start_frame, playback_fps, end_condition)
        return kf2_type.TextureV1(1, name, mip_maps_num, filtering_type, textures, animation_info)