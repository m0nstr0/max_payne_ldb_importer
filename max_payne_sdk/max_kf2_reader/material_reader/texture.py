import max_payne_sdk.max_type as max_type
import max_payne_sdk.max_kf2_type as kf2_type
import max_payne_sdk.max_kf2_reader as kf2_reader


class TextureChunkReader(kf2_reader.KF2ReaderBase):
    def getAllowedVersions(self):
        return [1]

    def parse(self, f, kf2_chunk: kf2_type.KF2ChunkHeader):
        name = max_type.parseType(f)
        mip_maps_num = max_type.parseType(f)
        filtering_type = max_type.parseType(f)
        num_textures = max_type.parseType(f)
        textures = []
        for i in range(num_textures):
            textures.append(max_type.parseType(f))
        is_automatic_start = max_type.parseType(f) if num_textures > 1 else 0
        is_random_start_frame = max_type.parseType(f) if num_textures > 1 else 0
        start_frame = max_type.parseType(f) if num_textures > 1 else 0
        playback_fps = max_type.parseType(f) if num_textures > 1 else 0
        end_condition = max_type.parseType(f) if num_textures > 1 else 0
        animation_info = kf2_type.TextureAnimationInfo(is_automatic_start, is_random_start_frame, start_frame,
                                                       playback_fps, end_condition) if num_textures > 1 else None
        return kf2_type.Texture(kf2_chunk.version, name, mip_maps_num, filtering_type, textures, animation_info)
