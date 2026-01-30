import maya.api.OpenMaya as OpenMaya
from max_payne_maya.mp2nodes.mp2_attr_util import create_attr_string, create_attr_numeric, create_attr_enum
from max_payne_maya.mp2nodes.mp2_node_ids import MP2_TRIGGER_NODE_ID, MP2_TRIGGER_NODE_NAME, MP2_USE_ACTIVATE_ANIMATIONS
from max_payne_maya.mp2nodes.mp2_node_locator import MP2NodeLocator, MP2NodeLocatorDrawData, MP2NodeLocatorDrawOverride


class MP2NodeTrigger(MP2NodeLocator):
    NODE_ID = OpenMaya.MTypeId(MP2_TRIGGER_NODE_ID)
    NODE_NAME = MP2_TRIGGER_NODE_NAME

    FSMAttr = OpenMaya.MObject()
    RadiusAttr = []
    TriggerPlayerAttr = OpenMaya.MObject()
    TriggerUseAttr = OpenMaya.MObject()
    TriggerEnemyAttr = OpenMaya.MObject()
    TriggerBulletAttr = OpenMaya.MObject()
    TriggerLookAtAttr = OpenMaya.MObject()
    TriggerVisibilityAttr = OpenMaya.MObject()
    ActivatorsAnimationCustomAttr = OpenMaya.MObject()
    ActivatorsAnimationCommonAttr = OpenMaya.MObject()
    ActivatorsAnimationUseCustomAttr = OpenMaya.MObject()

    @classmethod
    def drawOverrideCreator(cls):
        return MP2NodeTriggerDrawOverride.creator

    @classmethod
    def initializer(cls):
        super().initializer()
        create_attr_string(cls, "FSMAttr", 'na_fsm', '')

        create_attr_numeric(cls, "ActivatorsAnimationUseCustomAttr", 'na_activatorsAnimationUseCustom', OpenMaya.MFnNumericData.kBoolean, 0)
        create_attr_string(cls, "ActivatorsAnimationCustomAttr", 'na_activatorsAnimationCustom', MP2_USE_ACTIVATE_ANIMATIONS[0])
        create_attr_enum(cls, "ActivatorsAnimationCommonAttr", 'na_activatorsAnimationCommon', MP2_USE_ACTIVATE_ANIMATIONS)

        create_attr_numeric(cls, "TriggerVisibilityAttr", 'na_visibility', OpenMaya.MFnNumericData.kBoolean, 0)
        create_attr_numeric(cls, "TriggerLookAtAttr", 'na_lookAt', OpenMaya.MFnNumericData.kBoolean, 0)
        create_attr_numeric(cls, "TriggerBulletAttr", 'na_bullet', OpenMaya.MFnNumericData.kBoolean, 0)
        create_attr_numeric(cls, "TriggerEnemyAttr", 'na_enemy', OpenMaya.MFnNumericData.kBoolean, 0)
        create_attr_numeric(cls, "TriggerUseAttr", 'na_use', OpenMaya.MFnNumericData.kBoolean, 0)
        create_attr_numeric(cls, "TriggerPlayerAttr", 'na_player', OpenMaya.MFnNumericData.kBoolean, 0)
        create_attr_numeric(cls, "RadiusAttr", 'na_radius', OpenMaya.MFnNumericData.kFloat, 0.5)


class MP2NodeTriggerDrawData(MP2NodeLocatorDrawData):
    COLOR = (0.12, 0.25, 0.25, 0.25)
    TEXT_COLOR = (0.12, 0.25, 0.25)
    RADIUS = 0.5
    LABEL = MP2NodeTrigger.NODE_NAME


class MP2NodeTriggerDrawOverride(MP2NodeLocatorDrawOverride):
    def getDataClass(self):
        return MP2NodeTriggerDrawData

    def updateData(self, data, objPath, cameraPath, frameContext, oldData):
        plug = OpenMaya.MPlug(objPath.node(), MP2NodeTrigger.RadiusAttr)
        if not plug.isNull:
            data.setRadius(plug.asFloat())

