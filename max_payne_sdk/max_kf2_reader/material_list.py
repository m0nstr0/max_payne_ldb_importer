import max_payne_sdk.max_type as max_type
import max_payne_sdk.max_kf2_type as kf2_type
import max_payne_sdk.max_kf2_reader as kf2_reader
import max_payne_sdk.max_kf2_reader.material as kf2_material

class MaterialListChunkReaderV0(kf2_reader.KF2ReaderBase):
    def __parseChunk(self, kf2_chunk: kf2_type.KF2ChunkHeader, f):
        if kf2_chunk.version == 1:
            return kf2_material.MaterialChunkReaderV1().parse(f)
        if kf2_chunk.version == 2:
            return kf2_material.MaterialChunkReaderV2().parse(f)
        raise ValueError("Unknown material chunk version %s" % kf2_chunk.version)

    def parse(self, f):
        texture_dirs = max_type.parseType(f)
        materials = []
        for i in range(max_type.parseType(f)):
            kf2_chunk = self.readChunk(f)
            materials.append(self.__parseChunk(kf2_chunk, f))
        return kf2_type.MaterialListV0(0, texture_dirs, materials)

class MaterialListChunkReader:
    def create(self, kf2_chunk: kf2_type.KF2ChunkHeader):
        if (kf2_chunk.id != kf2_type.MATERIAL_LIST):
            raise ValueError("Unknown chunk id %s" % kf2_chunk.id.hex())
        if (kf2_chunk.version == 0):
            return MaterialListChunkReaderV0()
        raise ValueError("Unknown material list chunk version %i" % kf2_chunk.version)