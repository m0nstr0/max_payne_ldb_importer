import max_payne_sdk.max_kf2_type as kf2_type
import max_payne_sdk.max_type as max_type

class SkinChunkReaderV1:
    def parse(self, f):
        pass

class SkinChunkReader:
    def create(self, kf2_chunk: kf2_type.KF2ChunkHeader):
        if (kf2_chunk.id != kf2_type.SKIN):
            raise ValueError("Unknown chunk id %s" % kf2_chunk.id.hex())
        if (kf2_chunk.version == 1):
            return SkinChunkReaderV1()
        raise ValueError("Unknown skin chunk version %i" % kf2_chunk.version)
