from max_payne_sdk.lvl2.max_camera_settings import MaxCameraSettings
from max_payne_sdk.lvl2.max_document_settings import MaxDocumentSettings
from max_payne_sdk.lvl2.max_header import MaxHeader
from max_payne_sdk.lvl2.max_light_maps import MaxLightMaps
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
        self.nodes = MaxNodeWorldGroup()
        self.selection_info: MaxSelectionInfo = MaxSelectionInfo()
        self.camera_settings: MaxCameraSettings = MaxCameraSettings()
        self.player_groups: MaxPlayerGroups = MaxPlayerGroups()

    def getBytes(self):
        data = self.file_header.getBytes()
        data = data + self.textures_and_materials.getBytes()
        data = data + self.light_maps.getBytes()
        data = data + self.document_settings.getBytes()
        data = data + self.nodes.getBytes()
        data = data + self.selection_info.getBytes()
        data = data + self.camera_settings.getBytes()
        data = data + self.player_groups.getBytes()
        return data