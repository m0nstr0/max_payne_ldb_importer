import maya.api.OpenMaya as OpenMaya
import maya.api.OpenMayaRender as OpenMayaRender
import maya.api.OpenMayaUI as OpenMayaUI
import maya.cmds as cmds

from max_payne_maya.mp2nodes.mp2_attr_util import create_attr_numeric, create_attr_string, create_attr_enum
from max_payne_maya.mp2nodes.mp2_node_ids import MP2_PHYSIC_MATERIALS_NAMES, MP2_ROOM_SOUND_ENVIRONMENTS_NAMES


class MP2NodeMesh(OpenMaya.MPxNode):
    NODE_ID = OpenMaya.MObject()
    NODE_NAME = OpenMaya.MObject()

    IsFlippedAttr = OpenMaya.MObject()

    # gis
    GisCastNoShadowsAttr = OpenMaya.MObject()
    GisRayTracingAttr = OpenMaya.MObject()

    # visuals
    DoNotRenderAttr = OpenMaya.MObject()
    UseLightMapsAttr = OpenMaya.MObject()
    PointLightAffectAttr = OpenMaya.MObject()
    NoDecalsAttr = OpenMaya.MObject()

    # collision
    CollisionsAttr = OpenMaya.MObject()
    BulletCollisionsAttr = OpenMaya.MObject()
    CharacterCollisionsAttr = OpenMaya.MObject()
    GenerateBoundingBoxHullAttr = OpenMaya.MObject()
    GenerateConvexHullAttr = OpenMaya.MObject()
    ElevatorAttr = OpenMaya.MObject()
    BlockExplosionsAttr = OpenMaya.MObject()

    FsmContUpdateAttr = OpenMaya.MObject()

    PhysicalMaterialUseCustomAttr = OpenMaya.MObject()
    PhysicalMaterialCustomAttr = OpenMaya.MObject()
    PhysicalMaterialCommonAttr = OpenMaya.MObject()

    RoomSoundEnvironmentUseCustomAttr = OpenMaya.MObject()
    RoomSoundEnvironmentCustomAttr = OpenMaya.MObject()
    RoomSoundEnvironmentCommonAttr = OpenMaya.MObject()

    HiddenAttr = OpenMaya.MObject()
    ExcludeFromGameAttr = OpenMaya.MObject()
    ExcludeFromLightingAttr = OpenMaya.MObject()
    EnableExportRegroupingAttr = OpenMaya.MObject()
    GameplayCriticalAttr = OpenMaya.MObject()

    InMeshAttr = OpenMaya.MObject()
    OutMeshAttr = OpenMaya.MObject()

    @classmethod
    def creator(cls):
        return cls()

    @classmethod
    def registerNode(cls, plugin):
        plugin.registerNode(
            cls.NODE_NAME,
            cls.NODE_ID,
            cls.creator,
            cls.initializer
        )

    @classmethod
    def deregisterNode(cls, plugin):
        plugin.deregisterNode(cls.NODE_ID)

    @classmethod
    def initializer(cls):
        cls.initializeBaseAttributes()
        cls.initializeMeshAttributes()

        in_mesh_attr = OpenMaya.MFnTypedAttribute()
        cls.InMeshAttr = in_mesh_attr.create("inMesh", "in", OpenMaya.MFnData.kMesh)
        in_mesh_attr.hidden = False
        in_mesh_attr.keyable = False
        in_mesh_attr.writable = True
        in_mesh_attr.storable = True
        cls.addAttribute(cls.InMeshAttr)

        out_mesh_attr = OpenMaya.MFnTypedAttribute()
        cls.OutMeshAttr = out_mesh_attr.create("outMesh", "out", OpenMaya.MFnData.kMesh)
        out_mesh_attr.hidden = False
        out_mesh_attr.keyable = False
        out_mesh_attr.writable = False
        out_mesh_attr.storable = False
        cls.addAttribute(cls.OutMeshAttr)

        cls.attributeAffects(cls.InMeshAttr, cls.OutMeshAttr)

    @classmethod
    def initializeMeshAttributes(cls):
        create_attr_numeric(cls, "IsFlippedAttr", "na_isFlipped", OpenMaya.MFnNumericData.kBoolean, 1)
        create_attr_numeric(cls, "GisCastNoShadowsAttr", "na_castNoShadows", OpenMaya.MFnNumericData.kBoolean, 0)
        create_attr_numeric(cls, "GisRayTracingAttr", "na_rayTracing", OpenMaya.MFnNumericData.kBoolean, 0)
        create_attr_numeric(cls, "CollisionsAttr", "na_collisions", OpenMaya.MFnNumericData.kBoolean, 1)
        create_attr_numeric(cls, "BulletCollisionsAttr", "na_bulletCollisions", OpenMaya.MFnNumericData.kBoolean, 1)
        create_attr_numeric(cls, "CharacterCollisionsAttr", "na_characterCollisions", OpenMaya.MFnNumericData.kBoolean, 1)
        create_attr_numeric(cls, "GenerateBoundingBoxHullAttr", "na_generateBoundingBoxHull", OpenMaya.MFnNumericData.kBoolean, 0)
        create_attr_numeric(cls, "DoNotRenderAttr", "na_doNotRender", OpenMaya.MFnNumericData.kBoolean, 0)

        create_attr_numeric(cls, "BlockExplosionsAttr", 'na_blockExplosions', OpenMaya.MFnNumericData.kBoolean, 1)
        create_attr_numeric(cls, "ElevatorAttr", 'na_elevator', OpenMaya.MFnNumericData.kBoolean, 0)

        create_attr_numeric(cls, "PhysicalMaterialUseCustomAttr", 'na_physicalMaterialUseCustom', OpenMaya.MFnNumericData.kBoolean, 0)
        create_attr_string(cls, "PhysicalMaterialCustomAttr", 'na_physicalMaterialCustom', MP2_PHYSIC_MATERIALS_NAMES[0])
        create_attr_enum(cls, "PhysicalMaterialCommonAttr", 'na_physicalMaterialCommon', MP2_PHYSIC_MATERIALS_NAMES)

        create_attr_numeric(cls, "RoomSoundEnvironmentUseCustomAttr", 'na_roomSoundEnvironmentUseCustom', OpenMaya.MFnNumericData.kBoolean, 0)
        create_attr_string(cls, "RoomSoundEnvironmentCustomAttr", 'na_roomSoundEnvironmentCustom', MP2_ROOM_SOUND_ENVIRONMENTS_NAMES[0])
        create_attr_enum(cls, "RoomSoundEnvironmentCommonAttr", 'na_roomSoundEnvironmentCommon', MP2_ROOM_SOUND_ENVIRONMENTS_NAMES)

        create_attr_numeric(cls, "GenerateConvexHullAttr", "na_generateConvexHull", OpenMaya.MFnNumericData.kBoolean, 0)

        create_attr_numeric(cls, "UseLightMapsAttr", 'na_useLightMaps', OpenMaya.MFnNumericData.kBoolean, 1)
        create_attr_numeric(cls, "PointLightAffectAttr", 'na_pointLightsAffect', OpenMaya.MFnNumericData.kBoolean, 0)
        create_attr_numeric(cls, "NoDecalsAttr", 'na_noDecals', OpenMaya.MFnNumericData.kBoolean, 0)
        create_attr_numeric(cls, "FsmContUpdateAttr", 'na_fsmContUpdate', OpenMaya.MFnNumericData.kBoolean, 0)

    @classmethod
    def initializeBaseAttributes(cls):
        create_attr_numeric(cls, "HiddenAttr", "na_hidden", OpenMaya.MFnNumericData.kBoolean, 0)
        create_attr_numeric(cls, "ExcludeFromGameAttr", "na_excludeFromGame", OpenMaya.MFnNumericData.kBoolean, 0)
        create_attr_numeric(cls, "ExcludeFromLightingAttr", "na_excludeFromLighting", OpenMaya.MFnNumericData.kBoolean, 0)
        create_attr_numeric(cls, "EnableExportRegroupingAttr", "na_enableExportRegrouping", OpenMaya.MFnNumericData.kBoolean, 0)
        create_attr_numeric(cls, "GameplayCriticalAttr", "na_gameplayCritical", OpenMaya.MFnNumericData.kBoolean, 1)

    def __init__(self):
        OpenMaya.MPxNode.__init__(self)
