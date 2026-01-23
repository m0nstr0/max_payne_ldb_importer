import maya.api.OpenMaya as OpenMaya
import maya.api.OpenMayaRender as OpenMayaRender
import maya.api.OpenMayaUI as OpenMayaUI
import maya.cmds as cmds

from max_payne_maya.mp2nodes.mp2_node_ids import MP2_AIN_NODE_NAME, MP2_AIN_NODE_ID


class MP2NodeAin(OpenMayaUI.MPxLocatorNode):
    NODE_ID = OpenMaya.MTypeId(MP2_AIN_NODE_ID)
    NODE_NAME = MP2_AIN_NODE_NAME
    NODE_DRAW_CLASSIFICATION = 'drawdb/geometry/MP2NodeAin'
    NODE_DRAW_REGISTRANT_ID = 'MP2NodeAinDrawRegistrantID'
    NODE_SUB_CLASS = OpenMaya.MPxNode.kLocatorNode

    HiddenAttr = OpenMaya.MObject()
    ExcludeFromGameAttr = OpenMaya.MObject()
    ExcludeFromLightingAttr = OpenMaya.MObject()
    EnableExportRegroupingAttr = OpenMaya.MObject()

    @staticmethod
    def registerNode(plugin):
        plugin.registerNode(
            MP2NodeAin.NODE_NAME,
            MP2NodeAin.NODE_ID,
            MP2NodeAin.creator,
            MP2NodeAin.initializer,
            MP2NodeAin.NODE_SUB_CLASS,
            MP2NodeAin.NODE_DRAW_CLASSIFICATION
        )
        MP2NodeAin.registerDrawOverride()

    @staticmethod
    def deregisterNode(plugin):
        plugin.deregisterNode(MP2NodeAin.NODE_ID)
        MP2NodeAin.deregisterDrawOverride()

    @staticmethod
    def registerDrawOverride():
        OpenMayaRender.MDrawRegistry.registerDrawOverrideCreator(MP2NodeAin.NODE_DRAW_CLASSIFICATION,
                                                                 MP2NodeAin.NODE_DRAW_REGISTRANT_ID,
                                                                 MP2NodeAinDrawOverride.creator)

    @staticmethod
    def deregisterDrawOverride():
        OpenMayaRender.MDrawRegistry.deregisterDrawOverrideCreator(MP2NodeAin.NODE_DRAW_CLASSIFICATION,
                                                                   MP2NodeAin.NODE_DRAW_REGISTRANT_ID)

    @staticmethod
    def creator():
        return MP2NodeAin()

    @staticmethod
    def initializer():
        MP2NodeAin.initializeBaseAttributes()

    @staticmethod
    def initializeBaseAttributes():
        hidden_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeAin.HiddenAttr = hidden_attr.create("na_hidden", "na_hidden", OpenMaya.MFnNumericData.kBoolean, 0)
        hidden_attr.hidden = False
        hidden_attr.keyable = False
        hidden_attr.writable = True
        hidden_attr.storable = True
        MP2NodeAin.addAttribute(MP2NodeAin.HiddenAttr)

        exclude_from_game_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeAin.ExcludeFromGameAttr = exclude_from_game_attr.create("na_excludeFromGame", "na_excludeFromGame",
                                                                             OpenMaya.MFnNumericData.kBoolean, 0)
        exclude_from_game_attr.hidden = False
        exclude_from_game_attr.keyable = False
        exclude_from_game_attr.writable = True
        exclude_from_game_attr.storable = True
        MP2NodeAin.addAttribute(MP2NodeAin.ExcludeFromGameAttr)

        exclude_from_lighting_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeAin.ExcludeFromLightingAttr = exclude_from_lighting_attr.create("na_excludeFromLighting",
                                                                                     "na_excludeFromLighting",
                                                                                     OpenMaya.MFnNumericData.kBoolean,
                                                                                     0)
        exclude_from_lighting_attr.hidden = False
        exclude_from_lighting_attr.keyable = False
        exclude_from_lighting_attr.writable = True
        exclude_from_lighting_attr.storable = True
        MP2NodeAin.addAttribute(MP2NodeAin.ExcludeFromLightingAttr)

        enable_export_regrouping_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeAin.EnableExportRegroupingAttr = enable_export_regrouping_attr.create("na_enableExportRegrouping",
                                                                                           "na_enableExportRegrouping",
                                                                                           OpenMaya.MFnNumericData.kBoolean,
                                                                                           0)
        enable_export_regrouping_attr.hidden = False
        enable_export_regrouping_attr.keyable = False
        enable_export_regrouping_attr.writable = True
        enable_export_regrouping_attr.storable = True
        MP2NodeAin.addAttribute(MP2NodeAin.EnableExportRegroupingAttr)

    def __init__(self):
        OpenMayaUI.MPxLocatorNode.__init__(self)

    def compute(self, plug, dataBlock):
        pass


class MP2NodeAinDrawData(OpenMaya.MUserData):
    def __init__(self):
        OpenMaya.MUserData.__init__(self, False)

        self.text_color = OpenMaya.MColor((0.0, 0.0, 1.0))
        if cmds.upAxis(q=True, axis=True) == 'y':
            self.text_center = OpenMaya.MPoint((0.0, 0.7, 0.0))
        else:
            self.text_center = OpenMaya.MPoint((0.0, 0.0, 0.7))
        self.color = OpenMaya.MColor((0.0, 0.0, 1.0, 0.25))
        self.center = OpenMaya.MPoint(0.0, 0.0, 0.0)
        self.radius = 0.5
        self.subdivisionsAxis = 10
        self.subdivisionsHeight = 10
        self.filled = True


class MP2NodeAinDrawOverride(OpenMayaRender.MPxDrawOverride):

    @staticmethod
    def creator(obj):
        return MP2NodeAinDrawOverride(obj)

    def __init__(self, obj):
        OpenMayaRender.MPxDrawOverride.__init__(self, obj, None, False)

    def supportedDrawAPIs(self):
        return OpenMayaRender.MRenderer.kAllDevices

    def prepareForDraw(self, objPath, cameraPath, frameContext, oldData):
        data = oldData if isinstance(oldData, MP2NodeAinDrawData) else MP2NodeAinDrawData()
        return data

    def hasUIDrawables(self):
        return True

    def addUIDrawables(self, objPath, drawManager, frameContext, data):
        if not isinstance(data, MP2NodeAinDrawData):
            return
        drawManager.beginDrawable()
        drawManager.setColor(data.color)
        drawManager.sphere(data.center, data.radius, data.subdivisionsAxis, data.subdivisionsHeight, data.filled)
        drawManager.setColor(data.text_color)
        drawManager.text(data.text_center, 'MP2_Ain', OpenMayaRender.MUIDrawManager.kCenter)
        drawManager.endDrawable()
