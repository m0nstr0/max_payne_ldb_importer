import maya.api.OpenMaya as OpenMaya
import maya.api.OpenMayaRender as OpenMayaRender
import maya.api.OpenMayaUI as OpenMayaUI
import maya.cmds as cmds

from max_payne_maya.mp2nodes.mp2_attr_util import create_attr_numeric, create_attr_string, create_attr_enum
from max_payne_maya.mp2nodes.mp2_node_ids import MP2_LEVEL_ITEM_NODE_ID, MP2_LEVEL_ITEM_NODE_NAME, \
    MP2_LEVEL_ITEM_NAMES_COMMON, MP2_USE_ACTIVATE_ANIMATIONS
from max_payne_maya.mp2nodes.mp2_node_locator import MP2NodeLocator, MP2NodeLocatorDrawData, MP2NodeLocatorDrawOverride


class MP2NodeLevelItem(MP2NodeLocator):
    NODE_ID = OpenMaya.MTypeId(MP2_LEVEL_ITEM_NODE_ID)
    NODE_NAME = MP2_LEVEL_ITEM_NODE_NAME

    ItemNameCustomAttr = OpenMaya.MObject()
    ItemNameCommonAttr = OpenMaya.MObject()
    ItemNameUseCustomAttr = OpenMaya.MObject()

    @classmethod
    def drawOverrideCreator(cls):
        return MP2NodeFlareDrawOverride.creator

    @classmethod
    def initializer(cls):
        super().initializer()
        create_attr_numeric(cls, "ItemNameUseCustomAttr", 'na_itemNameUseCustom', OpenMaya.MFnNumericData.kBoolean,0)
        create_attr_string(cls, "ItemNameCustomAttr", 'na_itemNameCustom', MP2_LEVEL_ITEM_NAMES_COMMON[0])
        create_attr_enum(cls, "ItemNameCommonAttr", 'na_itemNameCommon', MP2_LEVEL_ITEM_NAMES_COMMON)


class MP2NodeLevelItemDrawData(MP2NodeLocatorDrawData):
    COLOR = (1.0, 1.0, 0.0, 0.25)
    TEXT_COLOR = (1.0, 1.0, 0.0)
    RADIUS = 0.05
    LABEL = MP2NodeLevelItem.NODE_NAME


class MP2NodeFlareDrawOverride(MP2NodeLocatorDrawOverride):
    def getDataClass(self):
        return MP2NodeLevelItemDrawData

