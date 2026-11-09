"""Skin v0 influence triples and v1 packed per-primitive weight tables."""
import math

import max_payne_sdk.max_kf2_type as kf2_type
import max_payne_sdk.max_type as max_type
import max_payne_sdk.max_kf2_reader as kf2_reader
from max_payne_sdk.binary import FormatError, read_exact, read_count


def _array(stream, packed):
    if packed and read_exact(stream, 1) != b'\x1c':
        raise FormatError("Expected Skin vector marker 1c")
    return [max_type.parseType(stream) for _ in range(read_count(stream))]


class SkinChunkReader(kf2_reader.KF2ReaderBase):
    def getAllowedVersions(self):
        return [0, 1]

    def parse(self, f, kf2_chunk):
        vertices = {}
        if kf2_chunk.version == 0:
            for _ in range(3):
                for _ in range(read_count(f)):
                    index = max_type.parseType(f)
                    bone = max_type.parseType(f)
                    weight = max_type.parseType(f)
                    if not isinstance(index, int) or index < 0:
                        raise FormatError("Invalid legacy Skin vertex index")
                    vertex = vertices.setdefault(index, kf2_type.SkinVertex(index, [], []))
                    vertex.vertex_bone_indices.append(bone)
                    vertex.vertex_weights.append(weight)

        packed = kf2_chunk.version == 1
        skin_names = _array(f, packed)
        bone_names = _array(f, packed)
        counts, offsets, legacy = [], [], []
        if not packed:
            legacy = _array(f, False)
        else:
            data_offsets = _array(f, True)
            bone_counts = _array(f, True)
            bones = _array(f, True)
            weights = _array(f, True)
            counts = _array(f, True)
            offsets = _array(f, True)
            if len(data_offsets) != len(bone_counts) or len(bones) != len(weights):
                raise FormatError("Mismatched Skin influence arrays")
            if len(counts) != len(offsets):
                raise FormatError("Mismatched Skin primitive arrays")
            for count, offset in zip(counts, offsets):
                self._range(offset, count, len(data_offsets), "primitive")
            for index, (offset, count) in enumerate(zip(data_offsets, bone_counts)):
                self._range(offset, count, len(bones), "influence")
                vertices[index] = kf2_type.SkinVertex(
                    index, bones[offset:offset + count], weights[offset:offset + count])

        for vertex in vertices.values():
            for bone, weight in zip(vertex.vertex_bone_indices, vertex.vertex_weights):
                if not isinstance(bone, int) or not 0 <= bone < len(bone_names):
                    raise FormatError("Skin bone index outside skeleton name table")
                if not isinstance(weight, (int, float)) or not math.isfinite(weight):
                    raise FormatError("Non-finite Skin weight")
        return kf2_type.Skin(kf2_chunk.version, skin_names, bone_names,
                             list(vertices.values()), counts, offsets, legacy)

    @staticmethod
    def _range(offset, count, size, name):
        if (not isinstance(offset, int) or not isinstance(count, int)
                or offset < 0 or count < 0 or offset + count > size):
            raise FormatError("Skin %s range outside table" % name)
