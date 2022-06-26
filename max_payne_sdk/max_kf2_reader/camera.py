import max_payne_sdk.max_kf2_type as kf2_type
import max_payne_sdk.max_type as max_type
import max_payne_sdk.max_kf2_reader as kf2_reader
import max_payne_sdk.max_kf2_reader.node as kf2_node

class CameraChunkReaderV0(kf2_reader.KF2ReaderBase):
    def parse(self, f):
        kf2_chunk = self.readChunk(f)
        if kf2_chunk.id != kf2_type.NODE:
            raise ValueError("Unknown chunk id %s" % kf2_chunk.id.hex())
        if kf2_chunk.version != 1:
            raise ValueError("Unknown node chunk version %i" % kf2_chunk.version)
        node = kf2_node.NodeChunkReaderV1().parse(f)
        fov = max_type.parseType(f)
        front_plane = max_type.parseType(f)
        back_plane = max_type.parseType(f)
        return kf2_type.CameraV0(0, node, fov, front_plane, back_plane)

class CameraChunkReader:
    def create(self, kf2_chunk: kf2_type.KF2ChunkHeader):
        if (kf2_chunk.id != kf2_type.CAMERA):
            raise ValueError("Unknown chunk id %s" % kf2_chunk.id.hex())
        if (kf2_chunk.version == 0):
            return CameraChunkReaderV0()
        raise ValueError("Unknown camera chunk version %i" % kf2_chunk.version)