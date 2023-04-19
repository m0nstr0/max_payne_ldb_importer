import max_payne_sdk.max_kf2_type as kf2_type


class KF2ReaderBase:
    def readChunk(self, f):
        chunk_tag = f.read(1)
        if not chunk_tag:
            return None
        if chunk_tag != kf2_type.CHUNK_HEADER_ID:
            raise ValueError("Unknown chunk tag id %s" % chunk_tag.hex())
        kf2_chunk = kf2_type.KF2ChunkHeader(
            int.from_bytes(f.read(4), byteorder = 'little', signed = False),
            int.from_bytes(f.read(4), byteorder = 'little', signed = False),
            int.from_bytes(f.read(4), byteorder = 'little', signed = False))
        return kf2_chunk

    def getAllowedVersions(self):
        return []

    def parse(self, f, kf2_chunk: kf2_type.KF2ChunkHeader):
        pass

    def create(self, f, chunk_id: int, kf2_chunk: kf2_type.KF2ChunkHeader):
        if kf2_chunk.id != chunk_id:
            raise ValueError("Unknown chunk id %s" % hex(kf2_chunk.id))
        if kf2_chunk.version not in self.getAllowedVersions():
            raise ValueError("Unknown chunk version %i" % kf2_chunk.version)
        return self.parse(f, kf2_chunk)
