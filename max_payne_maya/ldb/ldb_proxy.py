from dataclasses import dataclass
import max_payne_sdk.max_ldb as max_ldb
import maya.api.OpenMaya as OpenMaya

@dataclass
class MayaTextureProxy:
    file_path: str
    file_type_name: str
    data: bytes

@dataclass
class MayaMaterialPropertiesProxy:
    pass

@dataclass
class MayaMaterialProxy:
    id: int
    name: str
    diffuse_texture: MayaTextureProxy
    alpha_texture: MayaTextureProxy
    reflection_texture: MayaTextureProxy
    gloss_texture: MayaTextureProxy
    detail_texture: MayaTextureProxy
    properties: MayaMaterialPropertiesProxy

@dataclass
class MayaStaticMeshProxy:
    transform: []
    vertices: []
    normals: []
    us: []
    vs: []
    light_map_us: []
    light_map_vs: []
    indices: []
    vertices_per_poly: []
    materials: []

@dataclass
class MayaDynamicMeshProxy(MayaStaticMeshProxy):
    pass

class MayaLDBProxy:
    def __init__(self, ldb):
        self.ldb = ldb

    def getMaterialsNum(self) -> int:
        if isinstance(self.ldb, max_ldb.MaxLDB):
            return len(self.ldb.getMaterials().materials)
        return 0

    def getTexturesNum(self) -> int:
        if isinstance(self.ldb, max_ldb.MaxLDB):
            return len(self.ldb.getTextures().textures)
        return 0

    def getMaterial(self, index: int) -> MayaMaterialProxy:
        material_id: int = 0
        material_name: str = ""
        diffuse_texture: MayaTextureProxy = None
        alpha_texture: MayaTextureProxy = None
        reflection_texture: MayaTextureProxy = None
        gloss_texture: MayaTextureProxy = None
        detail_texture: MayaTextureProxy = None
        properties: MayaMaterialPropertiesProxy = None

        if isinstance(self.ldb, max_ldb.MaxLDB):
            material = self.ldb.getMaterials().materials[index]
            material_id = material.id
            material_name = "max_payne_mat_%i" % material_id
            if material.diffuse_texture is not None:
                diffuse_texture = MayaTextureProxy(material.diffuse_texture.file_path, material.diffuse_texture.getFileTypeName(), material.diffuse_texture.data)
            if material.alpha_texture is not None:
                alpha_texture = MayaTextureProxy(material.alpha_texture.file_path, material.alpha_texture.getFileTypeName(), material.alpha_texture.data)

        return MayaMaterialProxy(
            material_id,
            material_name,
            diffuse_texture,
            alpha_texture,
            reflection_texture,
            gloss_texture,
            detail_texture,
            properties
        )

    def getMaterials(self) -> []:
        return [self.getMaterial(i) for i in range(self.getMaterialsNum())]

    def getRoomsNum(self) -> int:
        if isinstance(self.ldb, max_ldb.MaxLDB):
            return len(self.ldb.getRooms().rooms)
        return 0

    def getStaticMeshesNum(self) -> int:
        return self.getRoomsNum()

    def getDynamicMeshesNum(self) -> int:
        result = 0
        for i in range(self.getRoomsNum()):
            result += self.getDynamicMeshesNumByRoomId(i)
        return result

    def getStaticMeshByRoomId(self, room_id: int) -> MayaStaticMeshProxy:
        static_mesh_id = self.ldb.getRooms().rooms[room_id].static_meshes[0]
        mesh = self.ldb.getStaticMeshes().getById(static_mesh_id)
        vertices = []
        normals = []
        indices = []
        vertices_per_poly = []
        materials = {}
        us = []
        vs = []
        lightmap_us = []
        lightmap_vs = []
        for polygon_idx in range(mesh.numPolygons()):
            polygon = mesh.polygons.polygons[polygon_idx]
            poly_indices = []
            start_vertex = len(vertices)
            for i in range(polygon.num_vertices):
                texture_vertex = mesh.texture_vertices.texture_vertices[polygon.texture_vertex_idx + i]
                vertex = mesh.vertices.vertices[texture_vertex.vertex_idx]
                normal = mesh.normals.vertices[texture_vertex.vertex_idx]
                vertices.append(OpenMaya.MFloatPoint(-vertex.x * 100.0, vertex.y * 100.0, vertex.z * 100.0))
                normals.append(OpenMaya.MVector(-normal.x, normal.y, normal.z))
                us.append(texture_vertex.uv.u)
                vs.append(1 - texture_vertex.uv.v)
                lightmap_us.append(texture_vertex.lightmap_uv.u)
                lightmap_vs.append(1 - texture_vertex.lightmap_uv.v)
                poly_indices.append(start_vertex + i)
            if polygon.material.id in materials:
                materials[polygon.material.id].append(polygon_idx)
            else:
                materials[polygon.material.id] = [polygon_idx]
            poly_indices[1:] = poly_indices[len(poly_indices):0:-1]
            indices = indices + poly_indices
            vertices_per_poly.append(len(poly_indices))
        return MayaStaticMeshProxy(mesh.transform, vertices, normals, us, vs, lightmap_us, lightmap_vs, indices, vertices_per_poly, materials)

    def getDynamicMeshesNumByRoomId(self, room_id: int) -> int:
        return len(self.ldb.getRooms().rooms[room_id].dynamic_meshes)

    def getDynamicMeshByIdAndRoomId(self, room_id: int, dynamic_mesh_id: int) -> MayaDynamicMeshProxy:
        mesh = self.ldb.getDynamicMeshes().getBySharedName(self.ldb.getRooms().rooms[room_id].dynamic_meshes[dynamic_mesh_id])
        vertices = []
        normals = []
        indices = []
        vertices_per_poly = []
        materials = {}
        us = []
        vs = []
        lightmap_us = []
        lightmap_vs = []
        for polygon_idx in range(mesh.numPolygons()):
            polygon = mesh.polygons.polygons[polygon_idx]
            poly_indices = []
            start_vertex = len(vertices)
            for i in range(polygon.num_vertices):
                texture_vertex = mesh.texture_vertices.texture_vertices[polygon.texture_vertex_idx + i]
                vertex = mesh.vertices.vertices[texture_vertex.vertex_idx]
                normal = mesh.normals.vertices[texture_vertex.vertex_idx]
                vertices.append(OpenMaya.MFloatPoint(-vertex.x * 100.0, vertex.y * 100.0, vertex.z * 100.0))
                normals.append(OpenMaya.MVector(-normal.x, normal.y, normal.z))
                us.append(texture_vertex.uv.u)
                vs.append(1 - texture_vertex.uv.v)
                lightmap_us.append(texture_vertex.lightmap_uv.u)
                lightmap_vs.append(1 - texture_vertex.lightmap_uv.v)
                poly_indices.append(start_vertex + i)
            if polygon.material.id in materials:
                materials[polygon.material.id].append(polygon_idx)
            else:
                materials[polygon.material.id] = [polygon_idx]
            poly_indices[1:] = poly_indices[len(poly_indices):0:-1]
            indices = indices + poly_indices
            vertices_per_poly.append(len(poly_indices))
        return MayaDynamicMeshProxy(mesh.properties.object_to_room_transform, vertices, normals, us, vs, lightmap_us, lightmap_vs, indices, vertices_per_poly, materials)