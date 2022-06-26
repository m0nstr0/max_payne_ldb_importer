import max_payne_sdk.max_kf2_type as kf2_type

class KF2ReaderBase:
    def readChunk(self, f):
        chunk_tag = f.read(1)
        if chunk_tag != kf2_type.CHUNK_HEADER_ID:
            raise ValueError("Unknown chunk tag id %s" % chunk_tag.hex())
        kf2_chunk = kf2_type.KF2ChunkHeader(
            int.from_bytes(f.read(4), 'little', False), 
            int.from_bytes(f.read(4), 'little', False), 
            int.from_bytes(f.read(4), 'little', False))
        return kf2_chunk