import max_payne_sdk.max_kf2_type as kf2_type
import max_payne_sdk.max_type as max_type
import max_payne_sdk.max_kf2_reader as kf2_reader

class SkinChunkReader(kf2_reader.KF2ReaderBase):
    def getAllowedVersions(self):
        return [0, 1]

    def parse(self, f, kf2_chunk: kf2_type.KF2ChunkHeader):
        skin_vertices = []
        if kf2_chunk.version == 0:
            bones_list_per_vertex = {}
            weights_list_per_vertex = {}
            for i in range(3):
                for j in range(max_type.parseType(f)):
                    vertex_index = max_type.parseType(f)
                    bone_index = max_type.parseType(f)
                    weight = max_type.parseType(f)
                    if vertex_index not in bones_list_per_vertex:
                        bones_list_per_vertex[vertex_index] = [bone_index]
                        weights_list_per_vertex[vertex_index] = [weight]
                    else:
                        bones_list_per_vertex[vertex_index].append(bone_index)
                        weights_list_per_vertex[vertex_index].append(weight)
            for key in bones_list_per_vertex:
                skin_vertices.append(kf2_type.SkinVertex(
                    key,
                    bones_list_per_vertex[key],
                    weights_list_per_vertex[key]
                ))
        if kf2_chunk.version == 1:
            f.read(1)
        skin_object_names = []
        for i in range(max_type.parseType(f)):
            skin_object_names.append(max_type.parseType(f))
        if kf2_chunk.version == 1:
            f.read(1)
        skeleton_object_names = []
        for i in range(max_type.parseType(f)):
            skeleton_object_names.append(max_type.parseType(f))
        if kf2_chunk.version == 0:
            for i in range(max_type.parseType(f)):
                max_type.parseType(f)
        if kf2_chunk.version == 1:
            f.read(1)
            vertex_indices = []
            for i in range(max_type.parseType(f)):
                vertex_indices.append(max_type.parseType(f))
            f.read(1)
            bones_num_per_vertex = []
            for i in range(max_type.parseType(f)):
                bones_num_per_vertex.append(max_type.parseType(f))
            f.read(1)
            bones_list_per_vertex = []
            for i in range(max_type.parseType(f)):
                bones_list_per_vertex.append(max_type.parseType(f))
            f.read(1)
            weights = []
            for i in range(max_type.parseType(f)):
                weights.append(max_type.parseType(f))
            f.read(1)
            vertex_num_per_primitive = []
            for i in range(max_type.parseType(f)):
                vertex_num_per_primitive.append(max_type.parseType(f))
            f.read(1)
            vertex_start_index_per_primitive = []
            for i in range(max_type.parseType(f)):
                vertex_start_index_per_primitive.append(max_type.parseType(f))

            skin_vertices = []
            for vertex_index in range(len(vertex_indices)):
                vertex_offset = vertex_indices[vertex_index]
                num_bones = bones_num_per_vertex[vertex_index]
                skin_vertices.append(kf2_type.SkinVertex(
                    vertex_index,
                    bones_list_per_vertex[vertex_offset: vertex_offset + num_bones],
                    weights[vertex_offset: vertex_offset + num_bones]
                ))
        return kf2_type.Skin(kf2_chunk.version, skin_object_names, skeleton_object_names, skin_vertices)