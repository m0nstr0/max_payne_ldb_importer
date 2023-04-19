import max_payne_sdk.max_kf2_type as kf2_type
import max_payne_sdk.max_type as max_type
import max_payne_sdk.max_kf2_reader as kf2_reader
import max_payne_sdk.max_kf2_reader.mesh_reader.polygon as kf2_polygon
import struct


class PolygonsChunkReader(kf2_reader.KF2ReaderBase):
    def getAllowedVersions(self):
        return [0, 1]

    def parse(self, f, kf2_chunk: kf2_type.KF2ChunkHeader):
        num_polygons = max_type.parseType(f)
        polygons_indices = []
        polygons_per_primitive = []
        if kf2_chunk.version == 0:
            for i in range(num_polygons):
                kf2_polygon_chunk = self.readChunk(f)
                polygon = kf2_polygon.PolygonChunkReader().create(f, kf2_type.POLYGON, kf2_polygon_chunk)
                polygons_indices = polygons_indices + polygon.vertex_indices
            polygons_per_primitive.append(int(len(polygons_indices) / 3))
            #unk1
            max_type.parseType(f)
            #unk2
            max_type.parseType(f)
        else:
            for i in range(num_polygons):
                polygons_indices.append(struct.unpack("<H", f.read(2))[0])
            num_primitives = max_type.parseType(f)
            for i in range(num_primitives):
                polygons_per_primitive.append(max_type.parseType(f))
        return kf2_type.Polygons(kf2_chunk.version, polygons_indices, polygons_per_primitive)