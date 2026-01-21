import maya.api.OpenMaya as OpenMaya
import maya.api.OpenMayaRender as OpenMayaRender

from max_payne_maya.mp2nodes.mp2_main_menu import mp2_create_main_menu, mp2_delete_main_menu
from max_payne_maya.mp2nodes.mp2_node_ain import MP2NodeAin, MP2NodeAinDrawOverride
from max_payne_maya.mp2nodes.mp2_node_dynamic_pointlight import MP2NodeDynamicPointlight, \
    MP2NodeDynamicPointlightDrawOverride
from max_payne_maya.mp2nodes.mp2_node_enemy import MP2NodeEnemy, MP2NodeEnemyDrawOverride
from max_payne_maya.mp2nodes.mp2_node_flare import MP2NodeFlare, MP2NodeFlareDrawOverride
from max_payne_maya.mp2nodes.mp2_node_fsm import MP2NodeFSM, MP2NodeFSMDrawOverride
from max_payne_maya.mp2nodes.mp2_node_ids import MP2_JUMP_POINT_NODE_NAME, MP2_LEVEL_ITEM_NODE_NAME, MP2_AIN_NODE_NAME, \
    MP2_WAY_POINT_NODE_NAME, MP2_FLARE_NODE_NAME, MP2_TRIGGER_NODE_NAME, MP2_FSM_NODE_NAME, MP2_PLAYER_NODE_NAME, \
    MP2_WORLD_GROUP_NODE_NAME, MP2_ENEMY_NODE_NAME, MP2_DYNAMIC_POINT_LIGHT_NODE_NAME, \
    MP2_VOLUME_LIGHTING_BOX_NODE_NAME, MP2_MATERIAL_NODE_NAME
from max_payne_maya.mp2nodes.mp2_node_jump_point import MP2NodeJumpPoint, MP2NodeJumpPointDrawOverride
from max_payne_maya.mp2nodes.mp2_node_level_item import MP2NodeLevelItem, MP2NodeLevelItemDrawOverride
from max_payne_maya.mp2nodes.mp2_node_material import MP2NodeMaterial, MP2NodeMaterialDrawOverride
from max_payne_maya.mp2nodes.mp2_node_player import MP2NodePlayer, MP2NodePlayerDrawOverride
from max_payne_maya.mp2nodes.mp2_node_trigger import MP2NodeTrigger, MP2NodeTriggerDrawOverride
from max_payne_maya.mp2nodes.mp2_node_volume_lighting_box import MP2NodeVolumeLightingBox, \
    MP2NodeVolumeLightingBoxDrawOverride
from max_payne_maya.mp2nodes.mp2_node_waypoint import MP2NodeWaypoint, MP2NodeWaypointDrawOverride

from shiboken6 import wrapInstance
import maya.api.OpenMayaUI as OpenMayaUI
from PySide6 import QtWidgets

from max_payne_maya.mp2nodes.mp2_node_world_group import MP2NodeWorldGroup, MP2NodeWorldGroupDrawOverride

PLUGIN_NAME = "Max Payne 2 Custom Nodes For LDB Import"
PLUGIN_COMPANY = "Bolotaev Sergey"


def maya_useNewAPI():
    """Tells Maya to use Python API 2.0."""
    pass


# JUMP POINT NODE START
def registerJumpPointNode(plugin):
    try:
        plugin.registerNode(
            MP2NodeJumpPoint.NODE_NAME,
            MP2NodeJumpPoint.NODE_ID,
            MP2NodeJumpPoint.creator,
            MP2NodeJumpPoint.initializer,
            OpenMaya.MPxNode.kLocatorNode,
            MP2NodeJumpPoint.NODE_DRAW_CLASSIFICATION
        )
        OpenMayaRender.MDrawRegistry.registerDrawOverrideCreator(MP2NodeJumpPoint.NODE_DRAW_CLASSIFICATION,
                                                                 MP2NodeJumpPoint.NODE_DRAW_REGISTRANT_ID,
                                                                 MP2NodeJumpPointDrawOverride.creator)
    except Exception:
        OpenMaya.MGlobal.displayError("Failed to register node: " + MP2_JUMP_POINT_NODE_NAME)
        raise


def deregisterJumpPointNode(plugin):
    try:
        OpenMayaRender.MDrawRegistry.deregisterDrawOverrideCreator(MP2NodeJumpPoint.NODE_DRAW_CLASSIFICATION,
                                                                   MP2NodeJumpPoint.NODE_DRAW_REGISTRANT_ID)
        plugin.deregisterNode(MP2NodeJumpPoint.NODE_ID)
    except Exception:
        OpenMaya.MGlobal.displayError("Failed to unregister node: " + MP2_JUMP_POINT_NODE_NAME)
        raise


# JUMP POINT NODE END

# LEVEL ITEM NODE START
def registerLevelItemNode(plugin):
    try:
        plugin.registerNode(
            MP2NodeLevelItem.NODE_NAME,
            MP2NodeLevelItem.NODE_ID,
            MP2NodeLevelItem.creator,
            MP2NodeLevelItem.initializer,
            OpenMaya.MPxNode.kLocatorNode,
            MP2NodeLevelItem.NODE_DRAW_CLASSIFICATION
        )
        OpenMayaRender.MDrawRegistry.registerDrawOverrideCreator(MP2NodeLevelItem.NODE_DRAW_CLASSIFICATION,
                                                                 MP2NodeLevelItem.NODE_DRAW_REGISTRANT_ID,
                                                                 MP2NodeLevelItemDrawOverride.creator)
    except Exception:
        OpenMaya.MGlobal.displayError("Failed to register node: " + MP2_LEVEL_ITEM_NODE_NAME)
        raise


def deregisterLevelItemNode(plugin):
    try:
        OpenMayaRender.MDrawRegistry.deregisterDrawOverrideCreator(MP2NodeLevelItem.NODE_DRAW_CLASSIFICATION,
                                                                   MP2NodeLevelItem.NODE_DRAW_REGISTRANT_ID)
        plugin.deregisterNode(MP2NodeLevelItem.NODE_ID)
    except Exception:
        OpenMaya.MGlobal.displayError("Failed to unregister node: " + MP2_LEVEL_ITEM_NODE_NAME)
        raise


# LEVEL ITEM NODE END


# AIN NODE START
def registerAinNode(plugin):
    try:
        plugin.registerNode(
            MP2NodeAin.NODE_NAME,
            MP2NodeAin.NODE_ID,
            MP2NodeAin.creator,
            MP2NodeAin.initializer,
            OpenMaya.MPxNode.kLocatorNode,
            MP2NodeAin.NODE_DRAW_CLASSIFICATION
        )
        OpenMayaRender.MDrawRegistry.registerDrawOverrideCreator(MP2NodeAin.NODE_DRAW_CLASSIFICATION,
                                                                 MP2NodeAin.NODE_DRAW_REGISTRANT_ID,
                                                                 MP2NodeAinDrawOverride.creator)
    except Exception:
        OpenMaya.MGlobal.displayError("Failed to register node: " + MP2_AIN_NODE_NAME)
        raise


def deregisterAinNode(plugin):
    try:
        OpenMayaRender.MDrawRegistry.deregisterDrawOverrideCreator(MP2NodeAin.NODE_DRAW_CLASSIFICATION,
                                                                   MP2NodeAin.NODE_DRAW_REGISTRANT_ID)
        plugin.deregisterNode(MP2NodeAin.NODE_ID)
    except Exception:
        OpenMaya.MGlobal.displayError("Failed to unregister node: " + MP2_AIN_NODE_NAME)
        raise


# AIN NODE END

# WAY POINT NODE START
def registerWaypointNode(plugin):
    try:
        plugin.registerNode(
            MP2NodeWaypoint.NODE_NAME,
            MP2NodeWaypoint.NODE_ID,
            MP2NodeWaypoint.creator,
            MP2NodeWaypoint.initializer,
            OpenMaya.MPxNode.kLocatorNode,
            MP2NodeWaypoint.NODE_DRAW_CLASSIFICATION
        )
        OpenMayaRender.MDrawRegistry.registerDrawOverrideCreator(MP2NodeWaypoint.NODE_DRAW_CLASSIFICATION,
                                                                 MP2NodeWaypoint.NODE_DRAW_REGISTRANT_ID,
                                                                 MP2NodeWaypointDrawOverride.creator)
    except Exception:
        OpenMaya.MGlobal.displayError("Failed to register node: " + MP2_WAY_POINT_NODE_NAME)
        raise


def deregisterWaypointNode(plugin):
    try:
        OpenMayaRender.MDrawRegistry.deregisterDrawOverrideCreator(MP2NodeWaypoint.NODE_DRAW_CLASSIFICATION,
                                                                   MP2NodeWaypoint.NODE_DRAW_REGISTRANT_ID)
        plugin.deregisterNode(MP2NodeWaypoint.NODE_ID)
    except Exception:
        OpenMaya.MGlobal.displayError("Failed to unregister node: " + MP2_WAY_POINT_NODE_NAME)
        raise


# WAY POINT NODE END


# FLARE NODE START
def registerFlareNode(plugin):
    try:
        plugin.registerNode(
            MP2NodeFlare.NODE_NAME,
            MP2NodeFlare.NODE_ID,
            MP2NodeFlare.creator,
            MP2NodeFlare.initializer,
            OpenMaya.MPxNode.kLocatorNode,
            MP2NodeFlare.NODE_DRAW_CLASSIFICATION
        )
        OpenMayaRender.MDrawRegistry.registerDrawOverrideCreator(MP2NodeFlare.NODE_DRAW_CLASSIFICATION,
                                                                 MP2NodeFlare.NODE_DRAW_REGISTRANT_ID,
                                                                 MP2NodeFlareDrawOverride.creator)
    except Exception:
        OpenMaya.MGlobal.displayError("Failed to register node: " + MP2_FLARE_NODE_NAME)
        raise


def deregisterFlareNode(plugin):
    try:
        OpenMayaRender.MDrawRegistry.deregisterDrawOverrideCreator(MP2NodeFlare.NODE_DRAW_CLASSIFICATION,
                                                                   MP2NodeFlare.NODE_DRAW_REGISTRANT_ID)
        plugin.deregisterNode(MP2NodeFlare.NODE_ID)
    except Exception:
        OpenMaya.MGlobal.displayError("Failed to unregister node: " + MP2_FLARE_NODE_NAME)
        raise


# FLARE NODE END

# TRIGGER NODE START
def registerTriggerNode(plugin):
    try:
        plugin.registerNode(
            MP2NodeTrigger.NODE_NAME,
            MP2NodeTrigger.NODE_ID,
            MP2NodeTrigger.creator,
            MP2NodeTrigger.initializer,
            OpenMaya.MPxNode.kLocatorNode,
            MP2NodeTrigger.NODE_DRAW_CLASSIFICATION
        )
        OpenMayaRender.MDrawRegistry.registerDrawOverrideCreator(MP2NodeTrigger.NODE_DRAW_CLASSIFICATION,
                                                                 MP2NodeTrigger.NODE_DRAW_REGISTRANT_ID,
                                                                 MP2NodeTriggerDrawOverride.creator)
    except Exception:
        OpenMaya.MGlobal.displayError("Failed to register node: " + MP2_TRIGGER_NODE_NAME)
        raise


def deregisterTriggerNode(plugin):
    try:
        OpenMayaRender.MDrawRegistry.deregisterDrawOverrideCreator(MP2NodeTrigger.NODE_DRAW_CLASSIFICATION,
                                                                   MP2NodeTrigger.NODE_DRAW_REGISTRANT_ID)
        plugin.deregisterNode(MP2NodeTrigger.NODE_ID)
    except Exception:
        OpenMaya.MGlobal.displayError("Failed to unregister node: " + MP2_TRIGGER_NODE_NAME)
        raise


# TRIGGER NODE END

# FSM NODE START
def registerFSMNode(plugin):
    try:
        plugin.registerNode(
            MP2NodeFSM.NODE_NAME,
            MP2NodeFSM.NODE_ID,
            MP2NodeFSM.creator,
            MP2NodeFSM.initializer,
            OpenMaya.MPxNode.kLocatorNode,
            MP2NodeFSM.NODE_DRAW_CLASSIFICATION
        )
        OpenMayaRender.MDrawRegistry.registerDrawOverrideCreator(MP2NodeFSM.NODE_DRAW_CLASSIFICATION,
                                                                 MP2NodeFSM.NODE_DRAW_REGISTRANT_ID,
                                                                 MP2NodeFSMDrawOverride.creator)
    except Exception:
        OpenMaya.MGlobal.displayError("Failed to register node: " + MP2_FSM_NODE_NAME)
        raise


def deregisterFSMNode(plugin):
    try:
        OpenMayaRender.MDrawRegistry.deregisterDrawOverrideCreator(MP2NodeFSM.NODE_DRAW_CLASSIFICATION,
                                                                   MP2NodeFSM.NODE_DRAW_REGISTRANT_ID)
        plugin.deregisterNode(MP2NodeFSM.NODE_ID)
    except Exception:
        OpenMaya.MGlobal.displayError("Failed to unregister node: " + MP2_FSM_NODE_NAME)
        raise


# FSM END

# PLAYER NODE START
def registerPlayerNode(plugin):
    try:
        plugin.registerNode(
            MP2NodePlayer.NODE_NAME,
            MP2NodePlayer.NODE_ID,
            MP2NodePlayer.creator,
            MP2NodePlayer.initializer,
            OpenMaya.MPxNode.kLocatorNode,
            MP2NodePlayer.NODE_DRAW_CLASSIFICATION
        )
        OpenMayaRender.MDrawRegistry.registerDrawOverrideCreator(MP2NodePlayer.NODE_DRAW_CLASSIFICATION,
                                                                 MP2NodePlayer.NODE_DRAW_REGISTRANT_ID,
                                                                 MP2NodePlayerDrawOverride.creator)
    except Exception:
        OpenMaya.MGlobal.displayError("Failed to register node: " + MP2_PLAYER_NODE_NAME)
        raise


def deregisterPlayerNode(plugin):
    try:
        OpenMayaRender.MDrawRegistry.deregisterDrawOverrideCreator(MP2NodePlayer.NODE_DRAW_CLASSIFICATION,
                                                                   MP2NodePlayer.NODE_DRAW_REGISTRANT_ID)
        plugin.deregisterNode(MP2NodePlayer.NODE_ID)
    except Exception:
        OpenMaya.MGlobal.displayError("Failed to unregister node: " + MP2_PLAYER_NODE_NAME)
        raise


# PLAYER END

# WORLD GROUP START
def registerWorldGroupNode(plugin):
    try:
        plugin.registerNode(
            MP2NodeWorldGroup.NODE_NAME,
            MP2NodeWorldGroup.NODE_ID,
            MP2NodeWorldGroup.creator,
            MP2NodeWorldGroup.initializer,
            OpenMaya.MPxNode.kLocatorNode,
            MP2NodeWorldGroup.NODE_DRAW_CLASSIFICATION
        )
        OpenMayaRender.MDrawRegistry.registerDrawOverrideCreator(MP2NodeWorldGroup.NODE_DRAW_CLASSIFICATION,
                                                                 MP2NodeWorldGroup.NODE_DRAW_REGISTRANT_ID,
                                                                 MP2NodeWorldGroupDrawOverride.creator)
    except Exception:
        OpenMaya.MGlobal.displayError("Failed to register node: " + MP2_WORLD_GROUP_NODE_NAME)
        raise


def deregisterWorldGroupNode(plugin):
    try:
        OpenMayaRender.MDrawRegistry.deregisterDrawOverrideCreator(MP2NodeWorldGroup.NODE_DRAW_CLASSIFICATION,
                                                                   MP2NodeWorldGroup.NODE_DRAW_REGISTRANT_ID)
        plugin.deregisterNode(MP2NodeWorldGroup.NODE_ID)
    except Exception:
        OpenMaya.MGlobal.displayError("Failed to unregister node: " + MP2_WORLD_GROUP_NODE_NAME)
        raise


# WORLD GROUP END

# ENEMY START
def registerEnemyNode(plugin):
    try:
        plugin.registerNode(
            MP2NodeEnemy.NODE_NAME,
            MP2NodeEnemy.NODE_ID,
            MP2NodeEnemy.creator,
            MP2NodeEnemy.initializer,
            OpenMaya.MPxNode.kLocatorNode,
            MP2NodeEnemy.NODE_DRAW_CLASSIFICATION
        )
        OpenMayaRender.MDrawRegistry.registerDrawOverrideCreator(MP2NodeEnemy.NODE_DRAW_CLASSIFICATION,
                                                                 MP2NodeEnemy.NODE_DRAW_REGISTRANT_ID,
                                                                 MP2NodeEnemyDrawOverride.creator)
    except Exception:
        OpenMaya.MGlobal.displayError("Failed to register node: " + MP2_ENEMY_NODE_NAME)
        raise


def deregisterEnemyNode(plugin):
    try:
        OpenMayaRender.MDrawRegistry.deregisterDrawOverrideCreator(MP2NodeEnemy.NODE_DRAW_CLASSIFICATION,
                                                                   MP2NodeEnemy.NODE_DRAW_REGISTRANT_ID)
        plugin.deregisterNode(MP2NodeEnemy.NODE_ID)
    except Exception:
        OpenMaya.MGlobal.displayError("Failed to unregister node: " + MP2_ENEMY_NODE_NAME)
        raise


# ENEMY END

# DYNAMIC POINT LIGHT START
def registerDynamicPointlightNode(plugin):
    try:
        plugin.registerNode(
            MP2NodeDynamicPointlight.NODE_NAME,
            MP2NodeDynamicPointlight.NODE_ID,
            MP2NodeDynamicPointlight.creator,
            MP2NodeDynamicPointlight.initializer,
            OpenMaya.MPxNode.kLocatorNode,
            MP2NodeDynamicPointlight.NODE_DRAW_CLASSIFICATION
        )
        OpenMayaRender.MDrawRegistry.registerDrawOverrideCreator(MP2NodeDynamicPointlight.NODE_DRAW_CLASSIFICATION,
                                                                 MP2NodeDynamicPointlight.NODE_DRAW_REGISTRANT_ID,
                                                                 MP2NodeDynamicPointlightDrawOverride.creator)
    except Exception:
        OpenMaya.MGlobal.displayError("Failed to register node: " + MP2_DYNAMIC_POINT_LIGHT_NODE_NAME)
        raise


def deregisterDynamicPointlightNode(plugin):
    try:
        OpenMayaRender.MDrawRegistry.deregisterDrawOverrideCreator(MP2NodeDynamicPointlight.NODE_DRAW_CLASSIFICATION,
                                                                   MP2NodeDynamicPointlight.NODE_DRAW_REGISTRANT_ID)
        plugin.deregisterNode(MP2NodeDynamicPointlight.NODE_ID)
    except Exception:
        OpenMaya.MGlobal.displayError("Failed to unregister node: " + MP2_DYNAMIC_POINT_LIGHT_NODE_NAME)
        raise


# DYNAMIC POINT LIGHT END

# VOLUME LIGHTING BOX START

def registerVolumelightingBoxNode(plugin):
    try:
        plugin.registerNode(
            MP2NodeVolumeLightingBox.NODE_NAME,
            MP2NodeVolumeLightingBox.NODE_ID,
            MP2NodeVolumeLightingBox.creator,
            MP2NodeVolumeLightingBox.initializer,
            OpenMaya.MPxNode.kLocatorNode,
            MP2NodeVolumeLightingBox.NODE_DRAW_CLASSIFICATION
        )
        OpenMayaRender.MDrawRegistry.registerDrawOverrideCreator(MP2NodeVolumeLightingBox.NODE_DRAW_CLASSIFICATION,
                                                                 MP2NodeVolumeLightingBox.NODE_DRAW_REGISTRANT_ID,
                                                                 MP2NodeVolumeLightingBoxDrawOverride.creator)
    except Exception:
        OpenMaya.MGlobal.displayError("Failed to register node: " + MP2_VOLUME_LIGHTING_BOX_NODE_NAME)
        raise


def deregisterVolumelightingBoxNode(plugin):
    try:
        OpenMayaRender.MDrawRegistry.deregisterDrawOverrideCreator(MP2NodeVolumeLightingBox.NODE_DRAW_CLASSIFICATION,
                                                                   MP2NodeVolumeLightingBox.NODE_DRAW_REGISTRANT_ID)
        plugin.deregisterNode(MP2NodeVolumeLightingBox.NODE_ID)
    except Exception:
        OpenMaya.MGlobal.displayError("Failed to unregister node: " + MP2_VOLUME_LIGHTING_BOX_NODE_NAME)
        raise


# VOLUME LIGHTING BOX END

# MATERIAL START

def registerMaterialNode(plugin):
    try:
        plugin.registerNode(
            MP2NodeMaterial.NODE_NAME,
            MP2NodeMaterial.NODE_ID,
            MP2NodeMaterial.creator,
            MP2NodeMaterial.initializer,
            OpenMaya.MPxNode.kDependNode,
            MP2NodeMaterial.NODE_CLASSIFICATION
        )
        OpenMayaRender.MDrawRegistry.registerSurfaceShadingNodeOverrideCreator(
            MP2NodeMaterial.NODE_DRAW_CLASSIFICATION,
            MP2NodeMaterial.NODE_DRAW_REGISTRANT_ID,
            MP2NodeMaterialDrawOverride.creator
        )
    except Exception:
        OpenMaya.MGlobal.displayError("Failed to register node: " + MP2_MATERIAL_NODE_NAME)
        raise


def deregisterMaterialNode(plugin):
    try:
        plugin.deregisterNode(MP2NodeMaterial.NODE_ID)
        OpenMayaRender.MDrawRegistry.deregisterSurfaceShadingNodeOverrideCreator(
            MP2NodeMaterial.NODE_DRAW_CLASSIFICATION,
            MP2NodeMaterial.NODE_DRAW_REGISTRANT_ID
        )
    except Exception:
        OpenMaya.MGlobal.displayError("Failed to unregister node: " + MP2_MATERIAL_NODE_NAME)
        raise


# MATERIAL END

def initializePlugin(maya_object):
    mp2_create_main_menu()
    plugin = OpenMaya.MFnPlugin(maya_object, PLUGIN_COMPANY, '1.0')
    registerJumpPointNode(plugin)
    registerLevelItemNode(plugin)
    registerAinNode(plugin)
    registerWaypointNode(plugin)
    registerFlareNode(plugin)
    registerTriggerNode(plugin)
    registerFSMNode(plugin)
    registerPlayerNode(plugin)
    registerWorldGroupNode(plugin)
    registerEnemyNode(plugin)
    registerDynamicPointlightNode(plugin)
    registerVolumelightingBoxNode(plugin)
    registerMaterialNode(plugin)


def uninitializePlugin(maya_object):
    mp2_delete_main_menu()
    plugin = OpenMaya.MFnPlugin(maya_object)
    deregisterJumpPointNode(plugin)
    deregisterLevelItemNode(plugin)
    deregisterAinNode(plugin)
    deregisterWaypointNode(plugin)
    deregisterFlareNode(plugin)
    deregisterTriggerNode(plugin)
    deregisterFSMNode(plugin)
    deregisterPlayerNode(plugin)
    deregisterWorldGroupNode(plugin)
    deregisterEnemyNode(plugin)
    deregisterDynamicPointlightNode(plugin)
    deregisterVolumelightingBoxNode(plugin)
    deregisterMaterialNode(plugin)
