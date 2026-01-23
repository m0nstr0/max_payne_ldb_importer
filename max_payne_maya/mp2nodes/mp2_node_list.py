import maya.api.OpenMaya as OpenMaya

from max_payne_maya.mp2nodes.mp2_node_ain import MP2NodeAin
from max_payne_maya.mp2nodes.mp2_node_dynamic_pointlight import MP2NodeDynamicPointLight
from max_payne_maya.mp2nodes.mp2_node_enemy import MP2NodeEnemy
from max_payne_maya.mp2nodes.mp2_node_flare import MP2NodeFlare
from max_payne_maya.mp2nodes.mp2_node_fsm import MP2NodeFSM
from max_payne_maya.mp2nodes.mp2_node_jump_point import MP2NodeJumpPoint
from max_payne_maya.mp2nodes.mp2_node_level_item import MP2NodeLevelItem
from max_payne_maya.mp2nodes.mp2_node_material import MP2NodeMaterial
from max_payne_maya.mp2nodes.mp2_node_player import MP2NodePlayer
from max_payne_maya.mp2nodes.mp2_node_trigger import MP2NodeTrigger
from max_payne_maya.mp2nodes.mp2_node_volume_lighting_box import MP2NodeVolumeLightingBox
from max_payne_maya.mp2nodes.mp2_node_waypoint import MP2NodeWaypoint
from max_payne_maya.mp2nodes.mp2_node_world_group import MP2NodeWorldGroup

MP2_NODES = [
    MP2NodeAin,
    MP2NodeDynamicPointLight,
    MP2NodeEnemy,
    MP2NodeFlare,
    MP2NodeFSM,
    MP2NodeJumpPoint,
    MP2NodeLevelItem,
    MP2NodeMaterial,
    MP2NodePlayer,
    MP2NodeTrigger,
    MP2NodeVolumeLightingBox,
    MP2NodeWaypoint,
    MP2NodeWorldGroup
]


def registerNodes(plugin):
    for node in MP2_NODES:
        try:
            node.registerNode(plugin)
        except Exception:
            OpenMaya.MGlobal.displayError("Failed to register node: " + node.NODE_NAME)
            raise


def deregisterNodes(plugin):
    for node in MP2_NODES:
        try:
            node.deregisterNode(plugin)
        except Exception:
            OpenMaya.MGlobal.displayError("Failed to register node: " + node.NODE_NAME)
            raise
