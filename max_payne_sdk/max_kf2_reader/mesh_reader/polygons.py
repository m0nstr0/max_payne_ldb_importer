import max_payne_sdk.max_kf2_type as kf2_type
import max_payne_sdk.max_type as max_type
import max_payne_sdk.max_kf2_reader as kf2_reader
import struct


class PolygonsChunkReader(kf2_reader.KF2ReaderBase):
    def getAllowedVersions(self):
        return [1]

    def parse(self, f, kf2_chunk: kf2_type.KF2ChunkHeader):
        num_polygons = max_type.parseType(f)
        polygons_indices = []
        for i in range(num_polygons):
            polygons_indices.append(struct.unpack("<H", f.read(2))[0])
        num_primitives = max_type.parseType(f)
        polygons_per_primitive = []
        for i in range(num_primitives):
            polygons_per_primitive.append(max_type.parseType(f))
        return kf2_type.Polygons(kf2_chunk.version, polygons_indices, polygons_per_primitive)
