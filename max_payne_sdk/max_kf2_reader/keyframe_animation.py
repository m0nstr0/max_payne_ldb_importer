import max_payne_sdk.max_type as max_type
import max_payne_sdk.max_kf2_type as kf2_type
import max_payne_sdk.max_kf2_reader as kf2_reader
import max_payne_sdk.max_kf2_reader.animation as kf2_animation

class KeyframeAnimationChunkReaderV5(kf2_reader.KF2ReaderBase):
    def parse(self, f):
        kf2_chunk = self.readChunk(f)
        if kf2_chunk.id != kf2_type.ANIMATION:
            raise ValueError("Unknown chunk id %s" % kf2_chunk.id.hex())
        if kf2_chunk.version != 0:
            raise ValueError("Unknown animation chunk version %i" % kf2_chunk.version)
        animation = kf2_animation.AnimationChunkReaderV0().parse(f)
        parent_name = max_type.parseType(f)
        use_loop_interpolation = max_type.parseType(f)
        num_total_keyframes = max_type.parseType(f)
        num_key_frames = max_type.parseType(f)
        keyframes = list[kf2_type.AnimationKeyframe] = []
        for i in range(num_key_frames):
            frame_id = max_type.parseType(f)
            transform = max_type.parseType(f)
            keyframes.append(kf2_type.AnimationKeyframe(frame_id, transform))
        num_visibility_frames = max_type.parseType(f)
        visibility_frames = list[kf2_type.AnimationVisibilityframe]
        for i in range(num_visibility_frames):
            frame_id = max_type.parseType(f)
            visibility = max_type.parseType(f)
            visibility_frames.append(kf2_type.AnimationVisibilityframe(frame_id, visibility))
        loop_to_frame = max_type.parseType(f)
        frame_to_frame_interpolation_method = max_type.parseType(f)
        maintain_matrix_scaling = max_type.parseType(f)
        return kf2_type.KeyframeAnimationV5(5, animation, parent_name, use_loop_interpolation, num_total_keyframes, num_key_frames, keyframes, num_visibility_frames, visibility_frames, loop_to_frame, frame_to_frame_interpolation_method, maintain_matrix_scaling)

class KeyframeAnimationChunkReader:
    def create(self, kf2_chunk: kf2_type.KF2ChunkHeader):
        if (kf2_chunk.id != kf2_type.KEYFRAME_ANIMATION):
            raise ValueError("Unknown chunk id %s" % kf2_chunk.id.hex())
        if (kf2_chunk.version == 5):
            return KeyframeAnimationChunkReaderV5()
        raise ValueError("Unknown keyframe animation chunk version %i" % kf2_chunk.version)