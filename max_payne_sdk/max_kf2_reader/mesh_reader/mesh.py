import math

import max_payne_sdk.max_kf2_type as kf2_type
import max_payne_sdk.max_kf2_reader as kf2_reader
import max_payne_sdk.max_kf2_reader.node as kf2_node
import max_payne_sdk.max_kf2_reader.mesh_reader.geometry as kf2_geometry
import max_payne_sdk.max_kf2_reader.mesh_reader.polygons as kf2_polygons
import max_payne_sdk.max_kf2_reader.mesh_reader.polygon_material as kf2_polygon_material
import max_payne_sdk.max_kf2_reader.mesh_reader.uv_mapping as kf2_uv_mapping
import max_payne_sdk.max_kf2_reader.mesh_reader.refference_to_data as kf2_reference_to_data
import max_payne_sdk.max_kf2_reader.mesh_reader.smoothing as kf2_smoothing


class MeshChunkReader(kf2_reader.KF2ReaderBase):
    def getAllowedVersions(self):
        return [1, 2]

    def parse(self, f, kf2_chunk: kf2_type.KF2ChunkHeader):
        self.node = None
        self.geometry = None
        self.polygons = None
        self.polygon_material = None
        self.reference_to_data = None
        self.uv_mapping = []
        self.smoothing = None
        while True:
            kf2_mesh_chunk = self.readChunk(f)
            if kf2_mesh_chunk is None:
                break
            if kf2_mesh_chunk.id == kf2_type.NODE:
                self.node = kf2_node.NodeChunkReader().create(f, kf2_type.NODE, kf2_mesh_chunk)
                continue
            if kf2_mesh_chunk.id == kf2_type.GEOMETRY:
                self.geometry = kf2_geometry.GeometryChunkReader().create(f, kf2_type.GEOMETRY, kf2_mesh_chunk)
                continue
            if kf2_mesh_chunk.id == kf2_type.POLYGONS:
                self.polygons = kf2_polygons.PolygonsChunkReader().create(f, kf2_type.POLYGONS, kf2_mesh_chunk)
                continue
            if kf2_mesh_chunk.id == kf2_type.POLYGON_MATERIAL:
                self.polygon_material = kf2_polygon_material.PolygonMaterialChunkReader().create(f, kf2_type.POLYGON_MATERIAL, kf2_mesh_chunk)
                continue
            if kf2_mesh_chunk.id == kf2_type.UVMAPPING:
                self.uv_mapping.append(kf2_uv_mapping.UVMappingChunkReader().create(f, kf2_type.UVMAPPING, kf2_mesh_chunk))
                continue
            if kf2_mesh_chunk.id == kf2_type.REFFERENCE_TO_DATA:
                self.reference_to_data = kf2_reference_to_data.ReferenceToDataChunkReader().create(f, kf2_type.REFFERENCE_TO_DATA, kf2_mesh_chunk)
                continue
            if kf2_mesh_chunk.id == kf2_type.SMOOTHING:
                self.smoothing = kf2_smoothing.SmoothingChunkReader().create(f, kf2_type.SMOOTHING, kf2_mesh_chunk)
                continue
            f.seek(f.tell() - 13)
            break

        if kf2_chunk.version == 2 and self.geometry is not None and self.polygons is not None:
            vertex_start_index = {0:0}
            for primitive_id in range(len(self.geometry.vertices_per_primitive)):
                vertex_start_index[primitive_id + 1] = vertex_start_index[primitive_id] + self.geometry.vertices_per_primitive[primitive_id]

            material_index_for_polygon = [[] for i in range(int(len(self.polygons.polygons_indices) / 3))]
            start_index = 0
            polygons_indices = []
            polygons_uv_indices = []
            for primitive_id in range(len(self.polygons.polygons_per_primitive)):
                for polygon_id in range(self.polygons.polygons_per_primitive[primitive_id]):
                    vertex_a = self.polygons.polygons_indices[start_index + 0] + vertex_start_index[primitive_id]
                    vertex_b = self.polygons.polygons_indices[start_index + 1] + vertex_start_index[primitive_id]
                    vertex_c = self.polygons.polygons_indices[start_index + 2] + vertex_start_index[primitive_id]
                    polygons_indices.append(vertex_a)
                    polygons_indices.append(vertex_b)
                    polygons_indices.append(vertex_c)
                    material_index_for_polygon[int(start_index / 3)] = primitive_id
                    polygons_uv_indices.append(kf2_type.PolygonUVIndex([vertex_a, vertex_b, vertex_c]))
                    start_index += 3

            self.polygons.polygons_indices = polygons_indices
            for i in range(len(self.uv_mapping)):
                self.uv_mapping[i].polygons_uv_indices = polygons_uv_indices

            if self.polygon_material is not None:
                self.polygon_material.material_index_for_polygon = material_index_for_polygon

        return kf2_type.Mesh(kf2_chunk.version, self.node, self.geometry, self.polygons, self.polygon_material, self.uv_mapping, self.reference_to_data, self.smoothing)