from max_payne_sdk.lvl2.max_chunk import MaxChunk
from max_payne_sdk.lvl2.max_pack import packUInt, packDouble, packBool, packInt, packString, packULong, packFloat, \
    packUChar


class MaxDocumentSettings:
    def __init__(self):
        self.unknown1 = 0
        #DocumentRendererSettings
        self.renderer_back_plane = 200.0
        self.renderer_front_plane = 0.10
        self.renderer_FOV = 70.0
        self.exit_acceleration = True
        # 0 - Diffuse Only, 1 - LightMapOnly, 2 - Diffuse + LightMap, 3 - LightLayer Only
        self.texturing_mode = 0
        self.renderer_connected_rooms = 3
        self.moddeling_rotate_angle_value = 2.0
        self.moddeling_angle_snap = '0.5;1;1.25;2;2.5;5;10;11.25;15;22.5;45'
        self.moddeling_grid_scale_Steps = '0.0078125;0.015625;0.03125;0.0625;0.125;0.25;0.5;1.0;2.0;4.0;8.0;16.0;32.0;64.0;128.0;256.0;512.0'
        self.texturing_default_uv_scaling = 128
        self.texturing_light_map_res = 2.0
        self.radiosity_average_light_map_border = False
        self.radiosity_view_port_size = 512
        self.radiosity_global_light_map_res = 100
        self.radiosity_default_light_color = 16777215
        self.radiosity_default_light_intensity = 100
        self.radiosity_gis_max_energy_per_shot = 2.0
        self.radiosity_gis_stop_at_energy = 0.50
        self.radiosity_gis_ignore_portals = True
        self.export_parameters = ''
        #RendererBackgroundColor
        self.R = 0
        self.G = 0
        self.B = 0
        self.A = 255

    def getBytes(self) -> []:
        data = [packUInt(self.unknown1),
                packDouble(self.renderer_back_plane),
                packDouble(self.renderer_front_plane),
                packDouble(self.renderer_FOV),
                packBool(self.exit_acceleration),
                packInt(self.texturing_mode),
                packUInt(self.renderer_connected_rooms),
                packDouble(self.moddeling_rotate_angle_value),
                packString(self.moddeling_angle_snap),
                packString(self.moddeling_grid_scale_Steps),
                packUInt(self.texturing_default_uv_scaling),
                packDouble(self.texturing_light_map_res),
                packBool(self.radiosity_average_light_map_border),
                packUInt(self.radiosity_view_port_size),
                packDouble(self.radiosity_global_light_map_res),
                packULong(self.radiosity_default_light_color),
                packFloat(self.radiosity_default_light_intensity),
                packFloat(self.radiosity_gis_max_energy_per_shot),
                packFloat(self.radiosity_gis_stop_at_energy),
                packBool(self.radiosity_gis_ignore_portals),
                packString(self.export_parameters),
                packUChar(self.R),
                packUChar(self.G),
                packUChar(self.B),
                packUChar(self.A)
                ]

        max_chunk = MaxChunk(0, 6)
        return max_chunk.getBytes(data)

