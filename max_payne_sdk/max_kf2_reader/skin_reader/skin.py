import max_payne_sdk.max_kf2_type as kf2_type
import max_payne_sdk.max_type as max_type
import max_payne_sdk.max_kf2_reader as kf2_reader

class SkinChunkReader(kf2_reader.KF2ReaderBase):
    def getAllowedVersions(self):
        return [1]

    def parse(self, f, kf2_chunk: kf2_type.KF2ChunkHeader):
        f.read(1)
        skin_object_names = []
        for i in range(max_type.parseType(f)):
            skin_object_names.append(max_type.parseType(f))
        f.read(1)
        skeleton_object_names = []
        for i in range(max_type.parseType(f)):
            skeleton_object_names.append(max_type.parseType(f))
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