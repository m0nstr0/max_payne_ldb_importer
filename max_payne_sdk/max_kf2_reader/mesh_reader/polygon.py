import max_payne_sdk.max_kf2_type as kf2_type
import max_payne_sdk.max_type as max_type
import max_payne_sdk.max_kf2_reader as kf2_reader
import struct


class PolygonChunkReader(kf2_reader.KF2ReaderBase):
    def getAllowedVersions(self):
        return [0]

    def parse(self, f, kf2_chunk: kf2_type.KF2ChunkHeader):
        num_vertices = max_type.parseType(f)
        vertex_indices = []
        for i in range(num_vertices):
            vertex_indices.append(max_type.parseType(f))
        return kf2_type.Polygon(kf2_chunk.version, num_vertices, vertex_indices)