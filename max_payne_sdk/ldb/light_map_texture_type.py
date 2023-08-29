from __future__ import annotations


class LightMapTexture:
    def __init__(self, id: int, file_type: int, data : bytes) -> None:
        self.id : int = id
        self.file_type : int = file_type
        self.data : bytes = data

    def getFileTypeName(self):
        if self.file_type == 0:
            return "tga"
        if self.file_type == 2:
            return "scx"
        if self.file_type == 3:
            return "pcx"
        if self.file_type == 4:
            return "jpg"
        if self.file_type == 5:
            return "dds"
        raise Exception("Unknown texture file type %i" % self.file_type)


class LightMapTextureContainer:
    def __init__(self) -> None:
        self.textures : list[LightMapTexture] = []

    def add(self, texture: LightMapTexture) -> None:
        self.textures.append(texture)

    def getTextureById(self, id: int) -> LightMapTexture:
        for texture in self.textures:
            if texture.id == id:
                return texture
        if id == -1:
            return None
        raise Exception("LightmapTexture not found with id %i" % id)
