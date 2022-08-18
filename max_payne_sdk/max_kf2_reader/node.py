import max_payne_sdk.max_kf2_type as kf2_type
import max_payne_sdk.max_type as max_type
import max_payne_sdk.max_kf2_reader as kf2_reader


class NodeChunkReader(kf2_reader.KF2ReaderBase):
    def getAllowedVersions(self):
        return [0, 1]

    def parse(self, f, kf2_chunk: kf2_type.KF2ChunkHeader):
        return kf2_type.Node(
            kf2_chunk.version,
            max_type.parseType(f),
            max_type.parseType(f),
            max_type.parseType(f),
            max_type.parseType(f),
            max_type.parseType(f) if kf2_chunk.version > 0 else "")
