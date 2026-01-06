import max_payne_sdk.max_ldb as mp
import json

from max_payne_sdk.lvl2.max_header import packString, packInt
from max_payne_sdk.lvl2.max_lvl2 import MaxLVL2
from max_payne_sdk.lvl2.max_material import MaxMaterial
from max_payne_sdk.lvl2.max_material_category import MaxMaterialCategory
from max_payne_sdk.lvl2.max_texture import MaxTexture

lvl2 = MaxLVL2()
lvl2.textures_and_materials.textures.append(MaxTexture())
lvl2.textures_and_materials.textures[0].name = 'Images\default_material.dds'

lvl2.textures_and_materials.categories.append(MaxMaterialCategory())
lvl2.textures_and_materials.categories[0].category_name = 'Default'
lvl2.textures_and_materials.categories[0].materials = [MaxMaterial()]
lvl2.textures_and_materials.categories[0].materials[0].material_name = 'Images\default_material.dds'
lvl2.textures_and_materials.categories[0].materials[0].num_frames = 1
lvl2.textures_and_materials.categories[0].materials[0].diffuse_textures = ['Images\default_material.dds']

with open('default_texture.dds', 'rb') as file:
    tex_data = file.read()
    #tex_data = list(tex_data)

lvl2.textures_and_materials.textures[0].data = tex_data
lvl2.textures_and_materials.textures[0].size = len(tex_data)

bytes = lvl2.getBytes()

with open('test_out.lv2', 'wb') as file:
    for i in bytes:
        file.write(i)
