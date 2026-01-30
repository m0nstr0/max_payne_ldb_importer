import maya.api.OpenMaya as OpenMaya
from max_payne_maya.mp2nodes.mp2_attr_util import create_attr_string, create_attr_numeric, create_attr_enum
from max_payne_maya.mp2nodes.mp2_node_ids import MP2_ENEMY_NODE_ID, MP2_ENEMY_NODE_NAME, MP2_USE_ACTIVATE_ANIMATIONS, \
    MP2_ENEMY_NAMES_COMMON, MP2_DEFAULT_PLAYER_GROUPS
from max_payne_maya.mp2nodes.mp2_node_locator import MP2NodeLocator, MP2NodeLocatorDrawData, MP2NodeLocatorDrawOverride


class MP2NodeEnemy(MP2NodeLocator):
    NODE_ID = OpenMaya.MTypeId(MP2_ENEMY_NODE_ID)
    NODE_NAME = MP2_ENEMY_NODE_NAME

    FSMAttr = OpenMaya.MObject()
    EnemyGroupAttr = OpenMaya.MObject()
    SkinCommonAttr = OpenMaya.MObject()
    SkinCustomAttr = OpenMaya.MObject()
    SkinUseCustomAttr = OpenMaya.MObject()

    ActivatorsAnimationUseCustomAttr = OpenMaya.MObject()
    ActivatorsAnimationCustomAttr = OpenMaya.MObject()
    ActivatorsAnimationCommonAttr = OpenMaya.MObject()

    @classmethod
    def drawOverrideCreator(cls):
        return MP2NodeEnemyDrawOverride.creator

    @classmethod
    def initializer(cls):
        super().initializer()
        create_attr_string(cls, "FSMAttr", 'na_fsm', '')

        create_attr_numeric(cls, "ActivatorsAnimationUseCustomAttr", 'na_activatorsAnimationUseCustom', OpenMaya.MFnNumericData.kBoolean, 0)
        create_attr_string(cls, "ActivatorsAnimationCustomAttr", 'na_activatorsAnimationCustom', MP2_USE_ACTIVATE_ANIMATIONS[0])
        create_attr_enum(cls, "ActivatorsAnimationCommonAttr", 'na_activatorsAnimationCommon', MP2_USE_ACTIVATE_ANIMATIONS)

        create_attr_numeric(cls, "SkinUseCustomAttr", 'na_skinUseCustom', OpenMaya.MFnNumericData.kBoolean, 0)
        create_attr_string(cls, "SkinCustomAttr", 'na_skinCustom', MP2_ENEMY_NAMES_COMMON[0])
        create_attr_enum(cls, "SkinCommonAttr", 'na_skinCommon', MP2_ENEMY_NAMES_COMMON)

        create_attr_enum(cls, "EnemyGroupAttr", 'na_enemyGroup', MP2_DEFAULT_PLAYER_GROUPS)


class MP2NodeEnemyDrawData(MP2NodeLocatorDrawData):
    COLOR = (0.0, 1.0, 1.0, 0.25)
    TEXT_COLOR = (0.0, 1.0, 1.0)
    RADIUS = 0.5
    LABEL = MP2NodeEnemy.NODE_NAME


class MP2NodeEnemyDrawOverride(MP2NodeLocatorDrawOverride):
    def getDataClass(self):
        return MP2NodeEnemyDrawData

