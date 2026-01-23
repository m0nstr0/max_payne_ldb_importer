import math

import maya.cmds as cmds
import maya.mel as mel

from max_payne_maya.mp2nodes.mp2_export_lv2.mp2_fill_material import fill_materials
from max_payne_maya.mp2nodes.mp2_export_lv2.mp2_fill_node import fill_node_base_data, fill_node_with_data
from max_payne_maya.mp2nodes.mp2_node_ids import MP2_WORLD_GROUP_NODE_NAME, MP2_JUMP_POINT_NODE_NAME, \
    MP2_WAY_POINT_NODE_NAME, MP2_AIN_NODE_NAME, MP2_LEVEL_ITEM_NODE_NAME, MP2_ENEMY_NODE_NAME, MP2_TRIGGER_NODE_NAME, \
    MP2_FSM_NODE_NAME, MP2_DYNAMIC_POINT_LIGHT_NODE_NAME, MP2_FLARE_NODE_NAME, MP2_VOLUME_LIGHTING_BOX_NODE_NAME, \
    MP2_PLAYER_NODE_NAME, MP2_MATERIAL_NODE_NAME
from max_payne_sdk.lvl2.max_lvl2 import MaxLVL2
from max_payne_sdk.lvl2.max_material import MaxMaterial
from max_payne_sdk.lvl2.max_material_category import MaxMaterialCategory
from max_payne_sdk.lvl2.max_texture import MaxTexture


def build_scene_tree():
    sel = cmds.ls(selection=True, long=True)
    if not sel or len(sel) > 1:
        cmds.confirmDialog(
            title=f"The selected node must be of type '{MP2_WORLD_GROUP_NODE_NAME}'.",
            message="Error",
            button=["OK"]
        )
        return []

    def build_tree(parent_node):
        children = cmds.listRelatives(parent_node, children=True, fullPath=True) or []

        parent = parent_node
        if cmds.nodeType(parent_node) == 'transform':
            parent = children[0]
            children.pop(0)

        m = cmds.getAttr(parent_node + ".matrix")

        matrix = [
            m[0:3],
            m[4:7],
            m[8:11]
        ]

        translate = [m[12], m[13], m[14]]

        bb_min = cmds.getAttr(parent + ".boundingBoxMin")[0]
        bb_max = cmds.getAttr(parent + ".boundingBoxMax")[0]

        # bb = cmds.exactWorldBoundingBox(node)
        # min_pt = bb[0:3]
        # max_pt = bb[3:6]

        dx = bb_max[0] - bb_min[0]
        dy = bb_max[1] - bb_min[1]
        dz = bb_max[2] - bb_min[2]

        radius = 0.5 * math.sqrt(dx * dx + dy * dy + dz * dz)


        return {
            "name": parent,
            "matrix": matrix,
            "translate": translate,
            "bb_min": bb_min,
            "bb_max": bb_max,
            "radius": radius,
            "type": cmds.nodeType(parent),
            "children": [build_tree(child) for child in children]
        }

    node_tree = []
    for node in sel:
        node_tree.append(build_tree(node))

    if len(node_tree) != 1:
        cmds.confirmDialog(
            title=f"The selected node must be of type '{MP2_WORLD_GROUP_NODE_NAME}'.",
            message="Error",
            button=["OK"]
        )
        return []

    return node_tree[0]

def build_materials(lv2):
    materials_names = []
    dg_materials = cmds.ls(materials=True)
    for material in dg_materials:
        if cmds.nodeType(material) == MP2_MATERIAL_NODE_NAME:
            materials_names.append(material)
    fill_materials(lv2, materials_names)

def create_lv2_node(node_type, lvl2:MaxLVL2):
    nodes = {
        MP2_JUMP_POINT_NODE_NAME: lvl2.createNodeJumpPoint,
        MP2_WAY_POINT_NODE_NAME: lvl2.createNodeWaypoint,
        MP2_AIN_NODE_NAME: lvl2.createNodeAin,
        MP2_LEVEL_ITEM_NODE_NAME: lvl2.createNodeLevelItem,
        MP2_ENEMY_NODE_NAME: lvl2.createNodeEnemy,
        MP2_TRIGGER_NODE_NAME: lvl2.createNodeTrigger,
        MP2_FLARE_NODE_NAME: lvl2.createNodeFlare,
        MP2_FSM_NODE_NAME: lvl2.createNodeFSM,
        MP2_DYNAMIC_POINT_LIGHT_NODE_NAME: lvl2.createNodeDynamicPointLight,
        MP2_VOLUME_LIGHTING_BOX_NODE_NAME: lvl2.createNodeVolumeLightingBox
    }

    return nodes[node_type]()

def foreach_nodes(parent, node_tree, lv2):
    for child in node_tree['children']:
        if child['type'] == MP2_WORLD_GROUP_NODE_NAME:
            continue
        if child['type'] == MP2_PLAYER_NODE_NAME:
            continue
        new_node = create_lv2_node(child['type'], lv2)
        fill_node_with_data(new_node, child)
        parent.children.append(new_node)
        foreach_nodes(new_node, child, lv2)


def export_lv2():
    node_tree = build_scene_tree()
    if len(node_tree) == 0:
        return

    lv2 = MaxLVL2()
    build_materials(lv2)
    foreach_nodes(lv2.node, node_tree, lv2)

    file_path = cmds.fileDialog2(
        caption="Save",
        dialogStyle=1,
        fileMode=0
    )

    bytes = lv2.getBytes()
    with open(file_path[0], 'wb') as file:
        for i in bytes:
            file.write(i)

    return