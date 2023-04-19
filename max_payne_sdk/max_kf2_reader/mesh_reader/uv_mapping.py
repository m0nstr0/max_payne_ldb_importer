import max_payne_sdk.max_kf2_type as kf2_type
import max_payne_sdk.max_type as max_type
import max_payne_sdk.max_kf2_reader as kf2_reader
import max_payne_sdk.max_kf2_reader.mesh_reader.polygon as kf2_polygon
import struct


class UVMappingChunkReader(kf2_reader.KF2ReaderBase):
    def getAllowedVersions(self):
        return [0, 1]

    def parse(self, f, kf2_chunk: kf2_type.KF2ChunkHeader):
        layer = max_type.parseType(f)
        polygons_uv_indices = []
        coordinates_per_primitive = []
        if kf2_chunk.version == 0:
            num_polygons = max_type.parseType(f)
            for i in range(num_polygons):
                kf2_polygon_chunk = self.readChunk(f)
                polygon = kf2_polygon.PolygonChunkReader().create(f, kf2_type.POLYGON, kf2_polygon_chunk)
                uv_indices = []
                for uv_index in polygon.vertex_indices:
                    uv_indices.append(uv_index)
                polygons_uv_indices.append(kf2_type.PolygonUVIndex(uv_indices))
            #reserved1
            max_type.parseType(f)
            #reserved2
            max_type.parseType(f)
        num_coordinates = max_type.parseType(f)
        coordinates = []
        for i in range(num_coordinates):
            if kf2_chunk.version == 0:
                coordinates.append(max_type.parseType(f))
            else:
                coordinates.append([
                    struct.unpack("<f", f.read(4))[0],
                    struct.unpack("<f", f.read(4))[0],
                    struct.unpack("<f", f.read(4))[0]
                ])
        if kf2_chunk.version == 1:
            num_primitives = max_type.parseType(f)
            for i in range(num_primitives):
                coordinates_per_primitive.append(max_type.parseType(f))
        return kf2_type.UVMapping(kf2_chunk.version, layer, coordinates, coordinates_per_primitive, polygons_uv_indices)