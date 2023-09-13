from __future__ import annotations

from max_payne_sdk.ldb.texture_type import Texture


class MaterialProperties:
    def __init__(self, has_alpha_test: int = 0, has_adult_content: int = 0) -> None:
        self.has_alpha_test: int  = has_alpha_test
        self.has_adult_content: int = has_adult_content


class Material:
    def __init__(self, idx: int, id: int, category_name: str, material_name: str) -> None:
        self.idx: int = idx
        self.id: int = id
        self.category_name: str = category_name
        self.material_name: str = material_name
        self.diffuse_texture: Texture = None
        self.alpha_texture: Texture = None
        self.properties: MaterialProperties = MaterialProperties()

    def setDiffuseTexture(self, texture: Texture):
        self.diffuse_texture = texture

    def setAlphaTexture(self, texture: Texture):
        self.alpha_texture = texture

    def setProperties(self, has_alpha_test: int, has_adult_content: int):
        self.properties.has_alpha_test = has_alpha_test
        self.properties.has_adult_content = has_adult_content


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

    def getMaterialByIndex(self, idx: int) -> Material:
        for material in self.materials:
            if material.idx == idx:
                return material
        raise Exception("Material not found with index %i" % idx)
