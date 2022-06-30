import max_payne_sdk.max_kf2_type as kf2_type
import max_payne_sdk.max_type as max_type

class EnvironmentChunkReaderV0:
    def parse(self, f):
        return kf2_type.EnvironmentV0(
            0,
            max_type.parseType(f),
            max_type.parseType(f),
            max_type.parseType(f),
            max_type.parseType(f),
            max_type.parseType(f),
            max_type.parseType(f),
            max_type.parseType(f),
            max_type.parseType(f))

class EnvironmentChunkReader:
    def create(self, kf2_chunk: kf2_type.KF2ChunkHeader):
        if (kf2_chunk.id != kf2_type.ENVIRONMENT):
            raise ValueError("Unknown chunk id %s" % kf2_chunk.id.hex())
        if (kf2_chunk.version == 0):
            return EnvironmentChunkReaderV0()
        raise ValueError("Unknown environment chunk version %i" % kf2_chunk.version)