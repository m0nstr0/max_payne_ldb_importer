import maya.api.OpenMaya as OpenMaya
import maya.api.OpenMayaRender as OpenMayaRender
import maya.api.OpenMayaUI as OpenMayaUI
import maya.cmds as cmds

from max_payne_maya.mp2nodes.mp2_node_ids import MP2_ENEMY_NODE_ID, MP2_ENEMY_NODE_NAME, MP2_USE_ACTIVATE_ANIMATIONS, \
    MP2_ENEMY_NAMES_COMMON, MP2_DEFAULT_PLAYER_GROUPS


class MP2NodeEnemy(OpenMayaUI.MPxLocatorNode):
    NODE_ID = OpenMaya.MTypeId(MP2_ENEMY_NODE_ID)
    NODE_NAME = MP2_ENEMY_NODE_NAME
    NODE_DRAW_CLASSIFICATION = 'drawdb/geometry/MP2NodeEnemy'
    NODE_DRAW_REGISTRANT_ID = 'MP2NodeEnemyDrawRegistrantID'
    DEFAULT_FSM_VALUE = '{"states":{},"default_state":{},"custom_events":{},"events":{"always_send_before":[], "always_send_after":[]"},"timers":{},"animations":{}}'

    HiddenAttr = OpenMaya.MObject()
    ExcludeFromGameAttr = OpenMaya.MObject()
    ExcludeFromLightingAttr = OpenMaya.MObject()
    EnableExportRegroupingAttr = OpenMaya.MObject()

    RadiusAttr = OpenMaya.MObject()
    EnemyPlayerAttr = OpenMaya.MObject()
    EnemyUseAttr = OpenMaya.MObject()
    EnemyEnemyAttr = OpenMaya.MObject()
    EnemyBulletAttr = OpenMaya.MObject()
    EnemyLookAtAttr = OpenMaya.MObject()
    EnemyVisibilityAttr = OpenMaya.MObject()
    EnemyGroup = OpenMaya.MObject()
    FSMAttr = OpenMaya.MObject()
    SkinCommonAttr = OpenMaya.MObject()
    SkinCustomAttr = OpenMaya.MObject()
    SkinUseCustomAttr = OpenMaya.MObject()
    @staticmethod
    def creator():
        return MP2NodeEnemy()

    @staticmethod
    def initializer():
        MP2NodeEnemy.create_base_attr()

        MP2NodeEnemy.create_use_animation_attr()

        MP2NodeEnemy.create_fsm_attr()

        MP2NodeEnemy.create_skin_attr()

        MP2NodeEnemy.create_enemy_group_attr()

    @staticmethod
    def create_fsm_attr():
        fsm_string = OpenMaya.MFnStringData().create(MP2NodeEnemy.DEFAULT_FSM_VALUE)
        fsm_attr = OpenMaya.MFnTypedAttribute()
        MP2NodeEnemy.FSMAttr = fsm_attr.create("na_fsm", "na_fsm", OpenMaya.MFnData.kString, fsm_string)
        fsm_attr.hidden = False
        fsm_attr.keyable = False
        fsm_attr.writable = True
        fsm_attr.storable = True
        MP2NodeEnemy.addAttribute(MP2NodeEnemy.FSMAttr)

    @staticmethod
    def create_use_animation_attr():
        animation_name_use_custom = OpenMaya.MFnNumericAttribute()
        MP2NodeEnemy.ActivatorsAnimationUseCustomAttr = animation_name_use_custom.create(
            "na_activatorsAnimationUseCustom", "na_activatorsAnimationUseCustom", OpenMaya.MFnNumericData.kBoolean,
            False)
        animation_name_use_custom.hidden = False
        animation_name_use_custom.keyable = False
        animation_name_use_custom.writable = True
        animation_name_use_custom.storable = True
        MP2NodeEnemy.addAttribute(MP2NodeEnemy.ActivatorsAnimationUseCustomAttr)

        animation_name_string_custom = OpenMaya.MFnStringData().create(MP2_USE_ACTIVATE_ANIMATIONS[0])
        animation_name_custom_attr = OpenMaya.MFnTypedAttribute()
        MP2NodeEnemy.ActivatorsAnimationCustomAttr = animation_name_custom_attr.create("na_activatorsAnimationCustom",
                                                                                         "na_activatorsAnimationCustom",
                                                                                         OpenMaya.MFnData.kString,
                                                                                         animation_name_string_custom)
        animation_name_custom_attr.hidden = False
        animation_name_custom_attr.keyable = False
        animation_name_custom_attr.writable = True
        animation_name_custom_attr.storable = True
        MP2NodeEnemy.addAttribute(MP2NodeEnemy.ActivatorsAnimationCustomAttr)

        animation_name_common_attr = OpenMaya.MFnEnumAttribute()
        MP2NodeEnemy.ActivatorsAnimationCommonAttr = animation_name_common_attr.create("na_activatorsAnimationCommon",
                                                                                         "na_activatorsAnimationCommon",
                                                                                         0)

        for i in range(len(MP2_USE_ACTIVATE_ANIMATIONS)):
            animation_name_common_attr.addField(MP2_USE_ACTIVATE_ANIMATIONS[i], i)

        animation_name_common_attr.hidden = False
        animation_name_common_attr.keyable = False
        animation_name_common_attr.writable = True
        animation_name_common_attr.storable = True
        MP2NodeEnemy.addAttribute(MP2NodeEnemy.ActivatorsAnimationCommonAttr)

    @staticmethod
    def create_skin_attr():
        skin_use_custom = OpenMaya.MFnNumericAttribute()
        MP2NodeEnemy.SkinUseCustomAttr = skin_use_custom.create("na_skinUseCustom", "na_skinUseCustom", OpenMaya.MFnNumericData.kBoolean, False)
        skin_use_custom.hidden = False
        skin_use_custom.keyable = False
        skin_use_custom.writable = True
        skin_use_custom.storable = True
        MP2NodeEnemy.addAttribute(MP2NodeEnemy.SkinUseCustomAttr)

        skin_name_string_custom = OpenMaya.MFnStringData().create(MP2_ENEMY_NAMES_COMMON[0])
        skin_name_custom_attr = OpenMaya.MFnTypedAttribute()
        MP2NodeEnemy.SkinCustomAttr = skin_name_custom_attr.create("na_skinCustom", "na_skinCustom", OpenMaya.MFnData.kString, skin_name_string_custom)
        skin_name_custom_attr.hidden = False
        skin_name_custom_attr.keyable = False
        skin_name_custom_attr.writable = True
        skin_name_custom_attr.storable = True
        MP2NodeEnemy.addAttribute(MP2NodeEnemy.SkinCustomAttr)

        skin_name_common_attr = OpenMaya.MFnEnumAttribute()
        MP2NodeEnemy.SkinCommonAttr = skin_name_common_attr.create("na_skinCommon", "na_skinCommon", 0)

        for i in range(len(MP2_ENEMY_NAMES_COMMON)):
            skin_name_common_attr.addField(MP2_ENEMY_NAMES_COMMON[i], i)

        skin_name_common_attr.hidden = False
        skin_name_common_attr.keyable = False
        skin_name_common_attr.writable = True
        skin_name_common_attr.storable = True
        MP2NodeEnemy.addAttribute(MP2NodeEnemy.SkinCommonAttr)
    @staticmethod
    def create_enemy_group_attr():
        enemy_group_attr = OpenMaya.MFnEnumAttribute()
        MP2NodeEnemy.EnemyGroup = enemy_group_attr.create("na_enemyGroup", "na_enemyGroup", 0)

        for i in range(len(MP2_DEFAULT_PLAYER_GROUPS)):
            enemy_group_attr.addField(MP2_DEFAULT_PLAYER_GROUPS[i], i)

        enemy_group_attr.hidden = False
        enemy_group_attr.keyable = False
        enemy_group_attr.writable = True
        enemy_group_attr.storable = True
        MP2NodeEnemy.addAttribute(MP2NodeEnemy.EnemyGroup)

    @staticmethod
    def create_base_attr():
        hidden_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeEnemy.HiddenAttr = hidden_attr.create("na_hidden", "na_hidden", OpenMaya.MFnNumericData.kBoolean, 0)
        hidden_attr.hidden = False
        hidden_attr.keyable = False
        hidden_attr.writable = True
        hidden_attr.storable = True
        MP2NodeEnemy.addAttribute(MP2NodeEnemy.HiddenAttr)

        exclude_from_game_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeEnemy.ExcludeFromGameAttr = exclude_from_game_attr.create("na_excludeFromGame", "na_excludeFromGame",
                                                                           OpenMaya.MFnNumericData.kBoolean, 0)
        exclude_from_game_attr.hidden = False
        exclude_from_game_attr.keyable = False
        exclude_from_game_attr.writable = True
        exclude_from_game_attr.storable = True
        MP2NodeEnemy.addAttribute(MP2NodeEnemy.ExcludeFromGameAttr)

        exclude_from_lighting_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeEnemy.ExcludeFromLightingAttr = exclude_from_lighting_attr.create("na_excludeFromLighting",
                                                                                   "na_excludeFromLighting",
                                                                                   OpenMaya.MFnNumericData.kBoolean, 0)
        exclude_from_lighting_attr.hidden = False
        exclude_from_lighting_attr.keyable = False
        exclude_from_lighting_attr.writable = True
        exclude_from_lighting_attr.storable = True
        MP2NodeEnemy.addAttribute(MP2NodeEnemy.ExcludeFromLightingAttr)

        enable_export_regrouping_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeEnemy.EnableExportRegroupingAttr = enable_export_regrouping_attr.create("na_enableExportRegrouping",
                                                                                         "na_enableExportRegrouping",
                                                                                         OpenMaya.MFnNumericData.kBoolean,
                                                                                         0)
        enable_export_regrouping_attr.hidden = False
        enable_export_regrouping_attr.keyable = False
        enable_export_regrouping_attr.writable = True
        enable_export_regrouping_attr.storable = True
        MP2NodeEnemy.addAttribute(MP2NodeEnemy.EnableExportRegroupingAttr)

    def __init__(self):
        OpenMayaUI.MPxLocatorNode.__init__(self)

    def compute(self, plug, dataBlock):
        pass

class MP2NodeEnemyDrawData(OpenMaya.MUserData):
    def __init__(self):
        OpenMaya.MUserData.__init__(self, False)

        self.radius = 0.5
        self.text_color = OpenMaya.MColor((0.0, 1.0, 1.0))
        self.text_center = OpenMaya.MPoint((0.0, self.radius + 0.2, 0.0))
        self.color = OpenMaya.MColor((0.0, 1.0, 1.0, 0.25))
        self.center = OpenMaya.MPoint(0.0, 0.0, 0.0)
        self.subdivisionsAxis = 20
        self.subdivisionsHeight = 20
        self.filled = True
        self.updateTextPosition()

    def updateTextPosition(self):
        if cmds.upAxis(q=True, axis=True) == 'y':
            self.text_center = OpenMaya.MPoint((0.0, self.radius + 0.2, 0.0))
        else:
            self.text_center = OpenMaya.MPoint((0.0, 0.0, self.radius + 0.2))


class MP2NodeEnemyDrawOverride(OpenMayaRender.MPxDrawOverride):

    @staticmethod
    def creator(obj):
        return MP2NodeEnemyDrawOverride(obj)

    def __init__(self, obj):
        OpenMayaRender.MPxDrawOverride.__init__(self, obj, None, False)

    def supportedDrawAPIs(self):
        return OpenMayaRender.MRenderer.kAllDevices

    def prepareForDraw(self, objPath, cameraPath, frameContext, oldData):
        data = oldData if isinstance(oldData, MP2NodeEnemyDrawData) else MP2NodeEnemyDrawData()
        plug = OpenMaya.MPlug(objPath.node(), MP2NodeEnemy.RadiusAttr)
        if not plug.isNull:
            data.radius = plug.asFloat()
            data.updateTextPosition()
        return data

    def hasUIDrawables(self):
        return True

    def addUIDrawables(self, objPath, drawManager, frameContext, data):
        if not isinstance(data, MP2NodeEnemyDrawData):
            return

        drawManager.beginDrawable()
        drawManager.setColor(data.color)
        drawManager.sphere(data.center, data.radius, data.subdivisionsAxis, data.subdivisionsHeight, data.filled)
        drawManager.setColor(data.text_color)
        drawManager.text(data.text_center, 'MP2_Enemy', OpenMayaRender.MUIDrawManager.kCenter)
        drawManager.endDrawable()
