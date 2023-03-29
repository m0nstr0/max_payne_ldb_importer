import maya.cmds as mc
import sys
import maya.OpenMayaMPx as OpenMayaMPx
import maya.api.OpenMaya as OpenMaya
import math

class MayaLDBMeshlOps:
    def __init__(self, ldb, materials, progress_callback) -> None:
        self.ldb = ldb
        self.materials = materials
        self.progress_callback = progress_callback
        self.processGeometry()

    def createPolygons(self, mesh):
        vertices = []
        normals = []
        indices = []
        vertices_per_poly = []
        materials = {}
        us = []
        vs = []
        uvs = []
        for polygon_idx in range(mesh.numPolygons()):
            if not self.progress_callback.updateProgressBar("Importing: Processing geometry"):
                break
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
                poly_indices.append(start_vertex + i)
            if polygon.material.id in materials:
                materials[polygon.material.id].append(polygon_idx)
            else:
                materials[polygon.material.id] = [polygon_idx]
            poly_indices[1:] = poly_indices[len(poly_indices):0:-1]
            indices = indices + poly_indices
            vertices_per_poly.append(len(poly_indices))

        new_mesh = OpenMaya.MFnMesh()
        new_mesh.create(vertices, vertices_per_poly, indices, us, vs)
        new_mesh.setVertexNormals(normals, range(len(vertices)))
        new_mesh.assignUVs(vertices_per_poly, indices)
        for material_id, polygons in materials.items():
            mc.select(clear = True)
            for polygon_id in polygons:
                mc.select('%s.f[%i]' % (new_mesh.name(), polygon_id), add = True)
            mc.hyperShade(assign = self.materials.getMaterialNameById(material_id))
        new_mesh.updateSurface()

        group_up = OpenMaya.MSelectionList()
        group_up.add(new_mesh.getPath())
        return group_up

    def groupAndTransform(self, group_up, transfrom):
        matrix = OpenMaya.MMatrix([
            transfrom[0] + [0.0], 
            transfrom[1] + [0.0], 
            transfrom[2] + [0.0], 
            transfrom[3] + [1.0]
        ])
        OpenMaya.MGlobal.setActiveSelectionList(group_up)
        group = mc.listRelatives(mc.ls(selection=True), parent=True, fullPath=False)[0]
        if group_up.length() > 1:
            group = mc.group()
        mc.move(0, 0, 0, group + ".scalePivot", group + ".rotatePivot")
        mm_transform = OpenMaya.MTransformationMatrix(matrix)
        translation = mm_transform.translation(OpenMaya.MSpace.kWorld)
        rotation = mm_transform.rotation(asQuaternion=False)
        scale = mm_transform.scale(OpenMaya.MSpace.kWorld)
        mc.rotate(rotation[0] * (180/math.pi), -rotation[1] * (180/math.pi), -rotation[2] * (180/math.pi), group, absolute=True)
        mc.move(-translation[0] * 100.0, translation[1] * 100.0, translation[2] * 100.0, group, absolute=True)
        mc.scale(scale[0], scale[1], scale[2], group, absolute=True)
        if group_up.length() > 1:
            mc.polyUnite(group, constructionHistory=False)
        return group

    def invRotationMatrix(self, in_m):
        m = [x[:] for x in in_m]
        det = m[0][0] * (m[1][1] * m[2][2] - m[2][1] * m[1][2]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0]) + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
        if det == 0:
            return m
        invdet = 1.0 / det
        m[0][0] = (m[1][1] * m[2][2] - m[2][1] * m[1][2]) * invdet
        m[0][1] = (m[0][2] * m[2][1] - m[0][1] * m[2][2]) * invdet
        m[0][2] = (m[0][1] * m[1][2] - m[0][2] * m[1][1]) * invdet
        m[1][0] = (m[1][2] * m[2][0] - m[1][0] * m[2][2]) * invdet
        m[1][1] = (m[0][0] * m[2][2] - m[0][2] * m[2][0]) * invdet
        m[1][2] = (m[1][0] * m[0][2] - m[0][0] * m[1][2]) * invdet
        m[2][0] = (m[1][0] * m[2][1] - m[2][0] * m[1][1]) * invdet
        m[2][1] = (m[2][0] * m[0][1] - m[0][0] * m[2][1]) * invdet
        m[2][2] = (m[0][0] * m[1][1] - m[1][0] * m[0][1]) * invdet
        return m

    def transformNodeWithParent(self, parent, child):
        result = [x[:] for x in parent]
        result = self.invRotationMatrix(result)
        for i in range(3):
            for j in range(3):
                sum = 0
                for k in range(3):
                    sum = sum + parent[i][k] * child[k][j]
                result[i][j] = sum
        result[3][0] = parent[3][0] + child[3][0]
        result[3][1] = parent[3][1] + child[3][1]
        result[3][2] = parent[3][2] + child[3][2]
        return result

    def processGeometry(self):
        #transform_tree = self.buildTransformTree(ldb)
        room_transform = {}
        for room in self.ldb.getRooms().rooms:
            if not self.progress_callback.updateProgressBar("Importing: Processing geometry"):
                break
            for static_mesh_id in room.static_meshes:
                if not self.progress_callback.updateProgressBar("Importing: Processing geometry"):
                    break
                static_mesh = self.ldb.getStaticMeshes().getById(static_mesh_id)
                self.groupAndTransform(self.createPolygons(static_mesh), static_mesh.transform)
                room_transform[room.id] = static_mesh.transform
        for room in self.ldb.getRooms().rooms:
            for dynamic_mesh_name in room.dynamic_meshes:
                if not self.progress_callback.updateProgressBar("Importing: Processing geometry"):
                    break
                dynamic_mesh =self.ldb.getDynamicMeshes().getBySharedName(dynamic_mesh_name)              
                self.groupAndTransform(self.createPolygons(dynamic_mesh), self.transformNodeWithParent(room_transform[dynamic_mesh.properties.room_id], dynamic_mesh.properties.object_to_room_transform))