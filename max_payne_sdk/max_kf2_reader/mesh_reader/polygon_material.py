import max_payne_sdk.max_kf2_type as kf2_type
import max_payne_sdk.max_type as max_type
import max_payne_sdk.max_kf2_reader as kf2_reader


class PolygonMaterialChunkReader(kf2_reader.KF2ReaderBase):
    def getAllowedVersions(self):
        return [0, 1]

    def parse(self, f, kf2_chunk: kf2_type.KF2ChunkHeader):
        num_materials = max_type.parseType(f)
        name = []
        material_index_for_polygon = []
        for i in range(num_materials):
            name.append(max_type.parseType(f))
        if kf2_chunk.version == 0:
            num_polygons = max_type.parseType(f)
            for i in range(num_polygons):
                material_index_for_polygon.append(max_type.parseType(f))
        return kf2_type.PolygonMaterial(kf2_chunk.version, name, material_index_for_polygon)