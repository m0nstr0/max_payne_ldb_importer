import maya.api.OpenMaya as OpenMaya
from max_payne_maya.mp2nodes.mp2_node_ids import MP2_JUMP_POINT_NODE_NAME, MP2_JUMP_POINT_NODE_ID
from max_payne_maya.mp2nodes.mp2_node_locator import MP2NodeLocator, MP2NodeLocatorDrawData, MP2NodeLocatorDrawOverride


class MP2NodeJumpPoint(MP2NodeLocator):
    NODE_ID = OpenMaya.MTypeId(MP2_JUMP_POINT_NODE_ID)
    NODE_NAME = MP2_JUMP_POINT_NODE_NAME

    @classmethod
    def drawOverrideCreator(cls):
        return MP2NodeJumpPointDrawOverride.creator


class MP2NodeJumpPointDrawData(MP2NodeLocatorDrawData):
    COLOR = (1.0, 0.0, 0.0, 0.25)
    TEXT_COLOR = (1.0, 0.0, 0.0)
    RADIUS = 0.5
    LABEL = MP2NodeJumpPoint.NODE_NAME


class MP2NodeJumpPointDrawOverride(MP2NodeLocatorDrawOverride):
    def getDataClass(self):
        return MP2NodeJumpPointDrawData
