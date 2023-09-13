from __future__ import annotations

class Texture:
    def __init__(self, group_id: int, file_path: str, file_type: int, data : bytes) -> None:
        self.file_path : str = file_path
        self.file_type : int = file_type
        self.data : bytes = data
        self.group_id : int = group_id

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


class TextureContainer:
    def __init__(self) -> None:
        self.textures : list[Texture] = []

    def __len__(self):
        return len(self.textures)

    def __getitem__(self, key):
        return self.textures[key]
    
    def add(self, texture: Texture) -> None:
        self.textures.append(texture)

    def findTextureByGroupAndID(self, group_id: int, id: int) -> Texture:
        index = -1
        for texture in self.textures:
            if texture.group_id == group_id:
                index = index + 1
                if index == id:
                    return texture
        return None
