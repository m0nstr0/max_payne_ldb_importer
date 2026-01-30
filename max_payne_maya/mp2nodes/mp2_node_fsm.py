import maya.api.OpenMaya as OpenMaya
from max_payne_maya.mp2nodes.mp2_attr_util import create_attr_string
from max_payne_maya.mp2nodes.mp2_node_ids import MP2_FSM_NODE_ID, MP2_FSM_NODE_NAME
from max_payne_maya.mp2nodes.mp2_node_locator import MP2NodeLocator, MP2NodeLocatorDrawData, MP2NodeLocatorDrawOverride


class MP2NodeFSM(MP2NodeLocator):
    NODE_ID = OpenMaya.MTypeId(MP2_FSM_NODE_ID)
    NODE_NAME = MP2_FSM_NODE_NAME

    FSMAttr = OpenMaya.MObject()

    @classmethod
    def drawOverrideCreator(cls):
        return MP2NodeFSMDrawOverride.creator

    @classmethod
    def initializer(cls):
        super().initializer()
        create_attr_string(cls, "FSMAttr", 'na_fsm', '')


class MP2NodeFSMDrawData(MP2NodeLocatorDrawData):
    COLOR = (0.0, 1.0, 0.0, 0.25)
    TEXT_COLOR = (0.0, 0.0, 1.0)
    RADIUS = 0.05
    LABEL = MP2NodeFSM.NODE_NAME


class MP2NodeFSMDrawOverride(MP2NodeLocatorDrawOverride):
    def getDataClass(self):
        return MP2NodeFSMDrawData
