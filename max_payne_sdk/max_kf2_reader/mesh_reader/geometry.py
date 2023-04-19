import max_payne_sdk.max_kf2_type as kf2_type
import max_payne_sdk.max_kf2_reader as kf2_reader
import max_payne_sdk.max_type as max_type
import struct


class GeometryChunkReader(kf2_reader.KF2ReaderBase):
    def getAllowedVersions(self):
        return [0, 1]

    def parse(self, f, kf2_chunk: kf2_type.KF2ChunkHeader):
        num_vertices = max_type.parseType(f)
        vertices = []
        for i in range(num_vertices):
            if kf2_chunk.version == 0:
                vertices.append(max_type.parseType(f))
            else:
                vertices.append([
                    struct.unpack("<f", f.read(4))[0],
                    struct.unpack("<f", f.read(4))[0],
                    struct.unpack("<f", f.read(4))[0]
                ])
        normals = []
        vertices_per_primitive = []
        if kf2_chunk.version == 0:
            vertices_per_primitive.append(len(vertices))
        else:
            for i in range(num_vertices):
                normals.append([
                    struct.unpack("<f", f.read(4))[0],
                    struct.unpack("<f", f.read(4))[0],
                    struct.unpack("<f", f.read(4))[0]
                ])
            num_primitives = max_type.parseType(f)
            vertices_per_primitive = []
            for i in range(num_primitives):
                vertices_per_primitive.append(max_type.parseType(f))
        return kf2_type.Geometry(kf2_chunk.version, vertices, normals, vertices_per_primitive)
