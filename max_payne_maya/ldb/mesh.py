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

    def generateUniqVerticesList(self, vertices, normals, uniq_vertices, poly_indices, poly_num_points, normals_per_poly):
        poly_num_points.append(len(vertices))
        for i in range(len(vertices)):
            found = False
            for j in range(len(uniq_vertices)):
                if not math.isclose(uniq_vertices[j].x, -vertices[i].x * 100.0):
                    continue
                if not math.isclose(uniq_vertices[j].y, vertices[i].y * 100.0):
                    continue
                if not math.isclose(uniq_vertices[j].z, vertices[i].z * 100.0):
                    continue
                found = True
                poly_indices.append(j)
                break
            if not found:
                uniq_vertices.append(OpenMaya.MFloatPoint(-vertices[i].x * 100.0, vertices[i].y * 100.0, vertices[i].z * 100.0))
                poly_indices.append(len(uniq_vertices) - 1)
            normals_per_poly.append([poly_indices[-1], OpenMaya.MVector(-normals[i].x, normals[i].y, normals[i].z)])

    def generateUniqUVList(self, uvs, us, vs, poly_uv_indices):
        for uv in uvs:
            found = False
            for j in range(len(us)):
                if not math.isclose(us[j], uv.u):
                    continue
                if not math.isclose(vs[j], 1.0 - uv.v):
                    continue
                found = True
                poly_uv_indices.append(j)
                break
            if not found:
                us.append(uv.u)
                vs.append(1.0 - uv.v)
                poly_uv_indices.append(len(us) - 1)

    def createPolygons(self, mesh):
        group_up = OpenMaya.MSelectionList()
        grouped_by_materials = {}
        for polygon_idx in range(mesh.numPolygons()):
            geometry = mesh.constructPolygon(polygon_idx)
            if geometry.material.id in grouped_by_materials:
                grouped_by_materials[geometry.material.id].append(geometry)
            else:
                grouped_by_materials[geometry.material.id] = [geometry]
        for material_id, geometries in grouped_by_materials.items():
            selection = OpenMaya.MSelectionList()
            poly_id = -1
            normals_per_poly = {}
            uniq_vertices = []
            poly_indices = []
            poly_num_points = []
            us = []
            vs = []
            poly_uv_indices = []
            for geometry in geometries:
                if not self.progress_callback.updateProgressBar("Importing: Processing geometry"):
                    break
                poly_id = poly_id + 1
                normals_per_poly[poly_id] = []
                self.generateUniqVerticesList(geometry.vertices, geometry.normals, uniq_vertices, poly_indices, poly_num_points, normals_per_poly[poly_id])
                self.generateUniqUVList(geometry.uv, us, vs, poly_uv_indices)
            new_mesh = OpenMaya.MFnMesh()
            new_mesh.create(uniq_vertices, poly_num_points, poly_indices, us, vs)
            new_mesh.assignUVs(poly_num_points, poly_uv_indices)
            for poly_id, normal_vertex in normals_per_poly.items():
                for element in normal_vertex:
                    new_mesh.setFaceVertexNormal(element[1], poly_id, element[0])
            selection.add(new_mesh.getPath())
            OpenMaya.MGlobal.setActiveSelectionList(selection)
            mc.hyperShade(assign=self.materials.getMaterialNameById(material_id))
            new_mesh.updateSurface()       
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
            for dynamic_mesh_name in room.dynamic_meshes:
                if not self.progress_callback.updateProgressBar("Importing: Processing geometry"):
                    break
                dynamic_mesh =self.ldb.getDynamicMeshes().getBySharedName(dynamic_mesh_name)              
                self.groupAndTransform(self.createPolygons(dynamic_mesh), self.transformNodeWithParent(room_transform[dynamic_mesh.properties.room_id], dynamic_mesh.properties.object_to_room_transform))