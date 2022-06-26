import max_payne_sdk.max_kf2_type as kf2_type
import max_payne_sdk.max_type as max_type
import struct

class UVMappingChunkReaderV1:
    def parse(self, f):
        layer = max_type.parseType(f)
        num_coordinates =  max_type.parseType(f)
        coordinates: list[float] = []
        for i in range(num_vertices):
            coordinates.append([
                struct.unpack("<f", f.read(4))[0],
                struct.unpack("<f", f.read(4))[0],
                struct.unpack("<f", f.read(4))[0]
                ])
        num_primitives = max_type.parseType(f)
        coordinates_per_primitive: list[uint] = []
        for i in range(num_primitives):
            coordinates_per_primitive.append(max_type.parseType(f))
        return kf2_type.UVMappingV1(1, layer, coordinates, coordinates_per_primitive)