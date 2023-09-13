from max_payne_sdk.ldb2.character_type import CharacterContainer, CharacterEnemyGroupContainer
from max_payne_sdk.ldb2.dynamic_light_type import DynamicLightContainer
from max_payne_sdk.ldb2.dynamic_mesh_type import DynamicMeshContainer
from max_payne_sdk.ldb2.flare_type import FlareContainer
from max_payne_sdk.ldb2.fsm_type import FSMContainer
from max_payne_sdk.ldb2.jump_point_type import JumpPointContainer
from max_payne_sdk.ldb2.level_item_type import LevelItemContainer
from max_payne_sdk.ldb2.light_map_texture_type import LightMapTextureContainer
from max_payne_sdk.ldb2.material_type import MaterialContainer
from max_payne_sdk.ldb2.portal_type import PortalContainer
from max_payne_sdk.ldb2.room_type import RoomContainer
from max_payne_sdk.ldb2.texture_type import TextureContainer
from max_payne_sdk.ldb2.way_point_type import WayPointContainer
from max_payne_sdk.ldb_common.max_ldb_interface import MaxLDBInterface


class MaxLDB2(MaxLDBInterface):
    def __init__(self) -> None:
        self.textures: TextureContainer = TextureContainer()
        self.light_maps: LightMapTextureContainer = LightMapTextureContainer()
        self.materials: MaterialContainer = MaterialContainer()
        self.rooms: RoomContainer = RoomContainer()
        self.dynamic_lights: DynamicLightContainer = DynamicLightContainer()
        self.flares: FlareContainer = FlareContainer()
        self.level_items: LevelItemContainer = LevelItemContainer()
        self.portals: PortalContainer = PortalContainer()
        self.jump_points: JumpPointContainer = JumpPointContainer()
        self.way_points: WayPointContainer = WayPointContainer()
        self.characters: CharacterContainer = CharacterContainer()
        self.character_enemy_groups: CharacterEnemyGroupContainer = CharacterEnemyGroupContainer()
        self.dynamic_meshes: DynamicMeshContainer = DynamicMeshContainer()
        self.fsms: FSMContainer = FSMContainer()

    def getTextures(self) -> TextureContainer:
        return self.textures

    def getMaterials(self) -> MaterialContainer:
        return self.materials

    def getLightMaps(self) -> LightMapTextureContainer:
        return self.light_maps

    def getRooms(self) -> RoomContainer:
        return self.rooms

    def getDynamicLights(self) -> DynamicLightContainer:
        return self.dynamic_lights

    def getFlares(self) -> FlareContainer:
        return self.flares

    def getLevelItems(self) -> LevelItemContainer:
        return self.level_items

    def getJumpPoints(self) -> JumpPointContainer:
        return self.jump_points

    def getWayPoints(self) -> WayPointContainer:
        return self.way_points

    def getPortals(self) -> PortalContainer:
        return self.portals

    def getCharacters(self) -> CharacterContainer:
        return self.characters

    def getCharacterEnemyGroups(self) -> CharacterEnemyGroupContainer:
        return self.character_enemy_groups

    def getDynamicMeshes(self) -> DynamicMeshContainer:
        return self.dynamic_meshes

    def getFSMS(self) -> FSMContainer:
        return self.fsms