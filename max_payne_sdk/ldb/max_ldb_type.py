from __future__ import annotations

from max_payne_sdk.ldb.bsp_type import BSPContainer
from max_payne_sdk.ldb.character_type import CharacterContainer
from max_payne_sdk.ldb.dynamic_light_type import DynamicLightContainer
from max_payne_sdk.ldb.dynamic_mesh_type import DynamicMeshContainer
from max_payne_sdk.ldb.exit_type import ExitContainer
from max_payne_sdk.ldb.fsm_type import FSMContainer
from max_payne_sdk.ldb.item_type import ItemContainer
from max_payne_sdk.ldb.light_map_texture_type import LightMapTextureContainer
from max_payne_sdk.ldb.material_type import MaterialContainer
from max_payne_sdk.ldb.point_light_type import PointLightContainer
from max_payne_sdk.ldb.room_type import RoomContainer
from max_payne_sdk.ldb.static_mesh_type import StaticMeshContainer
from max_payne_sdk.ldb.texture_type import TextureContainer
from max_payne_sdk.ldb.trigger_type import TriggerContainer
from max_payne_sdk.ldb.waypoint_type import WaypointContainer
from max_payne_sdk.ldb_common.max_ldb_interface import MaxLDBInterface


class MaxLDB (MaxLDBInterface):
    def __init__(self) -> None:
        self.bsp: BSPContainer = BSPContainer()
        self.materials: MaterialContainer = MaterialContainer()
        self.textures: TextureContainer = TextureContainer()
        self.lightmaps: LightMapTextureContainer = LightMapTextureContainer()
        self.exits: ExitContainer = ExitContainer()
        self.static_meshes: StaticMeshContainer = StaticMeshContainer()
        self.dynamic_lights: DynamicLightContainer = DynamicLightContainer()
        self.waypoints: WaypointContainer = WaypointContainer()
        self.fsms: FSMContainer = FSMContainer()
        self.characters: CharacterContainer = CharacterContainer()
        self.triggers: TriggerContainer = TriggerContainer()
        self.dynamic_meshes: DynamicMeshContainer = DynamicMeshContainer()
        self.items: ItemContainer = ItemContainer()
        self.pointlights: PointLightContainer = PointLightContainer()
        self.rooms: RoomContainer = RoomContainer()

    def getBsp(self) -> BSPContainer:
        return self.bsp

    def getTextures(self) -> TextureContainer:
        return self.textures
    
    def getMaterials(self) -> MaterialContainer:
        return self.materials

    def getLightMaps(self) -> LightMapTextureContainer:
        return self.lightmaps

    def getExits(self) -> ExitContainer:
        return self.exits

    def getStaticMeshes(self) -> StaticMeshContainer:
        return self.static_meshes

    def getDynamicLights(self) -> DynamicLightContainer:
        return self.dynamic_lights

    def getWaypoints(self) -> WaypointContainer:
        return self.waypoints

    def getFSMs(self) -> FSMContainer:
        return self.fsms

    def getCharacters(self) -> CharacterContainer:
        return self.characters

    def getTriggers(self) -> TriggerContainer:
        return self.triggers

    def getDynamicMeshes(self) -> DynamicMeshContainer:
        return self.dynamic_meshes

    def getItems(self) -> ItemContainer:
        return self.items

    def getPointlights(self) -> PointLightContainer:
        return self.pointlights

    def getRooms(self) -> RoomContainer:
        return self.rooms