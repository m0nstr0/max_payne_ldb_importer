from dataclasses import dataclass

CHUNK_HEADER_ID = b'\x0C'
MATERIAL_LIST = 0x0001000f
MATERIAL = 0x0010010
TEXTURE = 0x00010011
MESH = 0x00010005
NODE = 0x00010000
GEOMETRY = 0x00010006
POLYGONS = 0x00010007
POLYGON_MATERIAL = 0x0001000C
UVMAPPING = 0x0001000e
REFFERENCE_TO_DATA = 0x0001001A
SMOOTHING = 0x0001000B
CAMERA = 0x00010001
KEYFRAME_ANIMATION = 0x00010012
ANIMATION = 0x00010013
ENVIRONMENT = 0x00010015
SKIN = 0x00010014
POINT_LIGHT = 0x00010002
DIRECTIONAL_LIGHT = 0x00010003
SPOT_LIGHT = 0x00010004
HELPER = 0x00010016
POINT_LIGHT_ANIMATION = 0x00010017
DIRECTIONAL_LIGHT_ANIMATION = 0x00010018
SPOT_LIGHT_ANIMATION = 0x00010019
POLYGON_CHUNK = 0x00010008

@dataclass
class KF2ChunkHeader:
    id: int
    version: int
    size: int

@dataclass
class TextureAnimationInfo:
    is_automatic_start: bool
    is_random_start_frame: bool
    start_frame: int
    playback_fps: int
    #Loop 0x00 PingPong 0x01 Hold 0x02
    end_condition: int

@dataclass
class Texture:
    version: int
    name: str
    mip_maps_num: int
    #None 0x00 Billinear 0x01 Auto 0x02 Trilinear 0x03 Anisotropic 0x04
    filtering_type: int
    textures: []
    animation_info: TextureAnimationInfo

@dataclass
class Material:
    version: int
    name: str
    is_two_sided: bool
    is_fogging: bool
    is_diffuse_combined: bool
    is_invisible_geometry: bool
    has_vertex_alpha: bool
    has_diffuse_texture: bool
    has_reflection_texture: bool
    has_bump_texture: bool
    has_opacity_texture: bool
    has_mask_texture: bool
    has_lit: bool
    #None 0x00 Color 0x01 Gourand 0x02
    diffuse_color_type: int
    #None 0x00 Gourand 0x01
    specular_color_type: int
    #Phong 0x00 Environment 0x01 UVW2 0x02
    lit_type: int
    #UVW1 0x00 UVW2 0x01
    mask_texture_type: int
    #Copy 0x00 Additive 0x01 Multiplicative 0x02
    diffuse_texture_type: int
    #Copy 0x00 Additive 0x01 Multiplicative 0x02
    reflection_texture_type: int
    ambient_color_r: float
    ambient_color_g: float
    ambient_color_b: float
    ambient_color_a: float
    diffuse_color_r: float
    diffuse_color_g: float
    diffuse_color_b: float
    diffuse_color_a: float
    specular_color_r: float
    specular_color_g: float
    specular_color_b: float
    specular_color_a: float
    vertex_alpha: float
    specular_exponent: float
    emboss_factor: Texture
    diffuse_texture: Texture
    reflection_texture: Texture
    bump_texture: Texture
    opacity_texture: Texture
    mask_texture: Texture
    #max payne 2 flags (Material version 1)
    unk1: bool
    unk2: bool
    unk3: int

@dataclass
class MaterialList:
    version: int
    texture_dirs: str
    materials: []

@dataclass
class Node:
    version: int
    name: str
    parent_name: str
    object_to_parent_transform: []
    has_parent: bool
    user_defined_string: str

@dataclass
class Camera:
    version: int
    node: Node
    fov: float
    front_plane: float
    back_plane: float

@dataclass
class AnimationKeyframe:
    frame_id: int
    transform: []

@dataclass
class AnimationVisibilityframe:
    frame_id: int
    visibility: float

@dataclass
class Animation:
    version: int
    object_name: str
    fps: int
    is_looping: bool

@dataclass
class KeyframeAnimation:
    version: int
    animation: Animation
    parent_name: str
    use_loop_interpolation: bool
    num_total_keyframes: int #uint
    num_key_frames: int #uint
    keyframes: []
    num_visibility_frames: int #uint
    visibility_frames: []
    loop_to_frame: int
    frame_to_frame_interpolation_method: int
    maintain_matrix_scaling: bool

@dataclass
class Geometry:
    version: int
    vertices: [] #list[list[float]]
    normals: [] #list[list[float]]
    vertices_per_primitive: [] #list[int] #uint

@dataclass
class Polygons:
    version: int
    polygons_indices: [] #list[int]
    polygons_per_primitive: [] #list[int] #uint

@dataclass
class PolygonMaterial:
    version: int
    name: [] #list[str]

@dataclass
class UVMapping:
    version: int
    layer: int #uint
    #u,v,w
    coordinates: [] #list[list[float]]
    coordinates_per_primitive: [] #list[int] #uint

@dataclass
class RefferenceToData:
    version: int
    referenced_object_name: str

@dataclass
class SmoothingChunk:
    version: int

@dataclass
class Mesh:
    version: int
    node: Node
    geometry: Geometry
    polygons: Polygons
    polygon_material: PolygonMaterial
    uv_mapping: [] #list[UVMappingV1]
    reference_to_data: RefferenceToData
    smoothing: SmoothingChunk

@dataclass
class SkinVertex:
    vertex_index: int
    vertex_bone_indices: []
    vertex_weights: []

@dataclass
class Skin:
    version: int
    skin_object_names: []
    skeleton_object_names: []
    skin_vertices: []




















@dataclass
class EnvironmentV0:
    version: int
    ambient_light_color_r: int
    ambient_light_color_g: int
    ambient_light_color_b: int
    ambient_light_color_a: int
    clearing_color_r: int
    clearing_color_g: int
    clearing_color_b: int
    clearing_color_a: int



@dataclass
class Geometry:
    version: int
    vertices: [] #list[list[float]]
    normals: [] #list[list[float]]
    vertices_per_primitive: [] #list[int] #uint