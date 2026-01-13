import maya.api.OpenMaya as OpenMaya
import maya.api.OpenMayaRender as OpenMayaRender
import maya.api.OpenMayaUI as OpenMayaUI
import maya.cmds as cmds

from max_payne_maya.mp2nodes.mp2_fsm_ui import MP2FSMDialog
from max_payne_maya.mp2nodes.mp2_node_ids import MP2_TRIGGER_NODE_ID, MP2_TRIGGER_NODE_NAME


# {
#     "states": {
#         "test": {
#             "AlwaysSendBefore": [],
#             "AlwaysSendAfter": [],
#             "StateSpecific": {
#                 "state_name": []
#             }
#         }
#     },
#     "default_state": "none",
#     "custom_events": [],
#     "standart_events": {
#         "Startup": {
#             "AlwaysSendBefore": [],
#             "AlwaysSendAfter": []
#         }
#     },
#     "timers": {
#         "timer": {
#             "isRealTime": 1,
#             "TimerLength": 1
#
#         }
#     }
# }

class MP2NodeTrigger(OpenMayaUI.MPxLocatorNode):
    NODE_ID = OpenMaya.MTypeId(MP2_TRIGGER_NODE_ID)
    NODE_NAME = MP2_TRIGGER_NODE_NAME
    NODE_DRAW_CLASSIFICATION = 'drawdb/geometry/MP2NodeTrigger'
    NODE_DRAW_REGISTRANT_ID = 'MP2NodeTriggerDrawRegistrantID'
    DEFAULT_FSM_VALUE = '{"states":{},"default_state":{},"custom_events":{},"events":{"always_send_before":[], "always_send_after":[]"},"timers":{},"animations":{}}'

    HiddenAttr = OpenMaya.MObject()
    ExcludeFromGameAttr = OpenMaya.MObject()
    ExcludeFromLightingAttr = OpenMaya.MObject()
    EnableExportRegroupingAttr = OpenMaya.MObject()

    RadiusAttr = OpenMaya.MObject()
    TriggerPlayerAttr = OpenMaya.MObject()
    TriggerUseAttr = OpenMaya.MObject()
    TriggerEnemyAttr = OpenMaya.MObject()
    TriggerBulletAttr = OpenMaya.MObject()
    TriggerLookAtAttr = OpenMaya.MObject()
    TriggerVisibilityAttr = OpenMaya.MObject()
    ActivatorsAnimationCustomAttr = OpenMaya.MObject()
    ActivatorsAnimationCommonAttr = OpenMaya.MObject()
    ActivatorsAnimationUseCustomAttr = OpenMaya.MObject()
    TriggerFSMAttr = OpenMaya.MObject()

    @staticmethod
    def creator():
        return MP2NodeTrigger()

    @staticmethod
    def initializer():
        MP2NodeTrigger.create_base_attr()

        MP2NodeTrigger.create_radius_attr()

        MP2NodeTrigger.create_player_attr()

        MP2NodeTrigger.create_use_attr()

        MP2NodeTrigger.create_enemy_attr()

        MP2NodeTrigger.create_bullet_atr()

        MP2NodeTrigger.create_look_at_attr()

        MP2NodeTrigger.create_visibility_attr()

        MP2NodeTrigger.create_use_animation_attr()

        MP2NodeTrigger.create_fsm_attr()

    @staticmethod
    def create_fsm_attr():
        fsm_string = OpenMaya.MFnStringData().create(MP2NodeTrigger.DEFAULT_FSM_VALUE)
        fsm_attr = OpenMaya.MFnTypedAttribute()
        MP2NodeTrigger.TriggerFSMAttr = fsm_attr.create("na_fsm", "na_fsm", OpenMaya.MFnData.kString, fsm_string)
        fsm_attr.hidden = False
        fsm_attr.keyable = False
        fsm_attr.writable = True
        fsm_attr.storable = True
        MP2NodeTrigger.addAttribute(MP2NodeTrigger.TriggerFSMAttr)

    @staticmethod
    def create_use_animation_attr():
        animation_name_use_custom = OpenMaya.MFnNumericAttribute()
        MP2NodeTrigger.ActivatorsAnimationUseCustomAttr = animation_name_use_custom.create(
            "na_activatorsAnimationUseCustom", "na_activatorsAnimationUseCustom", OpenMaya.MFnNumericData.kBoolean,
            False)
        animation_name_use_custom.hidden = False
        animation_name_use_custom.keyable = False
        animation_name_use_custom.writable = True
        animation_name_use_custom.storable = True
        MP2NodeTrigger.addAttribute(MP2NodeTrigger.ActivatorsAnimationUseCustomAttr)

        animation_name_string_custom = OpenMaya.MFnStringData().create("Default")
        animation_name_custom_attr = OpenMaya.MFnTypedAttribute()
        MP2NodeTrigger.ActivatorsAnimationCustomAttr = animation_name_custom_attr.create("na_activatorsAnimationCustom",
                                                                                         "na_activatorsAnimationCustom",
                                                                                         OpenMaya.MFnData.kString,
                                                                                         animation_name_string_custom)
        animation_name_custom_attr.hidden = False
        animation_name_custom_attr.keyable = False
        animation_name_custom_attr.writable = True
        animation_name_custom_attr.storable = True
        MP2NodeTrigger.addAttribute(MP2NodeTrigger.ActivatorsAnimationCustomAttr)

        animation_name_common_attr = OpenMaya.MFnEnumAttribute()
        MP2NodeTrigger.ActivatorsAnimationCommonAttr = animation_name_common_attr.create("na_activatorsAnimationCommon",
                                                                                         "na_activatorsAnimationCommon",
                                                                                         0)
        animation_name_common_attr.addField("Default", 0)
        animation_name_common_attr.addField("Default1", 1)
        animation_name_common_attr.addField("Default2", 2)
        animation_name_common_attr.addField("Default3", 3)
        animation_name_common_attr.addField("Default4", 4)
        animation_name_common_attr.addField("Default5", 5)
        animation_name_common_attr.hidden = False
        animation_name_common_attr.keyable = False
        animation_name_common_attr.writable = True
        animation_name_common_attr.storable = True
        MP2NodeTrigger.addAttribute(MP2NodeTrigger.ActivatorsAnimationCommonAttr)

    @staticmethod
    def create_visibility_attr():
        visibility_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeTrigger.TriggerVisibilityAttr = visibility_attr.create("na_visibility", "na_visibility",
                                                                      OpenMaya.MFnNumericData.kBoolean, 0)
        visibility_attr.hidden = False
        visibility_attr.keyable = False
        visibility_attr.writable = True
        visibility_attr.storable = True
        MP2NodeTrigger.addAttribute(MP2NodeTrigger.TriggerVisibilityAttr)

    @staticmethod
    def create_look_at_attr():
        lookat_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeTrigger.TriggerLookAtAttr = lookat_attr.create("na_lookAt", "na_lookAt",
                                                              OpenMaya.MFnNumericData.kBoolean, 0)
        lookat_attr.hidden = False
        lookat_attr.keyable = False
        lookat_attr.writable = True
        lookat_attr.storable = True
        MP2NodeTrigger.addAttribute(MP2NodeTrigger.TriggerLookAtAttr)

    @staticmethod
    def create_bullet_atr():
        bullet_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeTrigger.TriggerBulletAttr = bullet_attr.create("na_bullet", "na_bullet",
                                                              OpenMaya.MFnNumericData.kBoolean, 0)
        bullet_attr.hidden = False
        bullet_attr.keyable = False
        bullet_attr.writable = True
        bullet_attr.storable = True
        MP2NodeTrigger.addAttribute(MP2NodeTrigger.TriggerBulletAttr)

    @staticmethod
    def create_enemy_attr():
        enemy_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeTrigger.TriggerEnemyAttr = enemy_attr.create("na_enemy", "na_enemy", OpenMaya.MFnNumericData.kBoolean, 0)
        enemy_attr.hidden = False
        enemy_attr.keyable = False
        enemy_attr.writable = True
        enemy_attr.storable = True
        MP2NodeTrigger.addAttribute(MP2NodeTrigger.TriggerEnemyAttr)

    @staticmethod
    def create_use_attr():
        us_eattr = OpenMaya.MFnNumericAttribute()
        MP2NodeTrigger.TriggerUseAttr = us_eattr.create("na_use", "na_use", OpenMaya.MFnNumericData.kBoolean, 0)
        us_eattr.hidden = False
        us_eattr.keyable = False
        us_eattr.writable = True
        us_eattr.storable = True
        MP2NodeTrigger.addAttribute(MP2NodeTrigger.TriggerUseAttr)

    @staticmethod
    def create_player_attr():
        player_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeTrigger.TriggerPlayerAttr = player_attr.create("na_player", "na_player",
                                                              OpenMaya.MFnNumericData.kBoolean, 0)
        player_attr.hidden = False
        player_attr.keyable = False
        player_attr.writable = True
        player_attr.storable = True
        MP2NodeTrigger.addAttribute(MP2NodeTrigger.TriggerPlayerAttr)

    @staticmethod
    def create_radius_attr():
        radius_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeTrigger.RadiusAttr = radius_attr.create("na_radius", "na_radius", OpenMaya.MFnNumericData.kFloat, 0.5)
        radius_attr.hidden = False
        radius_attr.keyable = False
        radius_attr.writable = True
        radius_attr.storable = True
        MP2NodeTrigger.addAttribute(MP2NodeTrigger.RadiusAttr)

    @staticmethod
    def create_base_attr():
        hidden_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeTrigger.HiddenAttr = hidden_attr.create("na_hidden", "na_hidden", OpenMaya.MFnNumericData.kBoolean, 0)
        hidden_attr.hidden = False
        hidden_attr.keyable = False
        hidden_attr.writable = True
        hidden_attr.storable = True
        MP2NodeTrigger.addAttribute(MP2NodeTrigger.HiddenAttr)

        exclude_from_game_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeTrigger.ExcludeFromGameAttr = exclude_from_game_attr.create("na_excludeFromGame", "na_excludeFromGame",
                                                                           OpenMaya.MFnNumericData.kBoolean, 0)
        exclude_from_game_attr.hidden = False
        exclude_from_game_attr.keyable = False
        exclude_from_game_attr.writable = True
        exclude_from_game_attr.storable = True
        MP2NodeTrigger.addAttribute(MP2NodeTrigger.ExcludeFromGameAttr)

        exclude_from_lighting_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeTrigger.ExcludeFromLightingAttr = exclude_from_lighting_attr.create("na_excludeFromLighting",
                                                                                   "na_excludeFromLighting",
                                                                                   OpenMaya.MFnNumericData.kBoolean, 0)
        exclude_from_lighting_attr.hidden = False
        exclude_from_lighting_attr.keyable = False
        exclude_from_lighting_attr.writable = True
        exclude_from_lighting_attr.storable = True
        MP2NodeTrigger.addAttribute(MP2NodeTrigger.ExcludeFromLightingAttr)

        enable_export_regrouping_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeTrigger.EnableExportRegroupingAttr = enable_export_regrouping_attr.create("na_enableExportRegrouping",
                                                                                         "na_enableExportRegrouping",
                                                                                         OpenMaya.MFnNumericData.kBoolean,
                                                                                         0)
        enable_export_regrouping_attr.hidden = False
        enable_export_regrouping_attr.keyable = False
        enable_export_regrouping_attr.writable = True
        enable_export_regrouping_attr.storable = True
        MP2NodeTrigger.addAttribute(MP2NodeTrigger.EnableExportRegroupingAttr)

    def __init__(self):
        OpenMayaUI.MPxLocatorNode.__init__(self)

    def compute(self, plug, dataBlock):
        pass

    @staticmethod
    def perform_edit_fsm_action(node_name):
        print(f"{node_name} value")

        node_only = node_name.split('.')[0]
        try:
            sel = OpenMaya.MSelectionList()
            sel.add(node_only)
            node = sel.getDependNode(0)
        except:
            return

        my_node = OpenMaya.MFnDependencyNode(node)
        if my_node:
            fsm_edit_widow = MP2FSMDialog(my_node, "na_fsm")
            fsm_edit_widow.show()

        # plug = fnNode.findPlug("na_fsm", False)
        # old_val = plug.asString()
        # plug.setString("qqwe2")
        # print(f"{node_name} value changed from {old_val}")

        # 3. Retrieve the Python class instance (MPxNode proxy)
        # This returns your actual custom class (e.g., MyCustomNode instance)
        # node_instance = OpenMaya.MPxNode.getInternalData(node)
        # if node_instance:
        #     node_instance.run_fsm_editor()


class MP2NodeTriggerDrawData(OpenMaya.MUserData):
    def __init__(self):
        OpenMaya.MUserData.__init__(self, False)

        self.radius = 0.5
        self.text_color = OpenMaya.MColor((0.12, 0.25, 0.25))
        self.text_center = OpenMaya.MPoint((0.0, self.radius + 0.2, 0.0))
        self.color = OpenMaya.MColor((0.12, 0.25, 0.25, 0.25))
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
        plug = OpenMaya.MPlug(objPath.node(), MP2NodeTrigger.RadiusAttr)
        if not plug.isNull:
            data.radius = plug.asFloat()
            data.updateTextPosition()
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
