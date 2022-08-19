import maya.cmds as mc
import os
from pathlib import Path
from PIL import Image
from PIL import ImageChops
import sys

class MayaLDBMaterialOps:
    def __init__(self, ldb, texture_directory, progress_callback) -> None:
        self.ldb = ldb
        self.empty_material = self.createMaterialNode("max_payne_mat_none", "", "")
        self.textures = {}
        self.materials = []
        self.texture_directory = texture_directory
        self.progress_callback = progress_callback
        self.processMaterials()

    def getMaterialNameById(self, id):
        for material in self.materials:
            if id == material[0]:
                return material[1]
        return self.empty_material

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

    def getUniqueFileNameAndPath(self, base_file_name, ext):
        file_name = base_file_name
        i = 0
        while os.path.exists(os.path.join(self.texture_directory, file_name + '.' + ext)):
            file_name = file_name + str(i)
            i = i + 1
        return (file_name, os.path.join(self.texture_directory, file_name + "." + ext))

    def getTextureFileName(self, texture, is_alpha = False):
        if texture == None:
            return ""
        if texture.file_path in self.textures:
            return self.textures[texture.file_path]
        return self.dumpTextureData(texture, is_alpha)

    def processMaterials(self):
        for material in self.ldb.getMaterials().materials:
            if not self.progress_callback.updateProgressBar("Importing: Processing materials"):
                break

            material_name = "max_payne_mat_%i" % material.id          
            diffuse_texture = self.getTextureFileName(material.diffuse_texture)
            
            alpha_texture = ""
            if material.alpha_texture != None:
                alpha_texture = self.getTextureFileName(material.alpha_texture, True)
            
            self.materials.append([
                material.id, 
                self.createMaterialNode(material_name, diffuse_texture, alpha_texture)
            ])

    def dumpTextureData(self, texture, is_alpha = False):
        file_name, file_path = self.getUniqueFileNameAndPath(Path(texture.file_path).stem, texture.getFileTypeName())
        try:
            with open(file_path, "wb") as f:
                f.write(texture.data)
        except IOError:
            sys.stderr.write("Error opening file %s for reading" % file_path)
            raise

        if texture.getFileTypeName() == "pcx":
            try:
                with Image.open(file_path) as im:
                    file_name, file_path = self.getUniqueFileNameAndPath(file_name, 'png')
                    im.save(file_path)
            except OSError:
                sys.stderr.write("Error converting file %s to png" % file_path)
                raise

        if texture.getFileTypeName() == "scx":
            sys.stdout.write("The level contains scx file. This format is not supported. Empty material_reader will be used")
            return ""

        if is_alpha == True:
            try:
                with Image.open(file_path) as im:
                    file_name, file_path = self.getUniqueFileNameAndPath(file_name + "_inverted", 'png')
                    inv_img = ImageChops.invert(im)
                    inv_img.save(file_path)
            except OSError:
                sys.stderr.write("Error converting file %s to png" % file_path)
                raise

        self.textures[texture.file_path] = file_path
        return file_path