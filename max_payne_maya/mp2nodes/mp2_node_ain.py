import maya.api.OpenMaya as OpenMaya

from max_payne_maya.mp2nodes.mp2_node_ids import MP2_AIN_NODE_NAME, MP2_AIN_NODE_ID
from max_payne_maya.mp2nodes.mp2_node_locator import MP2NodeLocator, MP2NodeLocatorDrawData, MP2NodeLocatorDrawOverride


class MP2NodeAin(MP2NodeLocator):
    NODE_ID = OpenMaya.MTypeId(MP2_AIN_NODE_ID)
    NODE_NAME = MP2_AIN_NODE_NAME

    @classmethod
    def drawOverrideCreator(cls):
        return MP2NodeAinDrawOverride.creator


class MP2NodeAinDrawData(MP2NodeLocatorDrawData):
    COLOR = (0.0, 0.0, 1.0, 0.25)
    TEXT_COLOR = (0.0, 0.0, 1.0)
    RADIUS = 0.5
    LABEL = MP2NodeAin.NODE_NAME


class MP2NodeAinDrawOverride(MP2NodeLocatorDrawOverride):
    def getDataClass(self):
        return MP2NodeAinDrawData
