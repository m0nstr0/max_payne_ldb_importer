import maya.cmds as mc
import sys
import maya.OpenMayaMPx as OpenMayaMPx
import maya.api.OpenMaya as OpenMaya
import math

import max_payne_maya.progress_bar as progress_bar
from max_payne_maya.ldb import MayaLDBProxy
from max_payne_maya.ldb.ldb_proxy import MayaStaticMeshProxy

class MayaLDBMeshlOps:
    def __init__(self, ldb: MayaLDBProxy, materials) -> None:
        self.ldb = ldb
        self.materials = materials

    def createPolygons(self, mesh: MayaStaticMeshProxy):
        new_mesh = OpenMaya.MFnMesh()
        new_mesh.create(mesh.vertices, mesh.vertices_per_poly, mesh.indices, mesh.us, mesh.vs)
        new_mesh.setVertexNormals(mesh.normals, range(len(mesh.vertices)))
        new_mesh.assignUVs(mesh.vertices_per_poly, mesh.indices)
        for material_id, polygons in mesh.materials.items():
            mc.select(clear = True)
            for polygon_id in polygons:
                mc.select('%s.f[%i]' % (new_mesh.name(), polygon_id), add = True)
            mc.hyperShade(assign = self.materials[material_id])
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
        room_transform = {}
        progress_bar.set_message("Importing: Processing geometry")
        for room_id in range(self.ldb.getRoomsNum()):
            if not progress_bar.update():
                break
            mesh = self.ldb.getStaticMeshByRoomId(room_id)
            self.groupAndTransform(self.createPolygons(mesh), mesh.transform)
            room_transform[room_id] = mesh.transform
        for room_id in range(self.ldb.getRoomsNum()):
            if not progress_bar.update():
                break
            for dynamic_mesh_id in range(self.ldb.getDynamicMeshesNumByRoomId(room_id)):
                if not progress_bar.update():
                    break
                mesh = self.ldb.getDynamicMeshByIdAndRoomId(room_id, dynamic_mesh_id)
                self.groupAndTransform(self.createPolygons(mesh), self.transformNodeWithParent(room_transform[room_id], mesh.transform))