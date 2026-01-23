import math

import maya.cmds as cmds
import maya.mel as mel
import maya.api.OpenMaya as OpenMaya

from max_payne_maya.mp2nodes.mp2_node_ids import MP2_LEVEL_ITEM_NODE_NAME, MP2_ENEMY_NODE_NAME, MP2_TRIGGER_NODE_NAME, \
    MP2_FLARE_NODE_NAME, MP2_FSM_NODE_NAME, MP2_DYNAMIC_POINT_LIGHT_NODE_NAME, MP2_VOLUME_LIGHTING_BOX_NODE_NAME, \
    MP2_LEVEL_ITEM_NAMES_COMMON, MP2_USE_ACTIVATE_ANIMATIONS, MP2_FLARE_NAMES_COMMON, MP2_ENEMY_NAMES_COMMON, \
    MP2_DEFAULT_PLAYER_GROUPS


def fill_node_base_data(lv2_node, dg_node):
    lv2_node.node_translate = dg_node["translate"]
    lv2_node.node_matrix33 = dg_node["matrix"]
    lv2_node.aabb_min = dg_node["bb_min"]
    lv2_node.aabb_max = dg_node["bb_max"]
    lv2_node.radius = dg_node["radius"]
    lv2_node.node_is_visible = not cmds.getAttr(dg_node["name"] + ".na_hidden")
    lv2_node.node_exclude_from_game = cmds.getAttr(dg_node["name"] + ".na_excludeFromGame")
    lv2_node.node_exclude_from_lighting = cmds.getAttr(dg_node["name"] + ".na_excludeFromLighting")
    lv2_node.node_enable_export_regrouping = cmds.getAttr(dg_node["name"] + ".na_enableExportRegrouping")
    lv2_node.node_gameplay_critical = True
    lv2_node.node_name = dg_node["name"].split('|')[-1]


def fill_node_level_item(lv2_node, dg_node):
    if cmds.getAttr(dg_node["name"] + ".na_itemNameUseCustom"):
        lv2_node.item_type = cmds.getAttr(dg_node["name"] + ".na_itemNameCustom")
        return

    lv2_node.item_type = MP2_LEVEL_ITEM_NAMES_COMMON[cmds.getAttr(dg_node["name"] + ".na_itemNameCommon")]


def fill_node_trigger(lv2_node, dg_node):
    lv2_node.radius = cmds.getAttr(dg_node["name"] + ".na_radius")
    lv2_node.node_gameplay_critical = True
    lv2_node.activator_player = cmds.getAttr(dg_node["name"] + ".na_player")
    lv2_node.activator_use = cmds.getAttr(dg_node["name"] + ".na_use")
    lv2_node.activator_enemy = cmds.getAttr(dg_node["name"] + ".na_enemy")
    lv2_node.activator_bullet = cmds.getAttr(dg_node["name"] + ".na_bullet")
    lv2_node.activator_look_at = cmds.getAttr(dg_node["name"] + ".na_lookAt")
    lv2_node.activator_visibility = cmds.getAttr(dg_node["name"] + ".na_visibility")

    if cmds.getAttr(dg_node["name"] + ".na_activatorsAnimationUseCustom"):
        lv2_node.activator_use_animation = cmds.getAttr(dg_node["name"] + ".na_activatorsAnimationCustom")
        return

    lv2_node.activator_use_animation = MP2_USE_ACTIVATE_ANIMATIONS[
        cmds.getAttr(dg_node["name"] + ".na_activatorsAnimationCommon")]


def fill_node_enemy(lv2_node, dg_node):
    if cmds.getAttr(dg_node["name"] + ".na_skinUseCustom"):
        lv2_node.enemy_skin = cmds.getAttr(dg_node["name"] + ".na_skinCustom")
    else:
        lv2_node.enemy_skin = MP2_ENEMY_NAMES_COMMON[cmds.getAttr(dg_node["name"] + ".na_skinCommon")]

    lv2_node.enemy_group = MP2_DEFAULT_PLAYER_GROUPS[cmds.getAttr(dg_node["name"] + ".na_enemyGroup")]

    if cmds.getAttr(dg_node["name"] + ".na_activatorsAnimationUseCustom"):
        lv2_node.activator_use_animation = cmds.getAttr(dg_node["name"] + ".na_activatorsAnimationCustom")
    else:
        lv2_node.activator_use_animation = MP2_USE_ACTIVATE_ANIMATIONS[
            cmds.getAttr(dg_node["name"] + ".na_activatorsAnimationCommon")]


def fill_node_flare(lv2_node, dg_node):
    if cmds.getAttr(dg_node["name"] + ".na_flareNameUseCustom"):
        lv2_node.flare_name = cmds.getAttr(dg_node["name"] + ".na_flareNameCustom")
        return

    lv2_node.flare_name = MP2_FLARE_NAMES_COMMON[cmds.getAttr(dg_node["name"] + ".na_flareNameCommon")]


def fill_node_fsm(lv2_node, dg_node):
    pass


def fill_node_dynamic_point_light(lv2_node, dg_node):
    pass


def fill_node_volume_lighting_box(lv2_node, dg_node):
    pass


def fill_node_with_data(lv2_node, dg_node):
    fill_node_base_data(lv2_node, dg_node)

    nodes = {
        MP2_LEVEL_ITEM_NODE_NAME: fill_node_level_item,
        MP2_ENEMY_NODE_NAME: fill_node_enemy,
        MP2_TRIGGER_NODE_NAME: fill_node_trigger,
        MP2_FLARE_NODE_NAME: fill_node_flare,
        MP2_FSM_NODE_NAME: fill_node_fsm,
        MP2_DYNAMIC_POINT_LIGHT_NODE_NAME: fill_node_dynamic_point_light,
        MP2_VOLUME_LIGHTING_BOX_NODE_NAME: fill_node_volume_lighting_box
    }

    if dg_node['type'] in nodes:
        nodes[dg_node['type']](lv2_node, dg_node)
