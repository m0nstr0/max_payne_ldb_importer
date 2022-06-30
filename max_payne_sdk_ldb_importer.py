from cProfile import label
import maya.OpenMayaMPx as OpenMayaMPx
import maya.api.OpenMaya as OpenMaya
import sys
import os
import math
import max_payne_sdk.max_ldb as max_ldb 
import maya.cmds as mc
from pathlib import Path
from PIL import Image

PLUGIN_NAME = "Max Payne LDB Import"
PLUGIN_COMPANY = "Bolotaev Sergey"
FILE_EXT = 'ldb'

class MaxPayneSDKTranslator( OpenMayaMPx.MPxFileTranslator ):
    def __init__(self):
        OpenMayaMPx.MPxFileTranslator.__init__(self)
        self.kwargs = {}
        self.textures = []
        self.materials = []

    def haveWriteMethod(self):
        return False

    def haveReadMethod(self):
        return True

    def filter(self):
        return "*.{}".format(FILE_EXT)

    def defaultExtension(self):
        return FILE_EXT

    def identifyFile (self, file_obj, buffer, size):
        return OpenMayaMPx.MPxFileTranslator.kIsMyFileType

    def specifyDirectoryForTextures(self):
        directory_path = mc.fileDialog2(
            caption="Set texture folder",
            dialogStyle=1,
            fileMode=3
        )
        if directory_path != None and directory_path != "":
            return str(directory_path[0])
        return ""

    def genUniqFileName(self, directory, in_file_name, ext):
        file_name = in_file_name
        i = 0
        while os.path.exists(os.path.join(directory, file_name + ext)):
            file_name = file_name + str(i)
            i = i + 1
        return file_name

    def dumpTextureData(self, out_directory, texture):
        file_name = Path(texture.file_path).stem
        ext = "." + texture.getFileTypeName()
        o_file_name = self.genUniqFileName(out_directory, file_name, ext)
        o_file_path = os.path.join(out_directory, o_file_name + ext)
        try:
            with open(o_file_path, "wb") as f:
                f.write(texture.data)
        except IOError:
            sys.stderr.write("Error While Opening the file! %s" % o_file_path)
            raise

        if texture.getFileTypeName() == "pcx":
            o_file_path = self.convertTextureData(out_directory, o_file_path, o_file_name)

        if texture.getFileTypeName() == "scx":
            sys.stdout.write("The level contains scx file. This format is not supported. Empty material will be used")
            return None

        return o_file_path

    def convertTextureData(self, out_directory, file_path, file_name):
        o_file_name = self.genUniqFileName(out_directory, file_name, ".png")
        o_file_path = os.path.join(out_directory, o_file_name + ".png")
        try:
            with Image.open(file_path) as im:
                im.save(o_file_path)
        except OSError:
            sys.stderr.write("Error While Converting the file! %s to png" % file_path)
            raise

    def processTextures(self, out_directory, ldb):
        MSG = "Importing: Processing textures"
        for texture in ldb.getTextures().textures:
            if not self.updateProgressBar(MSG):
                break
            file_path = self.dumpTextureData(out_directory, texture)
            self.textures[texture.file_path] = file_path

        for texture in ldb.getLightMaps().textures:
            if not self.updateProgressBar(MSG):
                break
            #self.dumpTextureData(out_directory, texture)

    def endProgressBar(self):
        mc.progressWindow(endProgress=1)

    def updateProgressBar(self, message):
        self.progress_amount = self.progress_amount + self.progress_delta
        window_title = "Importing MaxPayne Level"
        if mc.progressWindow( query=True, isCancelled=True ):
            self.endProgressBar()
            mc.confirmDialog(message="File import was canceled")
            return False
        if self.progress_amount == 0:
            mc.progressWindow(title=window_title,
					progress=0,
					status=message,
					isInterruptable=True)
            return True
        if self.progress_amount >= 100:
            self.endProgressBar()
            return True       
        mc.progressWindow(edit=True, progress=self.progress_amount, status=message)
        return True

    def createMaterialNode(self, material_name, diffuse_file_path, alpha_file_path):
        shader = mc.shadingNode("lambert", asShader=True, name=material_name)
        shading_group = mc.sets(renderable=True,noSurfaceShader=True,empty=True)
        mc.connectAttr("%s.outColor" % shader ,"%s.surfaceShader" % shading_group)

        if diffuse_file_path != "":
            diffuse_file_node = mc.shadingNode("file", asTexture=True, name=material_name + "_diffuse")
            mc.setAttr("%s.fileTextureName" % diffuse_file_node, diffuse_file_path, type="string")
            mc.connectAttr("%s.outColor" % diffuse_file_node, "%s.color" % shader)

        alpha_file_node = ""
        if alpha_file_path != "":
            alpha_file_node = mc.shadingNode("file", asTexture=True, name=material_name + "_alpha")
            mc.setAttr("%s.fileTextureName" % alpha_file_node, alpha_file_path, type="string")
            mc.connectAttr("%s.outColor" % alpha_file_node, "%s.transparency" % shader)

        return shader

    def processMaterials(self, ldb):
        self.empty_material = self.createMaterialNode("max_payne_mat_none", "", "")
        for material in ldb.getMaterials().materials:
            if not self.updateProgressBar("Importing: Processing materials"):
                break

            material_name = "max_payne_mat_%i" % material.id          
            diffuse_texture = ""
            if material.diffuse_texture != None:
                diffuse_texture = self.textures[material.diffuse_texture.file_path]
            
            alpha_texture = ""
            if material.alpha_texture != None:
                alpha_texture = self.textures[material.alpha_texture.file_path]
            
            self.materials.append([
                material.id, 
                self.createMaterialNode(material_name, diffuse_texture, alpha_texture)
            ])

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
            uniq_vertices = []
            uniq_uvs = []
            uvs_indices_poly = []
            poly_indices = []
            poly_nums_points = []
            selection = OpenMaya.MSelectionList()
            normals_per_poly = {}
            poly_id = -1
            for geometry in geometries:
                if not self.updateProgressBar("Importing: Processing geometry"):
                    break
                poly_id = poly_id + 1
                poly_nums_points.append(len(geometry.vertices))
                normals_per_poly[poly_id] = []
                for i in range(len(geometry.vertices)):
                    found = False
                    for j in range(len(uniq_vertices)):
                        if math.isclose(uniq_vertices[j].x, -geometry.vertices[i].x * 100.0):
                            if math.isclose(uniq_vertices[j].y, geometry.vertices[i].y * 100.0):
                                if math.isclose(uniq_vertices[j].z, geometry.vertices[i].z * 100.0):
                                    found = True
                                    poly_indices.append(j)
                                    break
                    if not found:
                        uniq_vertices.append(OpenMaya.MFloatPoint(-geometry.vertices[i].x * 100.0, geometry.vertices[i].y * 100.0, geometry.vertices[i].z * 100.0))
                        poly_indices.append(len(uniq_vertices) - 1)
                    normals_per_poly[poly_id].append([poly_indices[-1], OpenMaya.MVector(-geometry.normals[i].x, geometry.normals[i].y, geometry.normals[i].z)])

                for i in range(len(geometry.uv)):
                    found = False
                    for j in range(len(uniq_uvs)):
                        if math.isclose(uniq_uvs[j].u, geometry.uv[i].u):
                            if math.isclose(uniq_uvs[j].v, geometry.uv[i].v):
                                found = True
                                uvs_indices_poly.append(j)
                                break
                    if not found:
                        uniq_uvs.append(geometry.uv[i])
                        uvs_indices_poly.append(len(uniq_uvs) - 1)
            new_mesh = OpenMaya.MFnMesh()
            us = list(map(lambda uv: uv.u, uniq_uvs))
            vs = list(map(lambda uv: 1.0 - uv.v, uniq_uvs))
            new_mesh.create(uniq_vertices, poly_nums_points, poly_indices, us, vs)
            new_mesh.assignUVs(poly_nums_points, uvs_indices_poly)

            for poly_id, normal_vertex in normals_per_poly.items():
                for element in normal_vertex:
                    print(element[1], poly_id, element[0])
                    new_mesh.setFaceVertexNormal(element[1], poly_id, element[0])

            selection.add(new_mesh.getPath())
            group_up.add(new_mesh.getPath())
            OpenMaya.MGlobal.setActiveSelectionList(selection)
            found = False
            for material in self.materials:
                if material_id == material[0]:
                    mc.hyperShade(assign=material[1])
                    found = True
                    break
            if not found:
                mc.hyperShade(assign=self.empty_material)
            new_mesh.updateSurface()       
        return group_up

    def groupAndTransform(self, group_up, transfrom):
        matrix = OpenMaya.MMatrix([
            transfrom[0] + [0.0], 
            transfrom[1] + [0.0], 
            transfrom[2] + [0.0], 
            transfrom[3] + [1.0]
        ])
        OpenMaya.MGlobal.setActiveSelectionList(group_up)
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
        result = [x[:] for x in child]
        #result = self.invRotationMatrix(result)
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

    def buildTransformTree(self, ldb):
        room_transfoms = {}
        transform_tree = {}
        for room in ldb.getRooms().rooms:
            for static_mesh_id in room.static_meshes:
                static_mesh = ldb.getStaticMeshes().getById(static_mesh_id)
                room_transfoms[room.id] = static_mesh.transform
            for dynamic_mesh_name in room.dynamic_meshes:
                dynamic_mesh = ldb.getDynamicMeshes().getBySharedName(dynamic_mesh_name)

                transforms = [[x[:] for x in dynamic_mesh.transform]]
                parent_mesh = dynamic_mesh
                while (parent_mesh.properties.parent_dynamic_mesh_name != ""):
                    parent_mesh = ldb.getDynamicMeshes().getBySharedName(parent_mesh.properties.parent_dynamic_mesh_name)
                    transforms.append([x[:] for x in parent_mesh.transform])

                transform = [x[:] for x in room_transfoms[room.id]]
                for i in range(len(transforms) - 1, -1, -1):
                    transform = self.transformNodeWithParent(transform, transforms[i])
                transform_tree[dynamic_mesh.shared_name] = [x[:] for x in transform]
        return transform_tree

    def processGeometry(self, ldb):
        MSG = "Importing: Processing geometry"
        transform_tree = self.buildTransformTree(ldb)
        for room in ldb.getRooms().rooms:
            if not self.updateProgressBar(MSG):
                break
            for static_mesh_id in room.static_meshes:
                if not self.updateProgressBar(MSG):
                    break
                static_mesh = ldb.getStaticMeshes().getById(static_mesh_id)
                self.groupAndTransform(self.createPolygons(static_mesh), static_mesh.transform)
            for dynamic_mesh_name in room.dynamic_meshes:
                if not self.updateProgressBar(MSG):
                    break
                dynamic_mesh = ldb.getDynamicMeshes().getBySharedName(dynamic_mesh_name)
                transform = transform_tree[dynamic_mesh_name]
                self.groupAndTransform(self.createPolygons(dynamic_mesh), transform)

    def processFile(self, directory_for_texures, ldb):
        self.processTextures(directory_for_texures, ldb)
        self.processMaterials(ldb)
        self.processGeometry(ldb)

    def calculateItems(self, ldb):
        num_textures = len(ldb.getTextures().textures)
        num_lightmap_textures = len(ldb.getLightMaps().textures)
        num_materials = len(ldb.getMaterials().materials)
        num_static_mesh_polygons = 0
        num_rooms = len(ldb.getRooms().rooms)
        for static_mesh in ldb.getStaticMeshes().static_meshes:
            num_static_mesh_polygons = num_static_mesh_polygons + len(static_mesh.polygons.polygons)
        num_dynamic_mesh_polygons = 0
        for dynamic_mesh in ldb.getDynamicMeshes().dynamic_meshes:
            num_dynamic_mesh_polygons = num_dynamic_mesh_polygons + len(dynamic_mesh.polygons.polygons)
        return num_materials + num_textures + num_lightmap_textures + num_static_mesh_polygons + num_dynamic_mesh_polygons + num_rooms

    def reader(self, file, options, mode):
        self.textures = {}
        self.materials = []
        self.empty_material = None
        self.progress_amount = 0
        self.progress_delta = 0

        directory_for_texures = self.specifyDirectoryForTextures()

        if directory_for_texures == "":
            mc.confirmDialog(message="File import was canceled")
            return
        
        try:
            self.updateProgressBar("Importing: Reading File")
            ldb = max_ldb.MaxLDBReader().parse(file.expandedFullName())
            num_items = self.calculateItems(ldb)
            self.progress_delta = 100.0 / num_items
            self.processFile(directory_for_texures, ldb)
        except Exception:
            sys.stderr.write("Failed to import file: %s" % file.expandedFullName())
            mc.confirmDialog(message="Failed to import file: %s" % file.expandedFullName())
            self.endProgressBar()
            raise

        self.endProgressBar()
        mc.confirmDialog(message="File was imported")

def createMaxPayneSDKTranslator():
    return OpenMayaMPx.asMPxPtr( MaxPayneSDKTranslator() )

def initializePlugin( mobject ):
    mplugin = OpenMayaMPx.MFnPlugin(mobject, PLUGIN_COMPANY, '1.0', "Any")
    try:
        mplugin.registerFileTranslator( PLUGIN_NAME, None, createMaxPayneSDKTranslator)
    except:
        sys.stderr.write( "Failed to register translator: %s" % PLUGIN_NAME )
        raise

def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterFileTranslator( PLUGIN_NAME )
    except:
        sys.stderr.write( "Failed to deregister translator: %s" % PLUGIN_NAME )
        raise