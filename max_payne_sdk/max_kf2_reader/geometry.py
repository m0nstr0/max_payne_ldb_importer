import max_payne_sdk.max_kf2_type as kf2_type
import max_payne_sdk.max_type as max_type
import struct

class GeometryChunkReaderV1:
    def parse(self, f):
        num_vertices = max_type.parseType(f)
        vertices: list[float] = []
        for i in range(num_vertices):
            vertices.append([
                struct.unpack("<f", f.read(4))[0],
                struct.unpack("<f", f.read(4))[0],
                struct.unpack("<f", f.read(4))[0]
                ])
        normals: list[float] = []
        for i in range(num_vertices):
            normals.append([
                struct.unpack("<f", f.read(4))[0],
                struct.unpack("<f", f.read(4))[0],
                struct.unpack("<f", f.read(4))[0]
                ])
        num_primitives = max_type.parseType(f)
        vertices_per_primitive: list[uint] = []
        for i in range(num_primitives):
            vertices_per_primitive.append(max_type.parseType(f))
        return kf2_type.GeometryV1(1, vertices, normals, vertices_per_primitive)