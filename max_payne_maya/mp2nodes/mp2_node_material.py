import maya.api.OpenMaya as OpenMaya
import maya.api.OpenMayaRender as OpenMayaRender

from max_payne_maya.mp2nodes.mp2_node_ids import MP2_MATERIAL_NODE_ID, MP2_MATERIAL_NODE_NAME


class MP2NodeMaterial(OpenMaya.MPxNode):
    NODE_ID = OpenMaya.MTypeId(MP2_MATERIAL_NODE_ID)
    NODE_NAME = MP2_MATERIAL_NODE_NAME
    NODE_CLASSIFICATION = 'shader/surface'
    NODE_DRAW_REGISTRANT_ID = 'MP2NodeMaterialDrawRegistrantID'
    NODE_DRAW_CLASSIFICATION = 'drawdb/shader/surface/MP2NodeMaterial'
    NODE_SUB_CLASS = OpenMaya.MPxNode.kDependNode

    DiffuseTextureAdditionAttr = OpenMaya.MObject()
    CategoryNameAttr = OpenMaya.MObject()
    DualSidedAttr = OpenMaya.MObject()
    AdultContentAttr = OpenMaya.MObject()
    DiffuseDefaultWidthAttr = OpenMaya.MObject()
    DiffuseDefaultHeightAttr = OpenMaya.MObject()
    ActiveFrameAttr = OpenMaya.MObject()
    FramerateAttr = OpenMaya.MObject()
    # 3 - Additive, 0 - Normal, 1 - Alpha Compare, 2 - Alpha Blend
    TextureModeAttr = OpenMaya.MObject()

    # 1 - Alpha Compare
    AlphaCompareEdgeBlendAttr = OpenMaya.MObject()
    AlphaCompareReferenceValueAttr = OpenMaya.MObject()

    # 4 - With Detail Texture
    DetailTextureAttr = OpenMaya.MObject()
    DetailTextureDefaultScaleAttr = OpenMaya.MObject()

    ReflectionTextureAttr = OpenMaya.MObject()
    GlossTextureAttr = OpenMaya.MObject()

    LightLayerTextureAttr = OpenMaya.MObject()
    LightLayerDefaultWidthAttr = OpenMaya.MObject()
    LightLayerDefaultHeightAttr = OpenMaya.MObject()

    InColorAttr = OpenMaya.MObject()
    OutColorAttr = OpenMaya.MObject()

    @staticmethod
    def registerNode(plugin):
        plugin.registerNode(
            MP2NodeMaterial.NODE_NAME,
            MP2NodeMaterial.NODE_ID,
            MP2NodeMaterial.creator,
            MP2NodeMaterial.initializer,
            MP2NodeMaterial.NODE_SUB_CLASS,
            MP2NodeMaterial.NODE_CLASSIFICATION
        )
        MP2NodeMaterial.registerDrawOverride()

    @staticmethod
    def deregisterNode(plugin):
        plugin.deregisterNode(MP2NodeMaterial.NODE_ID)
        MP2NodeMaterial.deregisterDrawOverride()

    @staticmethod
    def registerDrawOverride():
        OpenMayaRender.MDrawRegistry.registerSurfaceShadingNodeOverrideCreator(
            MP2NodeMaterial.NODE_DRAW_CLASSIFICATION,
            MP2NodeMaterial.NODE_DRAW_REGISTRANT_ID,
            MP2NodeMaterialDrawOverride.creator
        )

    @staticmethod
    def deregisterDrawOverride():
        OpenMayaRender.MDrawRegistry.deregisterSurfaceShadingNodeOverrideCreator(
            MP2NodeMaterial.NODE_DRAW_CLASSIFICATION,
            MP2NodeMaterial.NODE_DRAW_REGISTRANT_ID
        )

    @staticmethod
    def creator():
        return MP2NodeMaterial()

    @staticmethod
    def initializer():
        # category
        category_name_default_string = OpenMaya.MFnStringData().create('Default')
        category_attr = OpenMaya.MFnTypedAttribute()
        MP2NodeMaterial.CategoryNameAttr = category_attr.create("na_category", "na_category", OpenMaya.MFnData.kString,
                                                                category_name_default_string)
        category_attr.hidden = False
        category_attr.keyable = False
        category_attr.writable = True
        category_attr.storable = True
        MP2NodeMaterial.addAttribute(MP2NodeMaterial.CategoryNameAttr)

        # dualsided
        dualsided_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeMaterial.DualSidedAttr = dualsided_attr.create("na_dualSided", "na_dualSided",
                                                              OpenMaya.MFnNumericData.kBoolean, 0)
        dualsided_attr.hidden = False
        dualsided_attr.keyable = False
        dualsided_attr.writable = True
        dualsided_attr.storable = True
        MP2NodeMaterial.addAttribute(MP2NodeMaterial.DualSidedAttr)

        # adultcontent
        adultcontent_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeMaterial.AdultContentAttr = adultcontent_attr.create("na_adultContent", "na_adultContent",
                                                                    OpenMaya.MFnNumericData.kBoolean, 0)
        adultcontent_attr.hidden = False
        adultcontent_attr.keyable = False
        adultcontent_attr.writable = True
        adultcontent_attr.storable = True
        MP2NodeMaterial.addAttribute(MP2NodeMaterial.AdultContentAttr)

        # diffuse_width
        diffuse_width_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeMaterial.DiffuseDefaultWidthAttr = diffuse_width_attr.create("na_diffuseTextureWidth",
                                                                            "na_diffuseTextureWidth",
                                                                            OpenMaya.MFnNumericData.kFloat, 2)
        diffuse_width_attr.hidden = False
        diffuse_width_attr.keyable = False
        diffuse_width_attr.writable = True
        diffuse_width_attr.storable = True
        MP2NodeMaterial.addAttribute(MP2NodeMaterial.DiffuseDefaultWidthAttr)

        # diffuse_height
        diffuse_height_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeMaterial.DiffuseDefaultHeightAttr = diffuse_height_attr.create("na_diffuseTextureHeight",
                                                                              "na_diffuseTextureHeight",
                                                                              OpenMaya.MFnNumericData.kFloat, 2)
        diffuse_height_attr.hidden = False
        diffuse_height_attr.keyable = False
        diffuse_height_attr.writable = True
        diffuse_height_attr.storable = True
        MP2NodeMaterial.addAttribute(MP2NodeMaterial.DiffuseDefaultHeightAttr)

        # active_frame
        active_frame_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeMaterial.ActiveFrameAttr = active_frame_attr.create("na_activeFrame", "na_activeFrame",
                                                                   OpenMaya.MFnNumericData.kInt, 0)
        active_frame_attr.hidden = False
        active_frame_attr.keyable = False
        active_frame_attr.writable = True
        active_frame_attr.storable = True
        MP2NodeMaterial.addAttribute(MP2NodeMaterial.ActiveFrameAttr)

        # framerate
        framerate_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeMaterial.FramerateAttr = framerate_attr.create("na_framerate", "na_framerate",
                                                              OpenMaya.MFnNumericData.kInt, 1)
        framerate_attr.hidden = False
        framerate_attr.keyable = False
        framerate_attr.writable = True
        framerate_attr.storable = True
        MP2NodeMaterial.addAttribute(MP2NodeMaterial.FramerateAttr)

        # detail_scale
        detail_scale_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeMaterial.DetailTextureDefaultScaleAttr = detail_scale_attr.create("na_detailTextureScale",
                                                                                 "na_detailTextureScale",
                                                                                 OpenMaya.MFnNumericData.kFloat, 1)
        detail_scale_attr.hidden = False
        detail_scale_attr.keyable = False
        detail_scale_attr.writable = True
        detail_scale_attr.storable = True
        MP2NodeMaterial.addAttribute(MP2NodeMaterial.DetailTextureDefaultScaleAttr)

        # light_layer_width
        light_layer_width_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeMaterial.LightLayerDefaultWidthAttr = light_layer_width_attr.create("na_lightLayerWidth",
                                                                                   "na_lightLayerWidth",
                                                                                   OpenMaya.MFnNumericData.kFloat, 1)
        light_layer_width_attr.hidden = False
        light_layer_width_attr.keyable = False
        light_layer_width_attr.writable = True
        light_layer_width_attr.storable = True
        MP2NodeMaterial.addAttribute(MP2NodeMaterial.LightLayerDefaultWidthAttr)

        # light_layer_height
        light_layer_height_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeMaterial.LightLayerDefaultHeightAttr = light_layer_height_attr.create("na_lightLayerHeight",
                                                                                     "na_lightLayerHeight",
                                                                                     OpenMaya.MFnNumericData.kFloat, 1)
        light_layer_height_attr.hidden = False
        light_layer_height_attr.keyable = False
        light_layer_height_attr.writable = True
        light_layer_height_attr.storable = True
        MP2NodeMaterial.addAttribute(MP2NodeMaterial.LightLayerDefaultHeightAttr)

        # alpha_compare_ref
        alpha_compare_ref_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeMaterial.AlphaCompareReferenceValueAttr = alpha_compare_ref_attr.create("na_alphaCompareReferenceValue",
                                                                                       "na_alphaCompareReferenceValue",
                                                                                       OpenMaya.MFnNumericData.kInt,
                                                                                       240)
        alpha_compare_ref_attr.hidden = False
        alpha_compare_ref_attr.keyable = False
        alpha_compare_ref_attr.writable = True
        alpha_compare_ref_attr.storable = True
        MP2NodeMaterial.addAttribute(MP2NodeMaterial.AlphaCompareReferenceValueAttr)

        # alpha_edge_blend
        alpha_edge_blend_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeMaterial.AlphaCompareEdgeBlendAttr = alpha_edge_blend_attr.create("na_alphaEdgeBlend",
                                                                                 "na_alphaEdgeBlend",
                                                                                 OpenMaya.MFnNumericData.kBoolean, 0)
        alpha_edge_blend_attr.hidden = False
        alpha_edge_blend_attr.keyable = False
        alpha_edge_blend_attr.writable = True
        alpha_edge_blend_attr.storable = True
        MP2NodeMaterial.addAttribute(MP2NodeMaterial.AlphaCompareEdgeBlendAttr)

        # detail_texture
        detail_texture_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeMaterial.DetailTextureAttr = detail_texture_attr.createColor("na_detailTexture", "na_detailTexture")
        detail_texture_attr.keyable = True
        detail_texture_attr.storable = True
        MP2NodeMaterial.addAttribute(MP2NodeMaterial.DetailTextureAttr)

        # reflection_texture
        reflection_texture_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeMaterial.ReflectionTextureAttr = reflection_texture_attr.createColor("na_reflectionTexture",
                                                                                    "na_reflectionTexture")
        reflection_texture_attr.keyable = True
        reflection_texture_attr.storable = True
        MP2NodeMaterial.addAttribute(MP2NodeMaterial.ReflectionTextureAttr)

        # gloss_texture
        gloss_texture_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeMaterial.GlossTextureAttr = gloss_texture_attr.createColor("na_glossTexture", "na_glossTexture")
        gloss_texture_attr.keyable = True
        gloss_texture_attr.storable = True
        MP2NodeMaterial.addAttribute(MP2NodeMaterial.GlossTextureAttr)

        # light_texture
        light_texture_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeMaterial.LightLayerTextureAttr = light_texture_attr.createColor("na_lightLayerTexture",
                                                                               "na_lightLayerTexture")
        light_texture_attr.keyable = True
        light_texture_attr.storable = True
        MP2NodeMaterial.addAttribute(MP2NodeMaterial.LightLayerTextureAttr)

        # texture_mode
        texture_mode_attr = OpenMaya.MFnEnumAttribute()
        MP2NodeMaterial.TextureModeAttr = texture_mode_attr.create("na_textureMode", "na_textureMode", 0)
        texture_mode_attr.addField("Normal", 0)
        texture_mode_attr.addField("Alpha Compare", 1)
        texture_mode_attr.addField("Alpha Blend", 2)
        texture_mode_attr.addField("Additive", 3)
        texture_mode_attr.hidden = False
        texture_mode_attr.keyable = False
        texture_mode_attr.writable = True
        texture_mode_attr.storable = True
        MP2NodeMaterial.addAttribute(MP2NodeMaterial.TextureModeAttr)

        # Input color
        diffuse_texture_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeMaterial.InColorAttr = diffuse_texture_attr.createColor("color", "col")
        diffuse_texture_attr.default = (0.5, 0.5, 0.5)
        diffuse_texture_attr.keyable = True
        diffuse_texture_attr.storable = True
        MP2NodeMaterial.addAttribute(MP2NodeMaterial.InColorAttr)

        # additional diffuse texture
        diffuse_texture_add_attr = OpenMaya.MFnNumericAttribute()
        MP2NodeMaterial.DiffuseTextureAdditionAttr = diffuse_texture_add_attr.createColor("na_diffuseTextureAdditional",
                                                                                          "na_diffuseTextureAdditional")
        diffuse_texture_add_attr.keyable = True
        diffuse_texture_add_attr.storable = True
        diffuse_texture_add_attr.array = True
        diffuse_texture_add_attr.usesArrayDataBuilder = True
        MP2NodeMaterial.addAttribute(MP2NodeMaterial.DiffuseTextureAdditionAttr)

        # Output color
        out_color = OpenMaya.MFnNumericAttribute()
        MP2NodeMaterial.OutColorAttr = out_color.createColor("outColor", "oc")
        out_color.writable = False
        out_color.storable = False
        out_color.readable = True
        out_color.usedAsColor = True
        MP2NodeMaterial.addAttribute(MP2NodeMaterial.OutColorAttr)

        # Dependency
        MP2NodeMaterial.attributeAffects(
            MP2NodeMaterial.InColorAttr,
            MP2NodeMaterial.OutColorAttr
        )

    def compute(self, plug, data_block):
        if plug != MP2NodeMaterial.OutColorAttr:
            return

        color = data_block.inputValue(
            MP2NodeMaterial.InColorAttr
        ).asFloat3()

        out_handle = data_block.outputValue(
            MP2NodeMaterial.OutColorAttr
        )

        out_handle.set3Float(color[0], color[1], color[2])
        out_handle.setClean()

    # def compute(self, plug, dataBlock):
    #
    #     if plug != MyShader.outColor:
    #         return
    #
    #     # Получаем array handle
    #     arrayHandle = dataBlock.inputArrayValue(MyShader.layerColor)
    #
    #     r = g = b = 0.0
    #
    #     for i in range(arrayHandle.elementCount()):
    #         arrayHandle.jumpToElement(i)
    #
    #         colorHandle = arrayHandle.inputValue()
    #         col = colorHandle.asFloat3()
    #
    #         r += col[0]
    #         g += col[1]
    #         b += col[2]
    #
    #     outHandle = dataBlock.outputValue(MyShader.outColor)
    #     outHandle.set3Float(r, g, b)
    #     outHandle.setClean()


class MP2NodeMaterialDrawOverride(OpenMayaRender.MPxSurfaceShadingNodeOverride):
    @staticmethod
    def creator(obj):
        return MP2NodeMaterialDrawOverride(obj)

    def __init__(self, obj):
        super().__init__(obj)
        self.texture_mode = 0

    def supportedDrawAPIs(self):
        return (
                OpenMayaRender.MRenderer.kOpenGL |
                OpenMayaRender.MRenderer.kOpenGLCoreProfile |
                OpenMayaRender.MRenderer.kDirectX11
        )

    def fragmentName(self):
        # Используем встроенный Maya GPU shader
        return "mayaLambertSurface"

    def updateDG(self):
        fn = OpenMaya.MFnDependencyNode(self.node())

        try:
            plug = fn.findPlug("na_textureMode", False)
            self.texture_mode = plug.asInt()
        except RuntimeError:
            self.texture_mode = 0

    def getCustomMappings(self):
        # Маппинг атрибутов ноды -> fragment parameters
        return {
            "color": "diffuseColor"
        }

    def updateShader(self, shader, mappings):
        #shader (MShaderInstance) - The shader instance.
        #mappings (MAttributeParameterMappingList)
        super().updateShader(shader, mappings)
