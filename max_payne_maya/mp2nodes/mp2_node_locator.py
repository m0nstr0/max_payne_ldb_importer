import maya.api.OpenMaya as OpenMaya
import maya.api.OpenMayaRender as OpenMayaRender
import maya.api.OpenMayaUI as OpenMayaUI
import maya.cmds as cmds

from max_payne_maya.mp2nodes.mp2_attr_util import create_attr_numeric


class MP2NodeLocator(OpenMayaUI.MPxLocatorNode):
    NODE_ID = None
    NODE_NAME = None

    HiddenAttr = OpenMaya.MObject()
    ExcludeFromGameAttr = OpenMaya.MObject()
    ExcludeFromLightingAttr = OpenMaya.MObject()
    EnableExportRegroupingAttr = OpenMaya.MObject()
    GameplayCriticalAttr = OpenMaya.MObject()

    @classmethod
    def registerNode(cls, plugin):
        plugin.registerNode(
            cls.NODE_NAME,
            cls.NODE_ID,
            cls.creator,
            cls.initializer,
            OpenMaya.MPxNode.kLocatorNode,
            'drawdb/geometry/{0}'.format(cls.__name__)
        )
        cls.registerDrawOverride()

    @classmethod
    def deregisterNode(cls, plugin):
        plugin.deregisterNode(cls.NODE_ID)
        cls.deregisterDrawOverride()

    @classmethod
    def registerDrawOverride(cls):
        OpenMayaRender.MDrawRegistry.registerDrawOverrideCreator('drawdb/geometry/{0}'.format(cls.__name__),
                                                                 '{0}DrawRegistrantID'.format(cls.__name__),
                                                                 cls.drawOverrideCreator())

    @classmethod
    def deregisterDrawOverride(cls):
        OpenMayaRender.MDrawRegistry.deregisterDrawOverrideCreator('drawdb/geometry/{0}'.format(cls.__name__),
                                                                   '{0}DrawRegistrantID'.format(cls.__name__))

    @classmethod
    def drawOverrideCreator(cls):
        return MP2NodeLocatorDrawOverride.creator

    @classmethod
    def creator(cls):
        return cls()

    @classmethod
    def initializer(cls):
        cls.initializeBaseAttributes()

    @classmethod
    def initializeBaseAttributes(cls):
        create_attr_numeric(cls, "HiddenAttr", "na_hidden", OpenMaya.MFnNumericData.kBoolean, 0)
        create_attr_numeric(cls, "ExcludeFromGameAttr", "na_excludeFromGame", OpenMaya.MFnNumericData.kBoolean, 0)
        create_attr_numeric(cls, "ExcludeFromLightingAttr", "na_excludeFromLighting", OpenMaya.MFnNumericData.kBoolean, 0)
        create_attr_numeric(cls, "EnableExportRegroupingAttr", "na_enableExportRegrouping", OpenMaya.MFnNumericData.kBoolean, 0)
        create_attr_numeric(cls, "GameplayCriticalAttr", "na_gameplayCritical", OpenMaya.MFnNumericData.kBoolean, 1)

    def __init__(self):
        OpenMayaUI.MPxLocatorNode.__init__(self)



class MP2NodeLocatorDrawData(OpenMaya.MUserData):
    COLOR = (0.0, 0.0, 1.0, 0.25)
    TEXT_COLOR = (0.0, 0.0, 1.0)
    RADIUS = 0.5
    LABEL = "MP_Node_Locator"

    def __init__(self):
        OpenMaya.MUserData.__init__(self, False)
        self.text_center = None
        self.text_color = OpenMaya.MColor(self.TEXT_COLOR)
        self.color = OpenMaya.MColor(self.COLOR)
        self.center = OpenMaya.MPoint(0.0, 0.0, 0.0)
        self.subdivisionsAxis = 10
        self.subdivisionsHeight = 10
        self.filled = True
        self.text = self.LABEL
        self.setRadius(self.RADIUS)

    def setRadius(self, r):
        self.radius = r
        if cmds.upAxis(q=True, axis=True) == 'y':
            self.text_center = OpenMaya.MPoint((0.0, self.radius + 0.2, 0.0))
        else:
            self.text_center = OpenMaya.MPoint((0.0, 0.0, self.radius + 0.2))


class MP2NodeLocatorDrawOverride(OpenMayaRender.MPxDrawOverride):

    @classmethod
    def creator(cls, obj):
        return cls(obj)

    def __init__(self, obj):
        OpenMayaRender.MPxDrawOverride.__init__(self, obj, None, False)

    def getDataClass(self):
        return MP2NodeLocatorDrawData

    def supportedDrawAPIs(self):
        return OpenMayaRender.MRenderer.kAllDevices

    def updateData(self, data, objPath, cameraPath, frameContext, oldData):
        pass

    def prepareForDraw(self, objPath, cameraPath, frameContext, oldData):
        data = oldData if isinstance(oldData, self.getDataClass()) else self.getDataClass()()
        self.updateData(data, objPath, cameraPath, frameContext, oldData)
        return data

    def hasUIDrawables(self):
        return True

    def addUIDrawables(self, objPath, drawManager, frameContext, data):
        if not isinstance(data, self.getDataClass()):
            return
        drawManager.beginDrawable()
        drawManager.setColor(data.color)
        drawManager.sphere(data.center, data.radius, data.subdivisionsAxis, data.subdivisionsHeight, data.filled)
        drawManager.setColor(data.text_color)
        drawManager.text(data.text_center, data.text, OpenMayaRender.MUIDrawManager.kCenter)
        drawManager.endDrawable()