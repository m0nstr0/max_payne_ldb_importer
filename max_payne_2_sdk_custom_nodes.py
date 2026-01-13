import maya.api.OpenMaya as OpenMaya
import maya.api.OpenMayaRender as OpenMayaRender

#from maya.OpenMaya import MGlobal

from max_payne_maya.mp2nodes.mp2_node_ain import MP2NodeAin, MP2NodeAinDrawOverride
from max_payne_maya.mp2nodes.mp2_node_flare import MP2NodeFlare, MP2NodeFlareDrawOverride
from max_payne_maya.mp2nodes.mp2_node_ids import MP2_JUMP_POINT_NODE_NAME, MP2_LEVEL_ITEM_NODE_NAME, MP2_AIN_NODE_NAME, MP2_WAY_POINT_NODE_NAME, MP2_FLARE_NODE_NAME, MP2_TRIGGER_NODE_NAME
from max_payne_maya.mp2nodes.mp2_node_jump_point import MP2NodeJumpPoint, MP2NodeJumpPointDrawOverride
from max_payne_maya.mp2nodes.mp2_node_level_item import MP2NodeLevelItem, MP2NodeLevelItemDrawOverride
from max_payne_maya.mp2nodes.mp2_node_trigger import MP2NodeTrigger, MP2NodeTriggerDrawOverride
from max_payne_maya.mp2nodes.mp2_node_waypoint import MP2NodeWaypoint, MP2NodeWaypointDrawOverride

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

def initializePlugin(maya_object):
    plugin = OpenMaya.MFnPlugin(maya_object, PLUGIN_COMPANY, '1.0')
    registerJumpPointNode(plugin)
    registerLevelItemNode(plugin)
    registerAinNode(plugin)
    registerWaypointNode(plugin)
    registerFlareNode(plugin)
    registerTriggerNode(plugin)

def uninitializePlugin(maya_object):
    plugin = OpenMaya.MFnPlugin(maya_object)
    deregisterJumpPointNode(plugin)
    deregisterLevelItemNode(plugin)
    deregisterAinNode(plugin)
    deregisterWaypointNode(plugin)
    deregisterFlareNode(plugin)
    deregisterTriggerNode(plugin)
