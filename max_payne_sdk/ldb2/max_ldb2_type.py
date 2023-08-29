from max_payne_sdk.ldb2.light_map_texture_type import LightMapTextureContainer
from max_payne_sdk.ldb2.material_type import MaterialContainer
from max_payne_sdk.ldb2.room_type import RoomContainer
from max_payne_sdk.ldb2.texture_type import TextureContainer
from max_payne_sdk.ldb_common.max_ldb_interface import MaxLDBInterface


class MaxLDB2 (MaxLDBInterface):
    def __init__(self) -> None:
        self.textures: TextureContainer = TextureContainer()
        self.lightmaps: LightMapTextureContainer = LightMapTextureContainer()
        self.materials: MaterialContainer = MaterialContainer()
        self.rooms: RoomContainer = RoomContainer()

    def getTextures(self) -> TextureContainer:
        return self.textures

    def getMaterials(self) -> MaterialContainer:
        return self.materials

    def getLightMaps(self) -> LightMapTextureContainer:
        return self.lightmaps

    def getRooms(self) -> RoomContainer:
        return self.rooms