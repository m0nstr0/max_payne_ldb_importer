import maya.OpenMayaMPx as OpenMayaMPx
import maya.api.OpenMaya as OpenMaya
import maya.api.OpenMayaRender as OpenMayaRender
import maya.api.OpenMayaUI as OpenMayaUI
import maya.cmds as cmds

from max_payne_maya.mp2nodes.mp2_node_ids import MP2_FLARE_NODE_NAME, MP2_FLARE_NODE_ID, MP2_FLARE_NAMES_COMMON


class MP2NodeFlare(OpenMayaUI.MPxLocatorNode):
    NODE_ID = OpenMaya.MTypeId(MP2_FLARE_NODE_ID)
    NODE_NAME = MP2_FLARE_NODE_NAME
    NODE_DRAW_CLASSIFICATION = 'drawdb/geometry/MP2NodeFlare'
    NODE_DRAW_REGISTRANT_ID = 'MP2NodeFlareDrawRegistrantID'

    HiddenAttr = OpenMaya.MObject()
    ExcludeFromGameAttr = OpenMaya.MObject()
    ExcludeFromLightingAttr = OpenMaya.MObject()
    EnableExportRegroupingAttr = OpenMaya.MObject()

    FlareNameCustomAttr = OpenMaya.MObject()
    FlareNameCommonAttr = OpenMaya.MObject()
    FlareNameUseCustomAttr = OpenMaya.MObject()

    @staticmethod
    def creator():
        return MP2NodeFlare()

    @staticmethod
    def initializer():
        MP2NodeFlare.initializeBaseAttributes()

        flare_name_use_custom = OpenMaya.MFnNumericAttribute()
        MP2NodeFlare.ItemNameUseCustomAttr = flare_name_use_custom.create("na_flareNameUseCustom", "na_flareNameUseCustom", OpenMaya.MFnNumericData.kBoolean, False)
        flare_name_use_custom.hidden = False
        flare_name_use_custom.keyable = False
        flare_name_use_custom.writable = True
        flare_name_use_custom.storable = True
        MP2NodeFlare.addAttribute(MP2NodeFlare.ItemNameUseCustomAttr)

        falre_name_custom_string = OpenMaya.MFnStringData().create(MP2_FLARE_NAMES_COMMON[0])
        falre_name_custom_attr = OpenMaya.MFnTypedAttribute()
        MP2NodeFlare.FlareNameCustomAttr = falre_name_custom_attr.create("na_flareNameCustom", "na_flareNameCustom", OpenMaya.MFnData.kString, falre_name_custom_string)
        falre_name_custom_attr.hidden = False
        falre_name_custom_attr.keyable = False
        falre_name_custom_attr.writable = True
        falre_name_custom_attr.storable = True
        MP2NodeFlare.addAttribute(MP2NodeFlare.FlareNameCustomAttr)

        flare_name_common_attr = OpenMaya.MFnEnumAttribute()
        MP2NodeFlare.ItemNameCommonAttr = flare_name_common_attr.create("na_flareNameCommon", "na_flareNameCommon", 0)

        for i in range(len(MP2_FLARE_NAMES_COMMON)):
            flare_name_common_attr.addField(MP2_FLARE_NAMES_COMMON[i], i)

        flare_name_common_attr.hidden = False
        flare_name_common_attr.keyable = False
        flare_name_common_attr.writable = True
        flare_name_common_attr.storable = True
        MP2NodeFlare.addAttribute(MP2NodeFlare.ItemNameCommonAttr)

    @staticmethod
    def initializeBaseAttributes():
        hidden_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeFlare.HiddenAttr = hidden_attr.create("na_hidden", "na_hidden", OpenMaya.MFnNumericData.kBoolean, 0)
        hidden_attr.hidden = False
        hidden_attr.keyable = False
        hidden_attr.writable = True
        hidden_attr.storable = True
        MP2NodeFlare.addAttribute(MP2NodeFlare.HiddenAttr)

        exclude_from_game_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeFlare.ExcludeFromGameAttr = exclude_from_game_attr.create("na_excludeFromGame", "na_excludeFromGame",
                                                                  OpenMaya.MFnNumericData.kBoolean, 0)
        exclude_from_game_attr.hidden = False
        exclude_from_game_attr.keyable = False
        exclude_from_game_attr.writable = True
        exclude_from_game_attr.storable = True
        MP2NodeFlare.addAttribute(MP2NodeFlare.ExcludeFromGameAttr)

        exclude_from_lighting_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeFlare.ExcludeFromLightingAttr = exclude_from_lighting_attr.create("na_excludeFromLighting", "na_excludeFromLighting",
                                                                      OpenMaya.MFnNumericData.kBoolean, 0)
        exclude_from_lighting_attr.hidden = False
        exclude_from_lighting_attr.keyable = False
        exclude_from_lighting_attr.writable = True
        exclude_from_lighting_attr.storable = True
        MP2NodeFlare.addAttribute(MP2NodeFlare.ExcludeFromLightingAttr)

        enable_export_regrouping_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeFlare.EnableExportRegroupingAttr = enable_export_regrouping_attr.create("na_enableExportRegrouping",
                                                                         "na_enableExportRegrouping",
                                                                         OpenMaya.MFnNumericData.kBoolean, 0)
        enable_export_regrouping_attr.hidden = False
        enable_export_regrouping_attr.keyable = False
        enable_export_regrouping_attr.writable = True
        enable_export_regrouping_attr.storable = True
        MP2NodeFlare.addAttribute(MP2NodeFlare.EnableExportRegroupingAttr)

    def __init__(self):
        OpenMayaUI.MPxLocatorNode.__init__(self)

    def compute(self, plug, dataBlock):
        pass


class MP2NodeFlareDrawData(OpenMaya.MUserData):
    def __init__(self):
        OpenMaya.MUserData.__init__(self, False)

        self.text_color = OpenMaya.MColor((0.9, 0.9, 0.5))
        if cmds.upAxis(q=True, axis=True) == 'y':
            self.text_center = OpenMaya.MPoint((0.0, 0.45, 0.0))
        else:
            self.text_center = OpenMaya.MPoint((0.0, 0.0, 0.45))
        self.color = OpenMaya.MColor((0.9, 0.9, 0.5, 0.25))
        self.center = OpenMaya.MPoint(0.0, 0.0, 0.0)
        self.radius = 0.25
        self.subdivisionsAxis = 10
        self.subdivisionsHeight = 10
        self.filled = True


class MP2NodeFlareDrawOverride(OpenMayaRender.MPxDrawOverride):

    @staticmethod
    def creator(obj):
        return MP2NodeFlareDrawOverride(obj)

    def __init__(self, obj):
        OpenMayaRender.MPxDrawOverride.__init__(self, obj, None, False)

    def supportedDrawAPIs(self):
        return OpenMayaRender.MRenderer.kAllDevices

    def prepareForDraw(self, objPath, cameraPath, frameContext, oldData):
        data = oldData if isinstance(oldData, MP2NodeFlareDrawData) else MP2NodeFlareDrawData()
        return data

    def hasUIDrawables(self):
        return True

    def addUIDrawables(self, objPath, drawManager, frameContext, data):
        if not isinstance(data, MP2NodeFlareDrawData):
            return

        drawManager.beginDrawable()
        drawManager.setColor(data.color)
        drawManager.sphere(data.center, data.radius, data.subdivisionsAxis, data.subdivisionsHeight, data.filled)
        drawManager.setColor(data.text_color)
        drawManager.text(data.text_center, 'MP2_Flare', OpenMayaRender.MUIDrawManager.kCenter)
        drawManager.endDrawable()
