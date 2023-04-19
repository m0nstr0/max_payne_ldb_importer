import max_payne_sdk.max_type as max_type
import max_payne_sdk.max_kf2_type as kf2_type
import max_payne_sdk.max_kf2_reader as kf2_reader


class AnimationChunkReader(kf2_reader.KF2ReaderBase):
    def getAllowedVersions(self):
        return [0]

    def parse(self, f, kf2_chunk: kf2_type.KF2ChunkHeader):
        return kf2_type.Animation(
            kf2_chunk.version,
            max_type.parseType(f),
            max_type.parseType(f),
            max_type.parseType(f))