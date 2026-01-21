# editorTemplate - label
# "Width" - addControl
# "";
# editorTemplate - label
# "Height" - addControl
# "";
# editorTemplate - label
# "Depth" - addControl
# "";
# editorTemplate - label
# "Resolution" - addControl
# "";

import maya.api.OpenMaya as OpenMaya
import maya.api.OpenMayaRender as OpenMayaRender
import maya.api.OpenMayaUI as OpenMayaUI
import maya.cmds as cmds

from max_payne_maya.mp2nodes.mp2_node_ids import MP2_VOLUME_LIGHTING_BOX_NODE_ID, MP2_VOLUME_LIGHTING_BOX_NODE_NAME


class MP2NodeVolumeLightingBox(OpenMayaUI.MPxLocatorNode):
    NODE_ID = OpenMaya.MTypeId(MP2_VOLUME_LIGHTING_BOX_NODE_ID)
    NODE_NAME = MP2_VOLUME_LIGHTING_BOX_NODE_NAME
    NODE_DRAW_CLASSIFICATION = 'drawdb/geometry/MP2NodeVolumeLightingBox'
    NODE_DRAW_REGISTRANT_ID = 'MP2NodeVolumeLightingBoxDrawRegistrantID'

    HiddenAttr = OpenMaya.MObject()
    ExcludeFromGameAttr = OpenMaya.MObject()
    ExcludeFromLightingAttr = OpenMaya.MObject()
    EnableExportRegroupingAttr = OpenMaya.MObject()

    WidthAttr = OpenMaya.MObject()
    HeightAttr = OpenMaya.MObject()
    DepthAttr = OpenMaya.MObject()
    ResolutionAttr = OpenMaya.MObject()

    @staticmethod
    def creator():
        return MP2NodeVolumeLightingBox()

    @staticmethod
    def initializer():
        MP2NodeVolumeLightingBox.initializeBaseAttributes()

        width_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeVolumeLightingBox.WidthAttr = width_attr.create("na_width", "na_width", OpenMaya.MFnNumericData.kFloat, 10.0)
        width_attr.hidden = False
        width_attr.keyable = False
        width_attr.writable = True
        width_attr.storable = True
        MP2NodeVolumeLightingBox.addAttribute(MP2NodeVolumeLightingBox.WidthAttr)

        height_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeVolumeLightingBox.HeightAttr = height_attr.create("na_height", "na_height", OpenMaya.MFnNumericData.kFloat, 10.0)
        height_attr.hidden = False
        height_attr.keyable = False
        height_attr.writable = True
        height_attr.storable = True
        MP2NodeVolumeLightingBox.addAttribute(MP2NodeVolumeLightingBox.HeightAttr)

        depth_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeVolumeLightingBox.DepthAttr = depth_attr.create("na_depth", "na_depth", OpenMaya.MFnNumericData.kFloat, 10.0)
        depth_attr.hidden = False
        depth_attr.keyable = False
        depth_attr.writable = True
        depth_attr.storable = True
        MP2NodeVolumeLightingBox.addAttribute(MP2NodeVolumeLightingBox.DepthAttr)

        resolution_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeVolumeLightingBox.ResolutionAttr = resolution_attr.create("na_resolution", "na_resolution", OpenMaya.MFnNumericData.kFloat, 1.0)
        resolution_attr.hidden = False
        resolution_attr.keyable = False
        resolution_attr.writable = True
        resolution_attr.storable = True
        MP2NodeVolumeLightingBox.addAttribute(MP2NodeVolumeLightingBox.ResolutionAttr)

    @staticmethod
    def initializeBaseAttributes():
        hidden_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeVolumeLightingBox.HiddenAttr = hidden_attr.create("na_hidden", "na_hidden", OpenMaya.MFnNumericData.kBoolean, 0)
        hidden_attr.hidden = False
        hidden_attr.keyable = False
        hidden_attr.writable = True
        hidden_attr.storable = True
        MP2NodeVolumeLightingBox.addAttribute(MP2NodeVolumeLightingBox.HiddenAttr)

        exclude_from_game_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeVolumeLightingBox.ExcludeFromGameAttr = exclude_from_game_attr.create("na_excludeFromGame", "na_excludeFromGame",
                                                                             OpenMaya.MFnNumericData.kBoolean, 0)
        exclude_from_game_attr.hidden = False
        exclude_from_game_attr.keyable = False
        exclude_from_game_attr.writable = True
        exclude_from_game_attr.storable = True
        MP2NodeVolumeLightingBox.addAttribute(MP2NodeVolumeLightingBox.ExcludeFromGameAttr)

        exclude_from_lighting_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeVolumeLightingBox.ExcludeFromLightingAttr = exclude_from_lighting_attr.create("na_excludeFromLighting",
                                                                                     "na_excludeFromLighting",
                                                                                     OpenMaya.MFnNumericData.kBoolean,
                                                                                     0)
        exclude_from_lighting_attr.hidden = False
        exclude_from_lighting_attr.keyable = False
        exclude_from_lighting_attr.writable = True
        exclude_from_lighting_attr.storable = True
        MP2NodeVolumeLightingBox.addAttribute(MP2NodeVolumeLightingBox.ExcludeFromLightingAttr)

        enable_export_regrouping_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeVolumeLightingBox.EnableExportRegroupingAttr = enable_export_regrouping_attr.create("na_enableExportRegrouping",
                                                                                           "na_enableExportRegrouping",
                                                                                           OpenMaya.MFnNumericData.kBoolean,
                                                                                           0)
        enable_export_regrouping_attr.hidden = False
        enable_export_regrouping_attr.keyable = False
        enable_export_regrouping_attr.writable = True
        enable_export_regrouping_attr.storable = True
        MP2NodeVolumeLightingBox.addAttribute(MP2NodeVolumeLightingBox.EnableExportRegroupingAttr)

    def __init__(self):
        OpenMayaUI.MPxLocatorNode.__init__(self)

    def compute(self, plug, dataBlock):
        pass


class MP2NodeVolumeLightingBoxDrawData(OpenMaya.MUserData):
    def __init__(self):
        OpenMaya.MUserData.__init__(self, False)

        self.text_color = OpenMaya.MColor((0.4, 0.4, 0.3))
        if cmds.upAxis(q=True, axis=True) == 'y':
            self.text_center = OpenMaya.MPoint((0.0, 0.7, 0.0))
            self.up = OpenMaya.MVector(0.0, 1.0, 0.0)
            self.right = OpenMaya.MVector(1.0, 0.0, 0.0)
        else:
            self.text_center = OpenMaya.MPoint((0.0, 0.0, 0.7))
            self.up = OpenMaya.MVector(0.0, 0.0, 1.0)
            self.right = OpenMaya.MVector(1.0, 0.0, 0.0)
        self.color = OpenMaya.MColor((0.4, 0.4, 0.3, 0.25))
        self.center = OpenMaya.MPoint(0.0, 0.0, 0.0)
        self.height = 10.0
        self.width = 10.0
        self.depth = 10.0
        self.radius = 0.5
        self.subdivisionsAxis = 10
        self.subdivisionsHeight = 10
        self.filled = True


class MP2NodeVolumeLightingBoxDrawOverride(OpenMayaRender.MPxDrawOverride):

    @staticmethod
    def creator(obj):
        return MP2NodeVolumeLightingBoxDrawOverride(obj)

    def __init__(self, obj):
        OpenMayaRender.MPxDrawOverride.__init__(self, obj, None, False)

    def supportedDrawAPIs(self):
        return OpenMayaRender.MRenderer.kAllDevices

    def prepareForDraw(self, objPath, cameraPath, frameContext, oldData):
        data = oldData if isinstance(oldData, MP2NodeVolumeLightingBoxDrawData) else MP2NodeVolumeLightingBoxDrawData()

        plug = OpenMaya.MPlug(objPath.node(), MP2NodeVolumeLightingBox.HeightAttr)
        if not plug.isNull:
            data.height = plug.asFloat()

        plug = OpenMaya.MPlug(objPath.node(), MP2NodeVolumeLightingBox.WidthAttr)
        if not plug.isNull:
            data.width = plug.asFloat()

        plug = OpenMaya.MPlug(objPath.node(), MP2NodeVolumeLightingBox.DepthAttr)
        if not plug.isNull:
            data.depth = plug.asFloat()

        return data

    def hasUIDrawables(self):
        return True

    def addUIDrawables(self, objPath, drawManager, frameContext, data):
        if not isinstance(data, MP2NodeVolumeLightingBoxDrawData):
            return
        drawManager.beginDrawable()
        drawManager.setColor(data.color)
        drawManager.box(data.center, data.up, data.right, data.width, data.height, data.depth, True)
        drawManager.sphere(data.center, data.radius, data.subdivisionsAxis, data.subdivisionsHeight, data.filled)
        drawManager.setColor(data.text_color)
        drawManager.text(data.text_center, 'MP2_VolumeLightingBox', OpenMayaRender.MUIDrawManager.kCenter)
        drawManager.endDrawable()
