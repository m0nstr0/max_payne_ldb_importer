import max_payne_sdk.max_kf2_type as kf2_type
import max_payne_sdk.max_type as max_type
import max_payne_sdk.max_kf2_reader as kf2_reader


class SmoothingChunkReader(kf2_reader.KF2ReaderBase):
    def getAllowedVersions(self):
        return [0]

    def parse(self, f, kf2_chunk: kf2_type.KF2ChunkHeader):
        num_groups = max_type.parseType(f)
        smoothing_groups = []
        for i in range(num_groups):
            smoothing_groups.append(max_type.parseType(f))
        return kf2_type.Smoothing(kf2_chunk.version, smoothing_groups)