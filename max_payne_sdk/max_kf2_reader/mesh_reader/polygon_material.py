import max_payne_sdk.max_kf2_type as kf2_type
import max_payne_sdk.max_type as max_type
import max_payne_sdk.max_kf2_reader as kf2_reader


class PolygonMaterialChunkReader(kf2_reader.KF2ReaderBase):
    def getAllowedVersions(self):
        return [1]

    def parse(self, f, kf2_chunk: kf2_type.KF2ChunkHeader):
        num_materials = max_type.parseType(f)
        name = []
        for i in range(num_materials):
            name.append(max_type.parseType(f))
        return kf2_type.PolygonMaterial(kf2_chunk.version, name)
