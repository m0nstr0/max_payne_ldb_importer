import maya.OpenMayaMPx as OpenMayaMPx
import maya.api.OpenMaya as OpenMaya
import sys
import os
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
        file_name = Path(texture.name).stem
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
        amount = 20.0
        percent = 20.0 / (ldb.textures.numTextures() + ldb.textures.numLightmaps())
        MSG = "Importing: Processing textures"

        for texture in ldb.textures.textures:
            if not self.updateProgressBar(int(amount), MSG):
                break
            amount = amount + percent
            file_path = self.dumpTextureData(out_directory, texture)
            self.textures.append(file_path)

        for texture in ldb.textures.lightmaps:
            if not self.updateProgressBar(int(amount), MSG):
                break
            amount = amount + percent
            self.dumpTextureData(out_directory, texture)

    def endProgressBar(self):
        mc.progressWindow(endProgress=1)

    def updateProgressBar(self, amount, message):
        window_title = "Importing MaxPayne Level"
        if mc.progressWindow( query=True, isCancelled=True ):
            self.endProgressBar()
            mc.confirmDialog(message="File import was canceled")
            return False
        if amount == 0:
            mc.progressWindow(title=window_title,
					progress=amount,
					status=message,
					isInterruptable=True)
            return True
        if amount >= 100:
            self.endProgressBar()
            return True       
        mc.progressWindow(edit=True, progress=amount, status=message)
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
        amount = 40.0
        percent = 20.0 / ldb.materials.numMaterials()
        MSG = "Importing: Processing materials"

        self.materials.append([
            -1, 
            self.createMaterialNode("max_payne_mat_none", "", "")
        ])

        for material in ldb.materials.materials:
            if not self.updateProgressBar(int(amount), MSG):
                break
            amount = amount + percent

            material_name = "max_payne_mat_%i" % material.id          
            diffuse_texture = ""
            if material.diffuse_texture != None:
                diffuse_texture = self.textures[material.diffuse_texture.id]
            
            alpha_texture = ""
            if material.alpha_texture != None:
                alpha_texture = self.textures[material.alpha_texture.id]
            
            self.materials.append([
                material.id, 
                self.createMaterialNode(material_name, diffuse_texture, alpha_texture)
            ])

    def processGeometry(self, ldb):
        amount = 60.0
        num_polygons = 0

        for room in ldb.rooms.rooms:
            num_polygons = num_polygons + len(room.polygons)
        
        percent = 40.0 / num_polygons
        MSG = "Importing: Processing geometry"

        for room in ldb.rooms.rooms:
            if not self.updateProgressBar(int(amount), MSG):
                break
            objects_to_group = OpenMaya.MSelectionList()
            per_object_selection = OpenMaya.MSelectionList()
            for polygon in room.polygons:
                if not self.updateProgressBar(int(amount), MSG):
                    break
                amount = amount + percent
        
                indices = list(range(polygon.num_vertices))
                u = []
                v = []

                for uv in polygon.getGeometry().uvs:
                    u.append(uv[0])
                    v.append(1.0 - uv[1])
                
                new_mesh = OpenMaya.MFnMesh()
                new_mesh.create(map(lambda x: OpenMaya.MFloatPoint(-x[0] * 100.0, x[1] * 100.0, x[2] * 100.0), polygon.getGeometry().vertices), [polygon.num_vertices], indices, u, v)
                new_mesh.setVertexNormals(map(lambda x: OpenMaya.MVector(-x[0], x[1], x[2]), polygon.getGeometry().normals), indices)  
                new_mesh.assignUVs([polygon.num_vertices], indices)

                #apply material
                per_object_selection.clear()
                per_object_selection.add(new_mesh.getPath())
                OpenMaya.MGlobal.setActiveSelectionList(per_object_selection)
                found = False
                for material in self.materials:
                    if polygon.material.id == material[0]:
                        mc.hyperShade(assign=material[1])
                        found = True
                        break
                if not found:
                    mc.hyperShade(assign=material[0][0])
                objects_to_group.add(new_mesh.getPath())
            OpenMaya.MGlobal.setActiveSelectionList(objects_to_group)
            group = mc.group()
            mm = OpenMaya.MMatrix([
                room.transform[0] + [0.0], 
                room.transform[1] + [0.0], 
                room.transform[2] + [0.0], 
                room.transform[3] + [1.0]
            ])
            mm_transform = OpenMaya.MTransformationMatrix(mm)
            translation = mm_transform.translation(OpenMaya.MSpace.kWorld)
            rotation = mm_transform.rotation(asQuaternion=False)
            scale = mm_transform.scale(OpenMaya.MSpace.kWorld)
            mc.rotate(rotation[0], rotation[1], rotation[2], group, absolute=True)
            mc.move(-translation[0] * 100.0, translation[1] * 100.0, translation[2] * 100.0, group, absolute=True)
            mc.scale(scale[0], scale[1], scale[2], group, absolute=True)

    def processFile(self, directory_for_texures, file_path):
        ldb = max_ldb.MaxLDB(file_path)
        self.processTextures(directory_for_texures, ldb)
        self.processMaterials(ldb)
        self.processGeometry(ldb)

    def reader(self, file, options, mode):
        self.textures = []
        self.materials = []
        
        directory_for_texures = self.specifyDirectoryForTextures()

        if directory_for_texures == "":
            mc.confirmDialog(message="File import was canceled")
            return
        
        try:
            self.updateProgressBar(0, "Importing: Reading File")
            self.processFile(directory_for_texures, file.expandedFullName())
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