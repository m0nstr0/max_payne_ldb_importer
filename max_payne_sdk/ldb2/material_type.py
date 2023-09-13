from __future__ import annotations
from dataclasses import dataclass

from max_payne_sdk.ldb2.light_map_texture_type import LightMapTexture
from max_payne_sdk.ldb2.texture_type import Texture

@dataclass
class MaterialProperties:
    # Normal - 0, AlphaBlend - 4, AlphaCompare - 1, AlphaCompareEdgeBlend - 2, Additive - 3, WithDetailTexure - 5,
    # WithReflectionTexture - 6, WithGlossTexture - 9, AlphaCompareReflectionGloss - 10,
    # AlphaCompareEdgeBlendReflectionGloss - 11 AlphaCompareEdgeBlendReflection - 8 AlphaCompareReflection - 7
    alpha_compare_reference_value: int
    # For Z-fighting (for instance: graffity textures)
    sort_priority: int
    # For Z-fighting (for instance: graffity textures)
    detail_offset: int
    dual_sided: int
    # For Z-fighting (for instance: graffity textures)
    writes_zbuffer: int
    framerate: int
    visible_frame: int
    frames: [Texture]
    blend_mode: int

class Material:
    def __init__(self, id: int) -> None:
        self.id: int = id
        self.diffuse_texture: Texture = None
        self.detail_texture: Texture = None
        self.reflection_texture: Texture = None
        self.gloss_texture: Texture = None
        self.lightmap_texture: LightMapTexture = None
        self.properties: MaterialProperties = None
    def setDiffuseTexture(self, texture: Texture) -> None:
        self.diffuse_texture = texture

    def setDetailTexture(self, texture: Texture) -> None:
        self.detail_texture = texture

    def setReflectionTexture(self, texture: Texture) -> None:
        self.reflection_texture = texture

    def setGlossTexture(self, texture: Texture) -> None:
        self.gloss_texture = texture

    def setLightmapTexture(self, texture: LightMapTexture) -> None:
        self.lightmap_texture = texture

    def setProperties(self, properties: MaterialProperties):
        self.properties = properties


class MaterialContainer:
    def __init__(self) -> None:
        self.materials: list[Material] = []

    def __getitem__(self, key):
        return self.materials[key]

    def __len__(self):
        return len(self.materials)

    def add(self, material: Material) -> None:
        self.materials.append(material)

    def findMaterialByCategoryAndName(self, category_name: str, material_name: str) -> Material:
        for material in self.materials:
            if material.category_name == category_name and material.material_name == material_name:
                return material
        return None

    def getMaterialById(self, id: int) -> Material:
        for material in self.materials:
            if material.id == id:
                return material
        raise Exception("Material not found with index %i" % id)
