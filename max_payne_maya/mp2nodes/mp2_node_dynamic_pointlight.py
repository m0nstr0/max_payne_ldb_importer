import maya.api.OpenMaya as OpenMaya
from max_payne_maya.mp2nodes.mp2_attr_util import create_attr_numeric, create_color_attr
from max_payne_maya.mp2nodes.mp2_node_ids import  MP2_DYNAMIC_POINT_LIGHT_NODE_ID, MP2_DYNAMIC_POINT_LIGHT_NODE_NAME
from max_payne_maya.mp2nodes.mp2_node_locator import MP2NodeLocator, MP2NodeLocatorDrawData, MP2NodeLocatorDrawOverride


class MP2NodeDynamicPointLight(MP2NodeLocator):
    NODE_ID = OpenMaya.MTypeId(MP2_DYNAMIC_POINT_LIGHT_NODE_ID)
    NODE_NAME = MP2_DYNAMIC_POINT_LIGHT_NODE_NAME

    IntensityAttr = OpenMaya.MObject()
    FalloffAttr = OpenMaya.MObject()
    ColorAttr = OpenMaya.MObject()

    @classmethod
    def drawOverrideCreator(cls):
        return MP2NodeDynamicPointLightDrawOverride.creator

    @classmethod
    def initializer(cls):
        super().initializer()

        create_attr_numeric(cls, 'IntensityAttr', 'na_intensity', OpenMaya.MFnNumericData.kFloat, 1.0)
        create_attr_numeric(cls, 'FalloffAttr', 'na_falloff', OpenMaya.MFnNumericData.kFloat, 10.0)
        create_color_attr(cls, "ColorAttr", 'na_color')


class MP2NodeDynamicPointLightDrawData(MP2NodeLocatorDrawData):
    COLOR = (1.0, 1.0, 1.0, 0.25)
    TEXT_COLOR = (1.0, 1.0, 1.0)
    RADIUS = 0.5
    LABEL = MP2NodeDynamicPointLight.NODE_NAME


class MP2NodeDynamicPointLightDrawOverride(MP2NodeLocatorDrawOverride):
    def getDataClass(self):
        return MP2NodeDynamicPointLightDrawData

