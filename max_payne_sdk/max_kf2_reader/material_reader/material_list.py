import max_payne_sdk.max_type as max_type
import max_payne_sdk.max_kf2_type as kf2_type
import max_payne_sdk.max_kf2_reader as kf2_reader
import max_payne_sdk.max_kf2_reader.material_reader.material as kf2_material


class MaterialListChunkReader(kf2_reader.KF2ReaderBase):
    def getAllowedVersions(self):
        return [0]

    def parse(self, f, kf2_chunk: kf2_type.KF2ChunkHeader):
        texture_dirs = max_type.parseType(f)
        materials = []
        for i in range(max_type.parseType(f)):
            kf2_chunk = self.readChunk(f)
            materials.append(kf2_material.MaterialChunkReader().create(f, kf2_type.MATERIAL, kf2_chunk))
        return kf2_type.MaterialList(kf2_chunk.version, texture_dirs, materials)