import maya.api.OpenMaya as OpenMaya
from max_payne_maya.mp2nodes.mp2_node_ids import MP2_WORLD_GROUP_NODE_NAME, MP2_WORLD_GROUP_NODE_ID
from max_payne_maya.mp2nodes.mp2_node_locator import MP2NodeLocator, MP2NodeLocatorDrawData, MP2NodeLocatorDrawOverride


class MP2NodeWorldGroup(MP2NodeLocator):
    NODE_ID = OpenMaya.MTypeId(MP2_WORLD_GROUP_NODE_ID)
    NODE_NAME = MP2_WORLD_GROUP_NODE_NAME

    @classmethod
    def drawOverrideCreator(cls):
        return MP2NodeWorldGroupDrawOverride.creator


class MP2NodeWorldGroupDrawData(MP2NodeLocatorDrawData):
    COLOR = (0.0, 0.0, 1.0, 0.25)
    TEXT_COLOR = (0.0, 0.0, 1.0)
    RADIUS = 0.05
    LABEL = MP2NodeWorldGroup.NODE_NAME


class MP2NodeWorldGroupDrawOverride(MP2NodeLocatorDrawOverride):
    def getDataClass(self):
        return MP2NodeWorldGroupDrawData

