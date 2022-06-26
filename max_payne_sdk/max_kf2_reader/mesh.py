import max_payne_sdk.max_kf2_type as kf2_type
import max_payne_sdk.max_kf2_reader as kf2_reader
import max_payne_sdk.max_type as max_type
import max_payne_sdk.max_kf2_reader.node as kf2_node
import max_payne_sdk.max_kf2_reader.geometry as kf2_geometry
import max_payne_sdk.max_kf2_reader.polygons as kf2_polygons
import max_payne_sdk.max_kf2_reader.polygon_material as kf2_polygon_material
import max_payne_sdk.max_kf2_reader.uv_mapping as kf2_uv_mapping
import max_payne_sdk.max_kf2_reader.refference_to_data as kf2_reference_to_data
import max_payne_sdk.max_kf2_reader.smoothing as kf2_smoothing

class MeshChunkReaderV1(kf2_reader.KF2ReaderBase):
    def parse(self, f):
        raise Exception("Mesh v1 unsupported yet")

class MeshChunkReaderV2(kf2_reader.KF2ReaderBase):
    def __init__(self) -> None:
        self.node = None
        self.geometry = None
        self.polygons = None
        self.polygon_matterial = None
        self.uv_mapping = []
        self.refference_to_data = None
        self.smoothing = None

    def __parseChunk(self, kf2_chunk, f) -> bool:
        if kf2_chunk.id == kf2_type.NODE:
            if kf2_chunk.version != 1:
                raise ValueError("Unknown node chunk version %s" % kf2_chunk.version.hex())
            self.node = kf2_node.NodeChunkReaderV1().parse(f)
            return True
        if kf2_chunk.id == kf2_type.GEOMETRY:
            if kf2_chunk.version != 1:
                raise ValueError("Unknown geometry chunk version %s" % kf2_chunk.version.hex())
            self.geometry = kf2_geometry.GeometryChunkReaderV1().parse(f)
            return True
        if kf2_chunk.id == kf2_type.POLYGONS:
            if kf2_chunk.vertsion != 1:
                raise ValueError("Unknown polygons chunk version %s" % kf2_chunk.version.hex())
            self.polygons = kf2_polygons.PolygonsChunkReaderV1().parse(f)
            return True
        if kf2_chunk.id == kf2_type.POLYGON_MATERIAL:
            if kf2_chunk.vertsion != 1:
                raise ValueError("Unknown polygon material chunk version %s" % kf2_chunk.version.hex())
            self.polygon_matterial = kf2_polygon_material.PolygonMaterialChunkReaderV1().parse(f)
            return True
        if kf2_chunk.id == kf2_type.UVMAPPING:
            if kf2_chunk.vertsion != 1:
                raise ValueError("Unknown polygon material chunk version %s" % kf2_chunk.version.hex())
            self.uv_mapping.append(kf2_uv_mapping.UVMappingChunkReaderV1().parse(f))
            return True
        if kf2_chunk.id == kf2_type.REFFERENCE_TO_DATA:
            if kf2_chunk.vertsion != 0:
                raise ValueError("Unknown refference to data chunk version %s" % kf2_chunk.version.hex())
            self.refference_to_data = kf2_reference_to_data.ReferenceToDataChunkReaderV0().parse(f)
            return True
        if kf2_chunk.id == kf2_type.SMOOTHING:
            if kf2_chunk.vertsion != 0:
                raise ValueError("Unknown smoothing chunk version %s" % kf2_chunk.version.hex())
            raise Exception("Smoothing unsupported yet")
            self.smoothing = kf2_smoothing.SmoothingChunkReaderV0().parse(f)
            return True
        f.seek(f.tell() - 13)
        return False
        
    def parse(self, f):
        kf2_chunk = self.readChunk(f)
        while self.__parseChunk(kf2_chunk, f):
            kf2_chunk = self.readChunk(f)
        return kf2_type.MeshV2(self.node, self.geometry, self.polygons, self.polygon_matterial, self.uv_mapping, self.refference_to_data, self.smoothing)

class MeshChunkReader:
    def create(self, kf2_chunk: kf2_type.KF2ChunkHeader):
        if kf2_chunk.id != kf2_type.MATERIAL_LIST:
            raise ValueError("Unknown chunk id %s" % kf2_chunk.id.hex())
        if kf2_chunk.version == 1:
            return MeshChunkReaderV1()
        if kf2_chunk.version == 2:
            return MeshChunkReaderV2()
        raise ValueError("Unknown mesh chunk version %i" % kf2_chunk.version)