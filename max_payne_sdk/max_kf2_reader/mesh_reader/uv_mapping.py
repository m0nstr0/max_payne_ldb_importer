import max_payne_sdk.max_kf2_type as kf2_type
import max_payne_sdk.max_type as max_type
import max_payne_sdk.max_kf2_reader as kf2_reader
import struct


class UVMappingChunkReader(kf2_reader.KF2ReaderBase):
    def getAllowedVersions(self):
        return [1]

    def parse(self, f, kf2_chunk: kf2_type.KF2ChunkHeader):
        layer = max_type.parseType(f)
        num_coordinates = max_type.parseType(f)
        coordinates = []
        for i in range(num_coordinates):
            coordinates.append([
                struct.unpack("<f", f.read(4))[0],
                struct.unpack("<f", f.read(4))[0],
                struct.unpack("<f", f.read(4))[0]
            ])
        num_primitives = max_type.parseType(f)
        coordinates_per_primitive = []
        for i in range(num_primitives):
            coordinates_per_primitive.append(max_type.parseType(f))
        return kf2_type.UVMapping(kf2_chunk.version, layer, coordinates, coordinates_per_primitive)
