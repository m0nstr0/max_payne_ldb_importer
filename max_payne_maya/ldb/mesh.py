import maya.cmds as mc
import maya.api.OpenMaya as OpenMaya
import math

import max_payne_maya.progress_bar as progress_bar
from max_payne_maya.ldb import MayaLDBProxy
from max_payne_maya.ldb.ldb_proxy import MayaStaticMeshProxy
from max_payne_maya.ldb.max_math import transformNodeWithParent


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

    def groupAndTransform(self, group_up, transform, pivot_point):
        matrix = OpenMaya.MMatrix([
            transform[0] + [0.0],
            transform[1] + [0.0],
            transform[2] + [0.0],
            transform[3] + [1.0]
        ])
        OpenMaya.MGlobal.setActiveSelectionList(group_up)
        group = mc.listRelatives(mc.ls(selection=True), parent=True, fullPath=False)[0]
        if group_up.length() > 1:
            group = mc.group()
        mc.setAttr(group + ".scalePivot", pivot_point[0] * 100, -pivot_point[1] * 100, -pivot_point[2] * 100)
        mc.setAttr(group + ".rotatePivot", pivot_point[0] * 100, -pivot_point[1] * 100, -pivot_point[2] * 100)
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

    def processGeometry(self):
        room_transform = {}
        progress_bar.set_message("Importing: Processing geometry")
        for room_id in range(self.ldb.getRoomsNum()):
            if not progress_bar.update():
                break
            mesh = self.ldb.getStaticMeshByRoomId(room_id)
            self.groupAndTransform(self.createPolygons(mesh), mesh.transform, mesh.pivot)
            room_transform[room_id] = mesh.transform
        for room_id in range(self.ldb.getRoomsNum()):
            if not progress_bar.update():
                break
            for dynamic_mesh_id in range(self.ldb.getDynamicMeshesNumByRoomId(room_id)):
                if not progress_bar.update():
                    break
                mesh = self.ldb.getDynamicMeshByIdAndRoomId(room_id, dynamic_mesh_id)
                if mesh.use_room_transform:
                    self.groupAndTransform(self.createPolygons(mesh), transformNodeWithParent(room_transform[room_id], mesh.transform), mesh.pivot)
                else:
                    self.groupAndTransform(self.createPolygons(mesh), mesh.transform, mesh.pivot)
