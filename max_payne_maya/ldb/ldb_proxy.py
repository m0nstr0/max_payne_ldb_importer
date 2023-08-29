from dataclasses import dataclass
from max_payne_sdk.ldb.max_ldb_type import MaxLDB
from max_payne_sdk.ldb2.max_ldb2_type import MaxLDB2
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
        return len(self.ldb.getMaterials())

    def getMaterial(self, index: int) -> MayaMaterialProxy:
        material_id: int = 0
        material_name: str = ""
        diffuse_texture: MayaTextureProxy = None
        alpha_texture: MayaTextureProxy = None
        reflection_texture: MayaTextureProxy = None
        gloss_texture: MayaTextureProxy = None
        detail_texture: MayaTextureProxy = None
        properties: MayaMaterialPropertiesProxy = None

        if isinstance(self.ldb, MaxLDB):
            material = self.ldb.getMaterials()[index]
            material_id = material.id
            material_name = "max_payne_mat_%i" % material_id
            if material.diffuse_texture is not None:
                diffuse_texture = MayaTextureProxy(material.diffuse_texture.file_path, material.diffuse_texture.getFileTypeName(), material.diffuse_texture.data)
            if material.alpha_texture is not None:
                alpha_texture = MayaTextureProxy(material.alpha_texture.file_path, material.alpha_texture.getFileTypeName(), material.alpha_texture.data)

        if isinstance(self.ldb, MaxLDB2):
            material = self.ldb.getMaterials()[index]
            material_id = material.id
            material_name = "max_payne_mat_%i" % material_id
            if material.diffuse_texture is not None:
                diffuse_texture = MayaTextureProxy(material.diffuse_texture.file_path, material.diffuse_texture.getFileTypeName(), material.diffuse_texture.data)
            if material.reflection_texture is not None:
                reflection_texture = MayaTextureProxy(material.reflection_texture.file_path, material.reflection_texture.getFileTypeName(), material.reflection_texture.data)
            if material.gloss_texture is not None:
                gloss_texture = MayaTextureProxy(material.gloss_texture.file_path, material.gloss_texture.getFileTypeName(), material.gloss_texture.data)
            if material.detail_texture is not None:
                detail_texture = MayaTextureProxy(material.detail_texture.file_path, material.detail_texture.getFileTypeName(), material.detail_texture.data)

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
        return len(self.ldb.getRooms())

    def getStaticMeshesNum(self) -> int:
        return self.getRoomsNum()

    def getDynamicMeshesNum(self) -> int:
        result = 0
        if isinstance(self.ldb, MaxLDB2):
            return 0
        if isinstance(self.ldb, MaxLDB):
            for i in range(self.getRoomsNum()):
                result += self.getDynamicMeshesNumByRoomId(i)
        return result

    def getStaticMeshByRoomId(self, room_id: int) -> MayaStaticMeshProxy:
        vertices = []
        normals = []
        indices = []
        vertices_per_poly = []
        materials = {}
        us = []
        vs = []
        lightmap_us = []
        lightmap_vs = []
        transform = []
        if isinstance(self.ldb, MaxLDB2):
            transform = self.ldb.getRooms()[room_id].transform
            mesh = self.ldb.getRooms()[room_id].static_mesh
            start_poly = 0
            for part_id in range(len(mesh)):
                start_vertex = len(vertices)
                indices = indices + [start_vertex + index for index in mesh[part_id].indices]
                vertices = vertices + [OpenMaya.MFloatPoint(-vertex.x * 100.0, vertex.y * 100.0, vertex.z * 100.0) for vertex in mesh[part_id].vertices]
                normals = normals + [OpenMaya.MFloatPoint(-normal.x, normal.y, normal.z) for normal in mesh[part_id].normals]
                us = us + [uv.u for uv in mesh[part_id].uvs]
                vs = vs + [1 - uv.v for uv in mesh[part_id].uvs]
                lightmap_us = lightmap_us + [uv.u for uv in mesh[part_id].lightmap_uvs]
                lightmap_vs = lightmap_vs + [1 - uv.v for uv in mesh[part_id].lightmap_uvs]
                if mesh[part_id].material_id in materials:
                    materials[mesh[part_id].material_id] = materials[mesh[part_id].material_id] + [poly_id for poly_id in range(start_poly, start_poly + len(mesh[part_id].indices))]
                else:
                    materials[mesh[part_id].material_id] = [poly_id for poly_id in range(start_poly, start_poly + int(len(mesh[part_id].indices) / 3))]
                start_poly = start_poly + int(len(mesh[part_id].indices) / 3)
                vertices_per_poly = vertices_per_poly + [3 for _ in range(int(len(mesh[part_id].indices) / 3))]

        if isinstance(self.ldb, MaxLDB):
            static_mesh_id = self.ldb.getRooms()[room_id].static_meshes[0]
            mesh = self.ldb.getStaticMeshes().getById(static_mesh_id)
            transform = mesh.transform
            for polygon_idx in range(mesh.numPolygons()):
                polygon = mesh.polygons[polygon_idx]
                poly_indices = []
                start_vertex = len(vertices)
                for i in range(polygon.num_vertices):
                    texture_vertex = mesh.texture_vertices[polygon.texture_vertex_idx + i]
                    vertex = mesh.vertices[texture_vertex.vertex_idx]
                    normal = mesh.normals[texture_vertex.vertex_idx]
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

        return MayaStaticMeshProxy(transform, vertices, normals, us, vs, lightmap_us, lightmap_vs, indices, vertices_per_poly, materials)

    def getDynamicMeshesNumByRoomId(self, room_id: int) -> int:
        return len(self.ldb.getRooms()[room_id].dynamic_meshes)

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
            polygon = mesh.polygons[polygon_idx]
            poly_indices = []
            start_vertex = len(vertices)
            for i in range(polygon.num_vertices):
                texture_vertex = mesh.texture_vertices[polygon.texture_vertex_idx + i]
                vertex = mesh.vertices[texture_vertex.vertex_idx]
                normal = mesh.normals[texture_vertex.vertex_idx]
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