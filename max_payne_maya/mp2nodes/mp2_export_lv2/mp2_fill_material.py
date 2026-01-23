import maya.cmds as cmds
from pathlib import Path
from max_payne_sdk.lvl2.max_material import MaxMaterial
from max_payne_sdk.lvl2.max_material_category import MaxMaterialCategory
from max_payne_sdk.lvl2.max_texture import MaxTexture


def get_textures(attribute):
    nodes = cmds.listConnections(attribute, s=True, fnn=True)
    textures = []

    if nodes is None:
        return textures

    for node in nodes:
        if cmds.nodeType(node) != 'file':
            pass
        textures.append({node: cmds.getAttr(node + '.fileTextureName')})
    return textures


def get_texture_type(file_path):
    filename = Path(file_path)
    ext = filename.suffix.lower()
    if ext == ".tga":
        return 0
    if ext == ".scx":
        return 2
    if ext == ".pcx":
        return 3
    if ext == ".jpg":
        return 4
    if ext == ".dds":
        return 5


def fill_textures(lv2, textures, has_texture):
    for texture in textures:
        for k in texture:
            if k in has_texture:
                continue
            max_texture = MaxTexture()
            max_texture.name = k
            max_texture.type = get_texture_type(texture[k])
            with open(texture[k], 'rb') as file:
                max_texture.data = file.read()
                max_texture.size = len(max_texture.data)
                lv2.textures_and_materials.textures.append(max_texture)
            has_texture[k] = True

def fill_materials(lv2, materials):
    has_texture = {}
    material_categories = {}
    for material in materials:
        diffuse_texture = get_textures(material + '.color')
        diffuse_texture = diffuse_texture + get_textures(material + '.na_diffuseTextureAdditional')
        detail_texture = get_textures(material + '.na_detailTexture')
        reflection_texture = get_textures(material + '.na_reflectionTexture')
        gloss_texture = get_textures(material + '.na_glossTexture')
        light_layer_texture = get_textures(material + '.na_lightLayerTexture')

        fill_textures(lv2, diffuse_texture + detail_texture + reflection_texture + gloss_texture + light_layer_texture, has_texture)

        category = cmds.getAttr(material + '.na_category')
        max_category = None
        if category not in material_categories:
            max_category = MaxMaterialCategory()
            max_category.category_name = category
            lv2.textures_and_materials.categories.append(max_category)
            material_categories[category] = max_category
        else:
            max_category = material_categories[category]

        max_material = MaxMaterial()
        max_material.material_name = material

        max_material.detail_texture = ''
        max_material.diffuse_textures = []
        max_material.light_layer_texture = ''
        max_material.reflection_texture = ''
        max_material.gloss_texture = ''

        for tex in diffuse_texture:
            for k in tex:
                max_material.diffuse_textures.append(k)
        max_material.num_frames = len(max_material.diffuse_textures)

        for tex in light_layer_texture:
            for k in tex:
                max_material.light_layer_texture = k

        for tex in detail_texture:
            for k in tex:
                max_material.detail_texture = k

        for tex in reflection_texture:
            for k in tex:
                max_material.reflection_texture = k

        for tex in gloss_texture:
            for k in tex:
                max_material.gloss_texture = k

        max_material.has_reflection_texture = True if len(reflection_texture) > 0 else False
        max_material.has_gloss_texture = True if len(gloss_texture) > 0 else False

        max_material.diffuse_default_width = cmds.getAttr(material + '.na_diffuseTextureWidth')
        max_material.diffuse_default_height = cmds.getAttr(material + '.na_diffuseTextureHeight')
        max_material.light_layer_default_width = cmds.getAttr(material + '.na_lightLayerWidth')
        max_material.light_layer_default_height = cmds.getAttr(material + '.na_lightLayerHeight')
        max_material.detail_texture_default_scale = cmds.getAttr(material + '.na_detailTextureScale')
        max_material.dual_sided = cmds.getAttr(material + '.na_dualSided')
        max_material.alpha_reference_value = cmds.getAttr(material + '.na_alphaCompareReferenceValue')
        max_material.adult_content = cmds.getAttr(material + '.na_adultContent')
        max_material.mode = cmds.getAttr(material + '.na_textureMode')
        max_material.alpha_compare_edge_blend = cmds.getAttr(material + '.na_alphaEdgeBlend')
        max_material.active_frame = cmds.getAttr(material + '.na_activeFrame')
        max_material.framerate = cmds.getAttr(material + '.na_framerate')

        max_category.materials.append(max_material)
