import maya.api.OpenMaya as OpenMaya
from max_payne_maya.mp2nodes.mp2_attr_util import create_attr_string
from max_payne_maya.mp2nodes.mp2_node_ids import MP2_PLAYER_NODE_NAME, MP2_PLAYER_NODE_ID
from max_payne_maya.mp2nodes.mp2_node_locator import MP2NodeLocator, MP2NodeLocatorDrawData, MP2NodeLocatorDrawOverride


class MP2NodePlayer(MP2NodeLocator):
    NODE_ID = OpenMaya.MTypeId(MP2_PLAYER_NODE_ID)
    NODE_NAME = MP2_PLAYER_NODE_NAME

    FSMAttr = OpenMaya.MObject()

    @classmethod
    def drawOverrideCreator(cls):
        return MP2NodePlayerDrawOverride.creator

    @classmethod
    def initializer(cls):
        super().initializer()
        create_attr_string(cls, "FSMAttr", 'na_fsm', '')


class MP2NodePlayerDrawData(MP2NodeLocatorDrawData):
    COLOR = (0.0, 1.0, 0.0, 0.25)
    TEXT_COLOR = (0.0, 1.0, 0.0)
    RADIUS = 0.05
    LABEL = MP2NodePlayer.NODE_NAME


class MP2NodePlayerDrawOverride(MP2NodeLocatorDrawOverride):
    def getDataClass(self):
        return MP2NodePlayerDrawData

