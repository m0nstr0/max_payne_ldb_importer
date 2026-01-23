import maya.api.OpenMaya as OpenMaya
import maya.api.OpenMayaRender as OpenMayaRender
import maya.api.OpenMayaUI as OpenMayaUI
import maya.cmds as cmds

from max_payne_maya.mp2nodes.mp2_node_ids import MP2_LEVEL_ITEM_NODE_ID, MP2_LEVEL_ITEM_NODE_NAME, \
    MP2_LEVEL_ITEM_NAMES_COMMON, MP2_USE_ACTIVATE_ANIMATIONS


class MP2NodeLevelItem(OpenMayaUI.MPxLocatorNode):
    NODE_ID = OpenMaya.MTypeId(MP2_LEVEL_ITEM_NODE_ID)
    NODE_NAME = MP2_LEVEL_ITEM_NODE_NAME
    NODE_DRAW_CLASSIFICATION = 'drawdb/geometry/MP2NodeLevelItem'
    NODE_DRAW_REGISTRANT_ID = 'MP2NodeLevelItemDrawRegistrantID'
    NODE_SUB_CLASS = OpenMaya.MPxNode.kLocatorNode

    HiddenAttr = OpenMaya.MObject()
    ExcludeFromGameAttr = OpenMaya.MObject()
    ExcludeFromLightingAttr = OpenMaya.MObject()
    EnableExportRegroupingAttr = OpenMaya.MObject()

    ItemNameCustomAttr = OpenMaya.MObject()
    ItemNameCommonAttr = OpenMaya.MObject()
    ItemNameUseCustomAttr = OpenMaya.MObject()

    @staticmethod
    def registerNode(plugin):
        plugin.registerNode(
            MP2NodeLevelItem.NODE_NAME,
            MP2NodeLevelItem.NODE_ID,
            MP2NodeLevelItem.creator,
            MP2NodeLevelItem.initializer,
            MP2NodeLevelItem.NODE_SUB_CLASS,
            MP2NodeLevelItem.NODE_DRAW_CLASSIFICATION
        )
        MP2NodeLevelItem.registerDrawOverride()

    @staticmethod
    def deregisterNode(plugin):
        plugin.deregisterNode(MP2NodeLevelItem.NODE_ID)
        MP2NodeLevelItem.deregisterDrawOverride()

    @staticmethod
    def registerDrawOverride():
        OpenMayaRender.MDrawRegistry.registerDrawOverrideCreator(MP2NodeLevelItem.NODE_DRAW_CLASSIFICATION,
                                                                 MP2NodeLevelItem.NODE_DRAW_REGISTRANT_ID,
                                                                 MP2NodeLevelItemDrawOverride.creator)

    @staticmethod
    def deregisterDrawOverride():
        OpenMayaRender.MDrawRegistry.deregisterDrawOverrideCreator(MP2NodeLevelItem.NODE_DRAW_CLASSIFICATION,
                                                                   MP2NodeLevelItem.NODE_DRAW_REGISTRANT_ID)
    @staticmethod
    def creator():
        return MP2NodeLevelItem()

    @staticmethod
    def initializer():
        MP2NodeLevelItem.initializeBaseAttributes()

        item_name_use_custom = OpenMaya.MFnNumericAttribute()
        MP2NodeLevelItem.ItemNameUseCustomAttr = item_name_use_custom.create("na_itemNameUseCustom", "na_itemNameUseCustom", OpenMaya.MFnNumericData.kBoolean, False)
        item_name_use_custom.hidden = False
        item_name_use_custom.keyable = False
        item_name_use_custom.writable = True
        item_name_use_custom.storable = True
        MP2NodeLevelItem.addAttribute(MP2NodeLevelItem.ItemNameUseCustomAttr)

        item_name_custom_string = OpenMaya.MFnStringData().create(MP2_LEVEL_ITEM_NAMES_COMMON[0])
        item_name_custom_attr = OpenMaya.MFnTypedAttribute()
        MP2NodeLevelItem.ItemNameCustomAttr = item_name_custom_attr.create("na_itemNameCustom", "na_itemNameCustom", OpenMaya.MFnData.kString, item_name_custom_string)
        item_name_custom_attr.hidden = False
        item_name_custom_attr.keyable = False
        item_name_custom_attr.writable = True
        item_name_custom_attr.storable = True
        MP2NodeLevelItem.addAttribute(MP2NodeLevelItem.ItemNameCustomAttr)

        item_name_common_attr = OpenMaya.MFnEnumAttribute()
        MP2NodeLevelItem.ItemNameCommonAttr = item_name_common_attr.create("na_itemNameCommon", "na_itemNameCommon", 0)

        for i in range(len(MP2_LEVEL_ITEM_NAMES_COMMON)):
            item_name_common_attr.addField(MP2_LEVEL_ITEM_NAMES_COMMON[i], i)

        item_name_common_attr.hidden = False
        item_name_common_attr.keyable = False
        item_name_common_attr.writable = True
        item_name_common_attr.storable = True
        MP2NodeLevelItem.addAttribute(MP2NodeLevelItem.ItemNameCommonAttr)


    @staticmethod
    def initializeBaseAttributes():
        hidden_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeLevelItem.HiddenAttr = hidden_attr.create("na_hidden", "na_hidden", OpenMaya.MFnNumericData.kBoolean, 0)
        hidden_attr.hidden = False
        hidden_attr.keyable = False
        hidden_attr.writable = True
        hidden_attr.storable = True
        MP2NodeLevelItem.addAttribute(MP2NodeLevelItem.HiddenAttr)

        exclude_from_game_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeLevelItem.ExcludeFromGameAttr = exclude_from_game_attr.create("na_excludeFromGame", "na_excludeFromGame", OpenMaya.MFnNumericData.kBoolean, 0)
        exclude_from_game_attr.hidden = False
        exclude_from_game_attr.keyable = False
        exclude_from_game_attr.writable = True
        exclude_from_game_attr.storable = True
        MP2NodeLevelItem.addAttribute(MP2NodeLevelItem.ExcludeFromGameAttr)

        exclude_from_lighting_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeLevelItem.ExcludeFromLightingAttr = exclude_from_lighting_attr.create("na_excludeFromLighting", "na_excludeFromLighting", OpenMaya.MFnNumericData.kBoolean, 0)
        exclude_from_lighting_attr.hidden = False
        exclude_from_lighting_attr.keyable = False
        exclude_from_lighting_attr.writable = True
        exclude_from_lighting_attr.storable = True
        MP2NodeLevelItem.addAttribute(MP2NodeLevelItem.ExcludeFromLightingAttr)

        enable_export_regrouping_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeLevelItem.EnableExportRegroupingAttr = enable_export_regrouping_attr.create("na_enableExportRegrouping", "na_enableExportRegrouping", OpenMaya.MFnNumericData.kBoolean, 0)
        enable_export_regrouping_attr.hidden = False
        enable_export_regrouping_attr.keyable = False
        enable_export_regrouping_attr.writable = True
        enable_export_regrouping_attr.storable = True
        MP2NodeLevelItem.addAttribute(MP2NodeLevelItem.EnableExportRegroupingAttr)

    def __init__(self):
        OpenMayaUI.MPxLocatorNode.__init__(self)

    def compute(self, plug, dataBlock):
        pass


class MP2NodeLevelItemDrawData(OpenMaya.MUserData):
    def __init__(self):
        OpenMaya.MUserData.__init__(self, False)

        self.text_color = OpenMaya.MColor((1.0, 1.0, 0.0))
        if cmds.upAxis(q=True, axis=True) == 'y':
            self.text_center = OpenMaya.MPoint((0.0, 0.25, 0.0))
        else:
            self.text_center = OpenMaya.MPoint((0.0, 0.0, 0.25))
        self.color = OpenMaya.MColor((1.0, 1.0, 0.0, 0.25))
        self.center = OpenMaya.MPoint(0.0, 0.0, 0.0)
        self.radius = 0.05
        self.subdivisionsAxis = 10
        self.subdivisionsHeight = 10
        self.filled = True


class MP2NodeLevelItemDrawOverride(OpenMayaRender.MPxDrawOverride):

    @staticmethod
    def creator(obj):
        return MP2NodeLevelItemDrawOverride(obj)

    def __init__(self, obj):
        OpenMayaRender.MPxDrawOverride.__init__(self, obj, None, False)

    def supportedDrawAPIs(self):
        return OpenMayaRender.MRenderer.kAllDevices

    def prepareForDraw(self, objPath, cameraPath, frameContext, oldData):
        data = oldData if isinstance(oldData, MP2NodeLevelItemDrawData) else MP2NodeLevelItemDrawData()
        return data

    def hasUIDrawables(self):
        return True

    def addUIDrawables(self, objPath, drawManager, frameContext, data):
        if not isinstance(data, MP2NodeLevelItemDrawData):
            return

        drawManager.beginDrawable()
        drawManager.setColor(data.color)
        drawManager.sphere(data.center, data.radius, data.subdivisionsAxis, data.subdivisionsHeight, data.filled)
        drawManager.setColor(data.text_color)
        drawManager.text(data.text_center, 'MP2_LevelItem', OpenMayaRender.MUIDrawManager.kCenter)
        drawManager.endDrawable()
