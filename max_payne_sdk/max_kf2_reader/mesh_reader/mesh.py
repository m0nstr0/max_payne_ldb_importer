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
        return [2]

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
            if kf2_chunk.id == kf2_type.REFFERENCE_TO_DATA:
                self.reference_to_data = kf2_reference_to_data.ReferenceToDataChunkReader().create(f, kf2_type.REFFERENCE_TO_DATA, kf2_mesh_chunk)
                continue
            if kf2_chunk.id == kf2_type.SMOOTHING:
                self.smoothing = kf2_smoothing.SmoothingChunkReader().create(f, kf2_type.SMOOTHING, kf2_mesh_chunk)
                continue
            f.seek(f.tell() - 13)
            break
        return kf2_type.Mesh(kf2_chunk.version, self.node, self.geometry, self.polygons, self.polygon_material, self.uv_mapping, self.reference_to_data, self.smoothing)