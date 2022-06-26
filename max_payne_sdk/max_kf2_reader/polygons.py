import max_payne_sdk.max_kf2_type as kf2_type
import max_payne_sdk.max_type as max_type
import struct

class PolygonsChunkReaderV1:
    def parse(self, f):
        num_polygons = max_type.parseType(f)
        polygons_indicies: list[int] = []
        for i in range(num_polygons):
            polygons_indicies.append(struct.unpack("<H", f.read(2))[0])
        num_primitives = max_type.parseType(f)
        polygons_per_primitive: list[uint] = []
        for i in range(num_primitives):
            polygons_per_primitive.append(max_type.parseType(f))
        return kf2_type.PolygonsV1(1, polygons_indicies, polygons_per_primitive)