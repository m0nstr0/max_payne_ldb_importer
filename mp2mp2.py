import max_payne_sdk.max_ldb as mp
import json

from max_payne_sdk.lvl2.max_header import packString, packInt
from max_payne_sdk.lvl2.max_lvl2 import MaxLVL2
from max_payne_sdk.lvl2.max_material import MaxMaterial
from max_payne_sdk.lvl2.max_material_category import MaxMaterialCategory
from max_payne_sdk.lvl2.max_node_mesh import MaxNodeMeshPolygon, MaxNodeMeshTriangle, MaxNodeMesh
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

wp_node = lvl2.createNodeWaypoint()
lvl2.node.children.append(wp_node)

ain_node = lvl2.createNodeAin()
lvl2.node.children.append(ain_node)

jmp_node = lvl2.createNodeJumpPoint()
lvl2.node.children.append(jmp_node)

fsm_node = lvl2.createNodeFSM()
lvl2.node.children.append(fsm_node)

lvi_node = lvl2.createNodeLevelItem()
lvi_node.item_type = 'Ammo_Beretta'
lvl2.node.children.append(lvi_node)

fl_node = lvl2.createNodeFlare()
fl_node.flare_name = 'flare02_directional'
lvl2.node.children.append(fl_node)

en_node = lvl2.createNodeEnemy()
en_node.enemy_skin = 'C04_BlackOps_C'
en_node.activator_use_animation = 'Default'
lvl2.node.children.append(en_node)

tr_node = lvl2.createNodeTrigger()
tr_node.shared_db_name= 'test'
tr_node.activator_use_animation = 'Default'
lvl2.node.children.append(tr_node)

dpl_node = lvl2.createNodeDynamicPointLight()
lvl2.node.children.append(dpl_node)

with open('default_texture.dds', 'rb') as file:
    tex_data = file.read()
    #tex_data = list(tex_data)

lvl2.textures_and_materials.textures[0].data = tex_data
lvl2.textures_and_materials.textures[0].size = len(tex_data)


mesh_node = lvl2.createNodeMesh()
lvl2.node.children.append(mesh_node)

mesh_node.vertices = [[0.0, 0.0, 0.0], [0.0, 0.0, 1.0], [1.0, 0.0, 1.0], [1.0, 0.0, 0.0]]

triangle = MaxNodeMeshTriangle()
triangle.normal = [0.0, 1.0, 0.0]
triangle.indices = [0, 1, 2, 3]

mesh_polygon = MaxNodeMeshPolygon()
mesh_polygon.normal = [0.0, 1.0, 0.0]
mesh_polygon.normal2unknown = [0.0, 1.0, 0.0]
mesh_polygon.point_on_plane = [0.0, 0.0, 0.0]
mesh_polygon.triangles = [triangle]
mesh_polygon.edges = [[0, 1], [1, 2], [2, 3], [3, 0]]
mesh_polygon.exit_id = -1

mesh_polygon.material_name = 'Images\default_material.dds'
mesh_polygon.material_category = 'Default'

mesh_node.polygons = [mesh_polygon]


bytes = lvl2.getBytes()
with open('test_out.lv2', 'wb') as file:
    for i in bytes:
        file.write(i)
