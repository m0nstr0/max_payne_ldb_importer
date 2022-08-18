import max_payne_sdk.max_type as max_type
import max_payne_sdk.max_kf2_type as kf2_type
import max_payne_sdk.max_kf2_reader as kf2_reader
import max_payne_sdk.max_kf2_reader.animation_reader.animation as kf2_animation


class KeyframeAnimationChunkReader(kf2_reader.KF2ReaderBase):
    def getAllowedVersions(self):
        return [0, 1, 2, 3, 4, 5]

    def parse(self, f, kf2_chunk: kf2_type.KF2ChunkHeader):
        animation = kf2_animation.AnimationChunkReader().create(f, kf2_type.ANIMATION, self.readChunk(f))
        parent_name = max_type.parseType(f)
        use_loop_interpolation = max_type.parseType(f)
        num_total_keyframes = max_type.parseType(f)
        num_key_frames = max_type.parseType(f)
        keyframes = []
        for i in range(num_key_frames):
            keyframes.append(kf2_type.AnimationKeyframe(
                max_type.parseType(f),
                max_type.parseType(f)
            ))
        num_visibility_frames = max_type.parseType(f) if kf2_chunk.version > 0 else 0
        visibility_frames = []
        for i in range(num_visibility_frames):
            visibility_frames.append(kf2_type.AnimationVisibilityframe(
                max_type.parseType(f),
                max_type.parseType(f)
            ))
        loop_to_frame = max_type.parseType(f) if kf2_chunk.version > 1 else 0
        frame_to_frame_interpolation_method = max_type.parseType(f) if kf2_chunk.version > 2 else 0
        maintain_matrix_scaling = max_type.parseType(f) if kf2_chunk.version > 3 else False
        num_total_keyframes = num_total_keyframes + 1 if kf2_chunk.version < 5 else num_total_keyframes
        return kf2_type.KeyframeAnimation(
            kf2_chunk.version,
            animation,
            parent_name,
            use_loop_interpolation,
            num_total_keyframes,
            num_key_frames,
            keyframes,
            num_visibility_frames,
            visibility_frames,
            loop_to_frame,
            frame_to_frame_interpolation_method,
            maintain_matrix_scaling)
