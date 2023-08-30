import maya.cmds as mc
import os
from pathlib import Path
from PIL import Image
import sys
import max_payne_maya.progress_bar as progress_bar

from max_payne_maya.ldb.ldb_proxy import MayaTextureProxy, MayaLDBProxy, MayaMaterialProxy

__TEXTURES_CACHE__ = {}

def createHyperShadeGraph(material_proxy: MayaMaterialProxy, diffuse_texture_path: str, alpha_texture_path: str,
                          reflection_texture_path: str, gloss_texture_path: str, detail_texture_path: str) -> str:

    shader = mc.shadingNode("lambert", asShader=True, name=material_proxy.name)
    shading_group = mc.sets(renderable=True, noSurfaceShader=True, empty=True)
    mc.connectAttr("%s.outColor" % shader, "%s.surfaceShader" % shading_group)

    if diffuse_texture_path != "":
        diffuse_node = mc.shadingNode("file", asTexture=True, name=material_proxy.name + "_diffuse")
        mc.setAttr("%s.fileTextureName" % diffuse_node, diffuse_texture_path, type="string")
        mc.connectAttr("%s.outColor" % diffuse_node, "%s.color" % shader)
        if material_proxy.properties is not None and material_proxy.properties.use_alpha_channel:
            mc.connectAttr("%s.outTransparency" % diffuse_node, "%s.transparency" % shader)

    if alpha_texture_path != "":
        alpha_node = mc.shadingNode("file", asTexture=True, name=material_proxy.name + "_alpha")
        mc.setAttr("%s.fileTextureName" % alpha_node, alpha_texture_path, type="string")
        mc.setAttr("%s.invert" % alpha_node, 1)
        mc.connectAttr("%s.outColor" % alpha_node, "%s.transparency" % shader)

    if reflection_texture_path != "":
        reflection_node = mc.shadingNode("file", asTexture=True, name=material_proxy.name + "_reflection")
        mc.setAttr("%s.fileTextureName" % reflection_node, reflection_texture_path, type="string")
        # mc.connectAttr("%s.outColor" % reflection_node, "%s.color" % shader)

    if gloss_texture_path != "":
        gloss_node = mc.shadingNode("file", asTexture=True, name=material_proxy.name + "_gloss")
        mc.setAttr("%s.fileTextureName" % gloss_node, gloss_texture_path, type="string")
        # mc.connectAttr("%s.outColor" % gloss_node, "%s.color" % shader)

    if detail_texture_path != "":
        detail_node = mc.shadingNode("file", asTexture=True, name=material_proxy.name + "_detail")
        mc.setAttr("%s.fileTextureName" % detail_node, detail_texture_path, type="string")
        # mc.connectAttr("%s.outColor" % detail_node, "%s.color" % shader)

    return shader


def getUniqueFileNameAndPath(texture_directory: str, base_file_name: str, ext: str):
    file_name = base_file_name
    i = 0
    while os.path.exists(os.path.join(texture_directory, file_name + '.' + ext)):
        file_name = file_name + str(i)
        i = i + 1
    return file_name, os.path.join(texture_directory, file_name + "." + ext)


def dumpTextureData(texture_directory: str, texture_proxy: MayaTextureProxy) -> str:
    global __TEXTURES_CACHE__

    if texture_proxy.file_path in __TEXTURES_CACHE__:
        return __TEXTURES_CACHE__[texture_proxy.file_path]

    file_name, file_path = getUniqueFileNameAndPath(texture_directory,
                                                    Path(texture_proxy.file_path).stem,
                                                    texture_proxy.file_type_name)
    try:
        with open(file_path, "wb") as f:
            f.write(texture_proxy.data)
    except IOError:
        sys.stderr.write("Error opening file %s for reading" % file_path)
        raise

    if texture_proxy.file_type_name == "pcx":
        try:
            with Image.open(file_path) as im:
                file_name, file_path = getUniqueFileNameAndPath(texture_directory, file_name, 'png')
                im.save(file_path)
        except OSError:
            sys.stderr.write("Error converting file %s to png" % file_path)
            raise

    if texture_proxy.file_type_name == "scx":
        sys.stdout.write(
            "The level contains scx file. This format is not supported. Empty material_reader will be used")
        return ""

    __TEXTURES_CACHE__[texture_proxy.file_path] = file_path

    return file_path


def processMaterials(ldb_proxy: MayaLDBProxy, texture_directory: str) -> {}:
    global __TEXTURES_CACHE__
    __TEXTURES_CACHE__ = {}

    materials_dict = {}
    progress_bar.set_message("Importing: Processing materials")
    for material in ldb_proxy.getMaterials():
        if not progress_bar.update():
            break

        diffuse_texture_path: str = ""
        alpha_texture_path: str = ""
        reflection_texture_path: str = ""
        gloss_texture_path: str = ""
        detail_texture_path: str = ""

        if material.diffuse_texture is not None:
            diffuse_texture_path = dumpTextureData(texture_directory, material.diffuse_texture)
        if material.alpha_texture is not None:
            alpha_texture_path = dumpTextureData(texture_directory, material.alpha_texture)
        if material.reflection_texture is not None:
            reflection_texture_path = dumpTextureData(texture_directory, material.reflection_texture)
        if material.gloss_texture is not None:
            gloss_texture_path = dumpTextureData(texture_directory, material.gloss_texture)
        if material.detail_texture is not None:
            detail_texture_path = dumpTextureData(texture_directory, material.detail_texture)

        shader = createHyperShadeGraph(material,
                              diffuse_texture_path,
                              alpha_texture_path,
                              reflection_texture_path,
                              gloss_texture_path,
                              detail_texture_path)

        materials_dict[material.id] = shader

    __TEXTURES_CACHE__ = {}
    return materials_dict