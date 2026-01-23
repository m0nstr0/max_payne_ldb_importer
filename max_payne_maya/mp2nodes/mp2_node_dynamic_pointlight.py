import maya.api.OpenMaya as OpenMaya
import maya.api.OpenMayaRender as OpenMayaRender
import maya.api.OpenMayaUI as OpenMayaUI
import maya.cmds as cmds

from max_payne_maya.mp2nodes.mp2_node_ids import MP2_AIN_NODE_NAME, MP2_AIN_NODE_ID, MP2_DYNAMIC_POINT_LIGHT_NODE_ID, \
    MP2_DYNAMIC_POINT_LIGHT_NODE_NAME


class MP2NodeDynamicPointLight(OpenMayaUI.MPxLocatorNode):
    NODE_ID = OpenMaya.MTypeId(MP2_DYNAMIC_POINT_LIGHT_NODE_ID)
    NODE_NAME = MP2_DYNAMIC_POINT_LIGHT_NODE_NAME
    NODE_DRAW_CLASSIFICATION = 'drawdb/geometry/MP2NodeDynamicPointLight'
    NODE_DRAW_REGISTRANT_ID = 'MP2NodeDynamicPointLightDrawRegistrantID'
    NODE_SUB_CLASS = OpenMaya.MPxNode.kLocatorNode

    HiddenAttr = OpenMaya.MObject()
    ExcludeFromGameAttr = OpenMaya.MObject()
    ExcludeFromLightingAttr = OpenMaya.MObject()
    EnableExportRegroupingAttr = OpenMaya.MObject()

    IntensityAttr = OpenMaya.MObject()
    FalloffAttr = OpenMaya.MObject()
    ColorAttr = OpenMaya.MObject()

    @staticmethod
    def registerNode(plugin):
        plugin.registerNode(
            MP2NodeDynamicPointLight.NODE_NAME,
            MP2NodeDynamicPointLight.NODE_ID,
            MP2NodeDynamicPointLight.creator,
            MP2NodeDynamicPointLight.initializer,
            MP2NodeDynamicPointLight.NODE_SUB_CLASS,
            MP2NodeDynamicPointLight.NODE_DRAW_CLASSIFICATION
        )
        MP2NodeDynamicPointLight.registerDrawOverride()

    @staticmethod
    def deregisterNode(plugin):
        plugin.deregisterNode(MP2NodeDynamicPointLight.NODE_ID)
        MP2NodeDynamicPointLight.deregisterDrawOverride()

    @staticmethod
    def registerDrawOverride():
        OpenMayaRender.MDrawRegistry.registerDrawOverrideCreator(MP2NodeDynamicPointLight.NODE_DRAW_CLASSIFICATION,
                                                                 MP2NodeDynamicPointLight.NODE_DRAW_REGISTRANT_ID,
                                                                 MP2NodeDynamicPointLightDrawOverride.creator)

    @staticmethod
    def deregisterDrawOverride():
        OpenMayaRender.MDrawRegistry.deregisterDrawOverrideCreator(MP2NodeDynamicPointLight.NODE_DRAW_CLASSIFICATION,
                                                                   MP2NodeDynamicPointLight.NODE_DRAW_REGISTRANT_ID)

    @staticmethod
    def creator():
        return MP2NodeDynamicPointLight()

    @staticmethod
    def initializer():
        MP2NodeDynamicPointLight.initializeBaseAttributes()

        intensity_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeDynamicPointLight.IntensityAttr = intensity_attr.create("na_intensity", "na_intensity", OpenMaya.MFnNumericData.kFloat, 1.0)
        intensity_attr.hidden = False
        intensity_attr.keyable = False
        intensity_attr.writable = True
        intensity_attr.storable = True
        MP2NodeDynamicPointLight.addAttribute(MP2NodeDynamicPointLight.IntensityAttr)

        falloff_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeDynamicPointLight.FalloffAttr = falloff_attr.create("na_falloff", "na_falloff", OpenMaya.MFnNumericData.kFloat, 10.0)
        falloff_attr.hidden = False
        falloff_attr.keyable = False
        falloff_attr.writable = True
        falloff_attr.storable = True
        MP2NodeDynamicPointLight.addAttribute(MP2NodeDynamicPointLight.FalloffAttr)

        color_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeDynamicPointLight.ColorAttr = color_attr.create("na_color", "na_color", OpenMaya.MFnNumericData.k3Float)
        color_attr.default = (1.0, 1.0, 1.0)
        color_attr.hidden = False
        color_attr.keyable = False
        color_attr.writable = True
        color_attr.storable = True
        color_attr.usedAsColor = True
        MP2NodeDynamicPointLight.addAttribute(MP2NodeDynamicPointLight.ColorAttr)

    @staticmethod
    def initializeBaseAttributes():
        hidden_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeDynamicPointLight.HiddenAttr = hidden_attr.create("na_hidden", "na_hidden", OpenMaya.MFnNumericData.kBoolean, 0)
        hidden_attr.hidden = False
        hidden_attr.keyable = False
        hidden_attr.writable = True
        hidden_attr.storable = True
        MP2NodeDynamicPointLight.addAttribute(MP2NodeDynamicPointLight.HiddenAttr)

        exclude_from_game_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeDynamicPointLight.ExcludeFromGameAttr = exclude_from_game_attr.create("na_excludeFromGame", "na_excludeFromGame",
                                                                                     OpenMaya.MFnNumericData.kBoolean, 0)
        exclude_from_game_attr.hidden = False
        exclude_from_game_attr.keyable = False
        exclude_from_game_attr.writable = True
        exclude_from_game_attr.storable = True
        MP2NodeDynamicPointLight.addAttribute(MP2NodeDynamicPointLight.ExcludeFromGameAttr)

        exclude_from_lighting_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeDynamicPointLight.ExcludeFromLightingAttr = exclude_from_lighting_attr.create("na_excludeFromLighting",
                                                                                     "na_excludeFromLighting",
                                                                                             OpenMaya.MFnNumericData.kBoolean,
                                                                                             0)
        exclude_from_lighting_attr.hidden = False
        exclude_from_lighting_attr.keyable = False
        exclude_from_lighting_attr.writable = True
        exclude_from_lighting_attr.storable = True
        MP2NodeDynamicPointLight.addAttribute(MP2NodeDynamicPointLight.ExcludeFromLightingAttr)

        enable_export_regrouping_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeDynamicPointLight.EnableExportRegroupingAttr = enable_export_regrouping_attr.create("na_enableExportRegrouping",
                                                                                           "na_enableExportRegrouping",
                                                                                                   OpenMaya.MFnNumericData.kBoolean,
                                                                                                   0)
        enable_export_regrouping_attr.hidden = False
        enable_export_regrouping_attr.keyable = False
        enable_export_regrouping_attr.writable = True
        enable_export_regrouping_attr.storable = True
        MP2NodeDynamicPointLight.addAttribute(MP2NodeDynamicPointLight.EnableExportRegroupingAttr)

    def __init__(self):
        OpenMayaUI.MPxLocatorNode.__init__(self)

    def compute(self, plug, dataBlock):
        pass


class MP2NodeDynamicPointLightDrawData(OpenMaya.MUserData):
    def __init__(self):
        OpenMaya.MUserData.__init__(self, False)

        self.text_color = OpenMaya.MColor((1.0, 1.0, 1.0))
        if cmds.upAxis(q=True, axis=True) == 'y':
            self.text_center = OpenMaya.MPoint((0.0, 0.7, 0.0))
        else:
            self.text_center = OpenMaya.MPoint((0.0, 0.0, 0.7))
        self.color = OpenMaya.MColor((1.0, 1.0, 1.0, 0.25))
        self.center = OpenMaya.MPoint(0.0, 0.0, 0.0)
        self.radius = 0.5
        self.subdivisionsAxis = 10
        self.subdivisionsHeight = 10
        self.filled = True


class MP2NodeDynamicPointLightDrawOverride(OpenMayaRender.MPxDrawOverride):

    @staticmethod
    def creator(obj):
        return MP2NodeDynamicPointLightDrawOverride(obj)

    def __init__(self, obj):
        OpenMayaRender.MPxDrawOverride.__init__(self, obj, None, False)

    def supportedDrawAPIs(self):
        return OpenMayaRender.MRenderer.kAllDevices

    def prepareForDraw(self, objPath, cameraPath, frameContext, oldData):
        data = oldData if isinstance(oldData, MP2NodeDynamicPointLightDrawData) else MP2NodeDynamicPointLightDrawData()
        return data

    def hasUIDrawables(self):
        return True

    def addUIDrawables(self, objPath, drawManager, frameContext, data):
        if not isinstance(data, MP2NodeDynamicPointLightDrawData):
            return
        drawManager.beginDrawable()
        drawManager.setColor(data.color)
        drawManager.sphere(data.center, data.radius, data.subdivisionsAxis, data.subdivisionsHeight, data.filled)
        drawManager.setColor(data.text_color)
        drawManager.text(data.text_center, 'MP2_DynamicPointlight', OpenMayaRender.MUIDrawManager.kCenter)
        drawManager.endDrawable()
