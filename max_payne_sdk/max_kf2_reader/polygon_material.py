import max_payne_sdk.max_kf2_type as kf2_type
import max_payne_sdk.max_type as max_type

class PolygonMaterialChunkReaderV1:
    def parse(self, f):
        num_materials = max_type.parseType(f)
        name: list[str] = []
        for i in range(num_materials):
            name.append(max_type.parseType(f))
        return kf2_type.PolygonMaterialV1(1, name)