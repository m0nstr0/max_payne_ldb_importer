import maya.api.OpenMaya as OpenMaya
from max_payne_maya.mp2nodes.mp2_node_ids import MP2_WAY_POINT_NODE_ID, MP2_WAY_POINT_NODE_NAME
from max_payne_maya.mp2nodes.mp2_node_locator import MP2NodeLocator, MP2NodeLocatorDrawData, MP2NodeLocatorDrawOverride


class MP2NodeWaypoint(MP2NodeLocator):
    NODE_ID = OpenMaya.MTypeId(MP2_WAY_POINT_NODE_ID)
    NODE_NAME = MP2_WAY_POINT_NODE_NAME

    @classmethod
    def drawOverrideCreator(cls):
        return MP2NodeWaypointDrawOverride.creator


class MP2NodeWaypointDrawData(MP2NodeLocatorDrawData):
    COLOR = (1.0, 0.5, 0.0, 0.25)
    TEXT_COLOR = (1.0, 0.5, 0.0)
    RADIUS = 0.5
    LABEL = MP2NodeWaypoint.NODE_NAME


class MP2NodeWaypointDrawOverride(MP2NodeLocatorDrawOverride):
    def getDataClass(self):
        return MP2NodeWaypointDrawData
