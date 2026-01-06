import random

from max_payne_sdk.lvl2.max_camera_settings import MaxCameraSettings
from max_payne_sdk.lvl2.max_document_settings import MaxDocumentSettings
from max_payne_sdk.lvl2.max_header import MaxHeader
from max_payne_sdk.lvl2.max_light_maps import MaxLightMaps
from max_payne_sdk.lvl2.max_node_ain import MaxNodeAin
from max_payne_sdk.lvl2.max_node_dynamic_pointlight import MaxNodeDynamicPointLight
from max_payne_sdk.lvl2.max_node_enemy import MaxNodeEnemy
from max_payne_sdk.lvl2.max_node_flare import MaxNodeFlare
from max_payne_sdk.lvl2.max_node_fsm import MaxNodeFSM
from max_payne_sdk.lvl2.max_node_jump_point import MaxNodeJumpPoint
from max_payne_sdk.lvl2.max_node_level_item import MaxNodeLevelItem
from max_payne_sdk.lvl2.max_node_player import MaxNodePlayer
from max_payne_sdk.lvl2.max_node_trigger import MaxNodeTrigger
from max_payne_sdk.lvl2.max_node_waypoint import MaxNodeWayPoint
from max_payne_sdk.lvl2.max_node_world_group import MaxNodeWorldGroup
from max_payne_sdk.lvl2.max_player_groups import MaxPlayerGroups
from max_payne_sdk.lvl2.max_selection_info import MaxSelectionInfo
from max_payne_sdk.lvl2.max_textures_and_materials import MaxTexturesAndMaterials


class MaxLVL2:
    def __init__(self):
        self.file_header: MaxHeader = MaxHeader()
        self.textures_and_materials: MaxTexturesAndMaterials = MaxTexturesAndMaterials()
        self.light_maps: MaxLightMaps = MaxLightMaps()
        self.document_settings: MaxDocumentSettings = MaxDocumentSettings()
        self.selection_info: MaxSelectionInfo = MaxSelectionInfo()
        self.camera_settings: MaxCameraSettings = MaxCameraSettings()
        self.player_groups: MaxPlayerGroups = MaxPlayerGroups()
        self.node = None
        self.nodes_ids = []
        self.node_names = []

        self.addBaseNodes()

    def getNextNodeId(self):
        while True:
            next_id = random.randint(1, 2147483646)
            found = False
            for i in self.nodes_ids:
                if i == next_id:
                    found = True
                    break
            if not found:
                self.nodes_ids.append(next_id)
                return next_id

    def getNextNodeNameWithPrefix(self, prefix, first_check=False):
        while True:
            index = 0
            if index == 0 and first_check:
                new_name = prefix
            else:
                new_name = prefix + str(index)
            found = False
            for i in self.node_names:
                if i.lower() == new_name.lower():
                    found = True
                    break
            if not found:
                self.node_names.append(new_name)
                return new_name

    def addBaseNodes(self):
        self.node = MaxNodeWorldGroup(self.getNextNodeId(), self.getNextNodeNameWithPrefix('World_Group', True))
        self.node.children.append(MaxNodePlayer(self.getNextNodeId(), self.getNextNodeNameWithPrefix('Player', True)))

    def createNodeAin(self) -> MaxNodeAin:
        new_node = MaxNodeAin(self.getNextNodeId(), self.getNextNodeNameWithPrefix('AIN_'))
        return new_node

    def createNodeDynamicPointLight(self) -> MaxNodeDynamicPointLight:
        new_node = MaxNodeDynamicPointLight(self.getNextNodeId(), self.getNextNodeNameWithPrefix('Dynamic_Pointlight_'))
        return new_node

    def createNodeEnemy(self) -> MaxNodeEnemy:
        new_node = MaxNodeEnemy(self.getNextNodeId(), self.getNextNodeNameWithPrefix('Enemy_'))
        return new_node

    def createNodeFlare(self) -> MaxNodeFlare:
        new_node = MaxNodeFlare(self.getNextNodeId(), self.getNextNodeNameWithPrefix('Flare_'))
        return new_node

    def createNodeFSM(self) -> MaxNodeFSM:
        new_node = MaxNodeFSM(self.getNextNodeId(), self.getNextNodeNameWithPrefix('FSM_'))
        return new_node

    def createNodeJumpPoint(self) -> MaxNodeJumpPoint:
        new_node = MaxNodeJumpPoint(self.getNextNodeId(), self.getNextNodeNameWithPrefix('Jumppoint_'))
        return new_node

    def createNodeLevelItem(self) -> MaxNodeLevelItem:
        new_node = MaxNodeLevelItem(self.getNextNodeId(), self.getNextNodeNameWithPrefix('Level_Item_'))
        return new_node

    def createNodeMesh(self):
        pass

    def createNodePolyGroup(self):
        pass

    def createNodePortal(self):
        pass

    def createNodePrefab(self):
        pass

    def createNodeRadiosityLight(self):
        pass

    def createNodeTriangleMesh(self):
        pass

    def createNodeTrigger(self) -> MaxNodeTrigger:
        new_node = MaxNodeTrigger(self.getNextNodeId(), self.getNextNodeNameWithPrefix('Trigger_'))
        return new_node

    def createNodeVolumeLightingBox(self):
        pass

    def createNodeWaypoint(self) -> MaxNodeWayPoint:
        new_node = MaxNodeWayPoint(self.getNextNodeId(), self.getNextNodeNameWithPrefix('Waypoint_'))
        return new_node

    def getBytes(self):
        data = self.file_header.getBytes()
        data = data + self.textures_and_materials.getBytes()
        data = data + self.light_maps.getBytes()
        data = data + self.document_settings.getBytes()
        data = data + self.node.getBytes()
        data = data + self.selection_info.getBytes()
        data = data + self.camera_settings.getBytes()
        data = data + self.player_groups.getBytes()
        return data
