import max_payne_sdk.max_type as max_type
import max_payne_sdk.max_kf2_type as kf2_type

class AnimationChunkReaderV0:
    def parse(self, f):
        object_name = max_type.parseType(f)
        fps = max_type.parseType(f)
        is_looping = max_type.parseType(f)
        return kf2_type.AnimationV0(0, object_name, fps, is_looping)