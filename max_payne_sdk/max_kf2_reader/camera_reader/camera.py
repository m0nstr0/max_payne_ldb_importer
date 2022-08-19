import max_payne_sdk.max_kf2_type as kf2_type
import max_payne_sdk.max_type as max_type
import max_payne_sdk.max_kf2_reader as kf2_reader
import max_payne_sdk.max_kf2_reader.node as kf2_node


class CameraChunkReader(kf2_reader.KF2ReaderBase):
    def getAllowedVersions(self):
        return [0]

    def parse(self, f, kf2_chunk: kf2_type.KF2ChunkHeader):
        kf2_chunk = self.readChunk(f)
        return kf2_type.Camera(
            kf2_chunk.version,
            kf2_node.NodeChunkReader().create(f, kf2_type.NODE, kf2_chunk),
            max_type.parseType(f),
            max_type.parseType(f),
            max_type.parseType(f))
