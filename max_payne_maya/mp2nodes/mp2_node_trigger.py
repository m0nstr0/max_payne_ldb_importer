import maya.OpenMayaMPx as OpenMayaMPx
import maya.api.OpenMaya as OpenMaya
import maya.api.OpenMayaRender as OpenMayaRender
import maya.api.OpenMayaUI as OpenMayaUI
import maya.cmds as cmds

from max_payne_maya.mp2nodes.mp2_node_ids import MP2_TRIGGER_NODE_ID, MP2_TRIGGER_NODE_NAME


class MP2NodeTrigger(OpenMayaUI.MPxLocatorNode):
    NODE_ID = OpenMaya.MTypeId(MP2_TRIGGER_NODE_ID)
    NODE_NAME = MP2_TRIGGER_NODE_NAME
    NODE_DRAW_CLASSIFICATION = 'drawdb/geometry/MP2NodeTrigger'
    NODE_DRAW_REGISTRANT_ID = 'MP2NodeTriggerDrawRegistrantID'

    HiddenAttr = OpenMaya.MObject()
    ExcludeFromGameAttr = OpenMaya.MObject()
    ExcludeFromLightingAttr = OpenMaya.MObject()
    EnableExportRegroupingAttr = OpenMaya.MObject()

    TriggerPlayerAttr = OpenMaya.MObject()
    TriggerUseAttr = OpenMaya.MObject()
    TriggerEnemyAttr = OpenMaya.MObject()
    TriggerBulletAttr = OpenMaya.MObject()
    TriggerLookAtAttr = OpenMaya.MObject()
    TriggerVisibilityAttr = OpenMaya.MObject()
    ActivatorsUseAnimation = OpenMaya.MObject()

    @staticmethod
    def creator():
        return MP2NodeTrigger()

    @staticmethod
    def initializer():
        MP2NodeTrigger.initializeBaseAttributes()

        player_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeTrigger.TriggerPlayerAttr = player_attr.create("Player", "Player", OpenMaya.MFnNumericData.kBoolean, 0)
        player_attr.hidden = False
        player_attr.keyable = False
        player_attr.writable = True
        player_attr.storable = True
        MP2NodeTrigger.addAttribute(MP2NodeTrigger.TriggerPlayerAttr)

        us_eattr = OpenMaya.MFnNumericAttribute()
        MP2NodeTrigger.TriggerUseAttr = us_eattr.create("Use", "Use", OpenMaya.MFnNumericData.kBoolean, 0)
        us_eattr.hidden = False
        us_eattr.keyable = False
        us_eattr.writable = True
        us_eattr.storable = True
        MP2NodeTrigger.addAttribute(MP2NodeTrigger.TriggerUseAttr)

        enemy_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeTrigger.TriggerEnemyAttr = enemy_attr.create("Enemy", "Enemy", OpenMaya.MFnNumericData.kBoolean, 0)
        enemy_attr.hidden = False
        enemy_attr.keyable = False
        enemy_attr.writable = True
        enemy_attr.storable = True
        MP2NodeTrigger.addAttribute(MP2NodeTrigger.TriggerEnemyAttr)

        bullet_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeTrigger.TriggerBulletAttr = bullet_attr.create("Bullet", "Bullet", OpenMaya.MFnNumericData.kBoolean, 0)
        bullet_attr.hidden = False
        bullet_attr.keyable = False
        bullet_attr.writable = True
        bullet_attr.storable = True
        MP2NodeTrigger.addAttribute(MP2NodeTrigger.TriggerBulletAttr)

        lookat_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeTrigger.TriggerLookAtAttr = lookat_attr.create("LookAt", "LookAt", OpenMaya.MFnNumericData.kBoolean, 0)
        lookat_attr.hidden = False
        lookat_attr.keyable = False
        lookat_attr.writable = True
        lookat_attr.storable = True
        MP2NodeTrigger.addAttribute(MP2NodeTrigger.TriggerLookAtAttr)

        visibility_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeTrigger.TriggerVisibilityAttr = visibility_attr.create("Visibility", "Visibility", OpenMaya.MFnNumericData.kBoolean, 0)
        visibility_attr.hidden = False
        visibility_attr.keyable = False
        visibility_attr.writable = True
        visibility_attr.storable = True
        MP2NodeTrigger.addAttribute(MP2NodeTrigger.TriggerVisibilityAttr)

        animation_name_string = OpenMaya.MFnStringData().create("Ammo_Beretta")
        animation_name_attr = OpenMaya.MFnTypedAttribute()
        MP2NodeTrigger.ActivatorsUseAnimation = animation_name_attr.create("ActivatorsUseAnimation", "ActivatorsUseAnimation", OpenMaya.MFnData.kString, animation_name_string)
        animation_name_attr.hidden = False
        animation_name_attr.keyable = False
        animation_name_attr.writable = True
        animation_name_attr.storable = True
        MP2NodeTrigger.addAttribute(MP2NodeTrigger.ActivatorsUseAnimation)

    @staticmethod
    def initializeBaseAttributes():
        hidden_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeTrigger.HiddenAttr = hidden_attr.create("Hidden", "Hidden", OpenMaya.MFnNumericData.kBoolean, 0)
        hidden_attr.hidden = False
        hidden_attr.keyable = False
        hidden_attr.writable = True
        hidden_attr.storable = True
        MP2NodeTrigger.addAttribute(MP2NodeTrigger.HiddenAttr)

        exclude_from_game_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeTrigger.ExcludeFromGameAttr = exclude_from_game_attr.create("ExcludeFromGame", "ExcludeFromGame",
                                                                  OpenMaya.MFnNumericData.kBoolean, 0)
        exclude_from_game_attr.hidden = False
        exclude_from_game_attr.keyable = False
        exclude_from_game_attr.writable = True
        exclude_from_game_attr.storable = True
        MP2NodeTrigger.addAttribute(MP2NodeTrigger.ExcludeFromGameAttr)

        exclude_from_lighting_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeTrigger.ExcludeFromLightingAttr = exclude_from_lighting_attr.create("ExcludeFromLighting", "ExcludeFromLighting",
                                                                      OpenMaya.MFnNumericData.kBoolean, 0)
        exclude_from_lighting_attr.hidden = False
        exclude_from_lighting_attr.keyable = False
        exclude_from_lighting_attr.writable = True
        exclude_from_lighting_attr.storable = True
        MP2NodeTrigger.addAttribute(MP2NodeTrigger.ExcludeFromLightingAttr)

        enable_export_regrouping_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeTrigger.EnableExportRegroupingAttr = enable_export_regrouping_attr.create("EnableExportRegrouping",
                                                                         "EnableExportRegrouping",
                                                                         OpenMaya.MFnNumericData.kBoolean, 0)
        enable_export_regrouping_attr.hidden = False
        enable_export_regrouping_attr.keyable = False
        enable_export_regrouping_attr.writable = True
        enable_export_regrouping_attr.storable = True
        MP2NodeTrigger.addAttribute(MP2NodeTrigger.EnableExportRegroupingAttr)

    def __init__(self):
        OpenMayaUI.MPxLocatorNode.__init__(self)

    def compute(self, plug, dataBlock):
        pass


class MP2NodeTriggerDrawData(OpenMaya.MUserData):
    def __init__(self):
        OpenMaya.MUserData.__init__(self, False)

        self.text_color = OpenMaya.MColor((0.12, 0.25, 0.25))
        if cmds.upAxis(q=True, axis=True) == 'y':
            self.text_center = OpenMaya.MPoint((0.0, 0.7, 0.0))
        else:
            self.text_center = OpenMaya.MPoint((0.0, 0.0, 0.7))
        self.color = OpenMaya.MColor((0.12, 0.25, 0.25, 0.25))
        self.center = OpenMaya.MPoint(0.0, 0.0, 0.0)
        self.radius = 0.5
        self.subdivisionsAxis = 10
        self.subdivisionsHeight = 10
        self.filled = True


class MP2NodeTriggerDrawOverride(OpenMayaRender.MPxDrawOverride):

    @staticmethod
    def creator(obj):
        return MP2NodeTriggerDrawOverride(obj)

    def __init__(self, obj):
        OpenMayaRender.MPxDrawOverride.__init__(self, obj, None, False)

    def supportedDrawAPIs(self):
        return OpenMayaRender.MRenderer.kAllDevices

    def prepareForDraw(self, objPath, cameraPath, frameContext, oldData):
        data = oldData if isinstance(oldData, MP2NodeTriggerDrawData) else MP2NodeTriggerDrawData()
        return data

    def hasUIDrawables(self):
        return True

    def addUIDrawables(self, objPath, drawManager, frameContext, data):
        if not isinstance(data, MP2NodeTriggerDrawData):
            return

        drawManager.beginDrawable()
        drawManager.setColor(data.color)
        drawManager.sphere(data.center, data.radius, data.subdivisionsAxis, data.subdivisionsHeight, data.filled)
        drawManager.setColor(data.text_color)
        drawManager.text(data.text_center, 'MP2_Trigger', OpenMayaRender.MUIDrawManager.kCenter)
        drawManager.endDrawable()
