import max_payne_sdk.max_kf2_type as kf2_type
from io import BytesIO
import struct
from max_payne_sdk.binary import FormatError, read_exact


class KF2ReaderBase:
    def readChunk(self, f):
        chunk_tag = f.read(1)
        if not chunk_tag:
            return None
        if chunk_tag != kf2_type.CHUNK_HEADER_ID:
            raise FormatError("Unknown chunk tag id %s" % chunk_tag.hex())
        kf2_chunk = kf2_type.KF2ChunkHeader(*struct.unpack('<III', read_exact(f, 12)))
        if kf2_chunk.size < 13:
            raise FormatError("Chunk 0x%x has invalid size %d" % (kf2_chunk.id, kf2_chunk.size))
        return kf2_chunk

    def getAllowedVersions(self):
        return []

    def parse(self, f, kf2_chunk: kf2_type.KF2ChunkHeader):
        pass

    def create(self, f, chunk_id: int, kf2_chunk: kf2_type.KF2ChunkHeader):
        if kf2_chunk is None:
            raise FormatError("Missing chunk 0x%x" % chunk_id)
        if kf2_chunk.id != chunk_id:
            raise ValueError("Unknown chunk id %s" % hex(kf2_chunk.id))
        if kf2_chunk.version not in self.getAllowedVersions():
            raise ValueError("Unknown chunk version %i" % kf2_chunk.version)
        if kf2_chunk.size < 13:
            raise FormatError("Chunk size is smaller than its header")
        # Nested readers cannot consume a sibling or parent record.
        payload = BytesIO(read_exact(f, kf2_chunk.size - 13))
        result = self.parse(payload, kf2_chunk)
        if payload.tell() != kf2_chunk.size - 13:
            raise FormatError("Chunk 0x%x v%d has %d unread payload bytes" % (
                kf2_chunk.id, kf2_chunk.version,
                kf2_chunk.size - 13 - payload.tell()))
        return result
