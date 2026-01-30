import maya.api.OpenMaya as OpenMaya
from max_payne_maya.mp2nodes.mp2_attr_util import create_attr_numeric, create_attr_string, create_attr_enum
from max_payne_maya.mp2nodes.mp2_node_ids import MP2_FLARE_NODE_NAME, MP2_FLARE_NODE_ID, MP2_FLARE_NAMES_COMMON
from max_payne_maya.mp2nodes.mp2_node_locator import MP2NodeLocator, MP2NodeLocatorDrawData, MP2NodeLocatorDrawOverride


class MP2NodeFlare(MP2NodeLocator):
    NODE_ID = OpenMaya.MTypeId(MP2_FLARE_NODE_ID)
    NODE_NAME = MP2_FLARE_NODE_NAME

    FlareNameCustomAttr = OpenMaya.MObject()
    FlareNameCommonAttr = OpenMaya.MObject()
    FlareNameUseCustomAttr = OpenMaya.MObject()

    @classmethod
    def drawOverrideCreator(cls):
        return MP2NodeFlareDrawOverride.creator

    @classmethod
    def initializer(cls):
        super().initializer()
        create_attr_numeric(cls, "FlareNameUseCustomAttr", 'na_flareNameUseCustom', OpenMaya.MFnNumericData.kBoolean,0)
        create_attr_string(cls, "FlareNameCustomAttr", 'na_flareNameCustom', MP2_FLARE_NAMES_COMMON[0])
        create_attr_enum(cls, "FlareNameCommonAttr", 'na_flareNameCommon', MP2_FLARE_NAMES_COMMON)


class MP2NodeFlareDrawData(MP2NodeLocatorDrawData):
    COLOR = (0.9, 0.9, 0.5, 0.25)
    TEXT_COLOR = (0.9, 0.9, 0.5)
    RADIUS = 0.5
    LABEL = MP2NodeFlare.NODE_NAME


class MP2NodeFlareDrawOverride(MP2NodeLocatorDrawOverride):
    def getDataClass(self):
        return MP2NodeFlareDrawData
