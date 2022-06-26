from dataclasses import dataclass

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

POINT_LIGHT = 0x00010002
DIRECTIONAL_LIGHT = 0x00010003
SPOT_LIGHT = 0x00010004

SKIN = 0x00010014
ENVIRONMENT = 0x00010015
HELPER = 0x00010016

POINT_LIGHT_ANIMATION = 0x00010017
DIRECTIONAL_LIGHT_ANIMATION = 0x00010018
SPOT_LIGHT_ANIMATION = 0x00010019

POLYGON_CHUNK = 0x00010008
CHUNK_HEADER_ID = b'\x0C'

@dataclass
class KF2ChunkHeader:
    id: int
    version: uint
    size: uint

@dataclass
class TextureAnimationInfo:
    is_automatic_start: bool
    is_random_start_frame: bool
    start_frame: int
    playback_fPS: int
    #Loop 0x00 PingPong 0x01 Hold 0x02
    end_condition: int

@dataclass
class TextureV1:
    version: int
    name: str
    mip_maps_num: int
    #None 0x00 Billinear 0x01 Auto 0x02 Trilinear 0x03 Anisotropic 0x04
    filtering_type: int
    textures: list[str]
    animation_info: TextureAnimationInfo

@dataclass
class MaterialV1:
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
    sepecular_exponent: float
    emboss_factor: TextureV1
    diffuse_texture: TextureV1
    reflection_texture: TextureV1
    bump_texture: TextureV1
    opacity_texture: TextureV1
    mask_texture: TextureV1

@dataclass
class MaterialV2(MaterialV1):
    unk1: bool
    unk2: bool
    unk3: int

@dataclass
class MaterialListV0:
    version: int
    texture_dirs: str
    materials = []

@dataclass
class NodeV1:
    version: int
    name: str
    parent_name: str
    object_to_parent_tranform: list[list[list[float]]]
    has_parent: bool
    user_defined_string: str

@dataclass
class GeometryV1:
    version: int
    vertices: list[list[float]]
    normals: list[list[float]]
    vertices_per_primitive: list[uint]

@dataclass
class PolygonsV1:
    version: int
    polygons_indicies: list[int]
    polygons_per_primitive: list[uint]

@dataclass
class PolygonMaterialV1:
    version: int
    name: list[str]

@dataclass
class UVMappingV1:
    version: int
    layer: uint
    #u,v,w
    coordinates: list[list[float]]
    coordinates_per_primitive: list[uint]

@dataclass
class RefferenceToDataV0:
    version: int
    referenced_object_name: str

@dataclass
class SmoothingChunkV0:
    version: int

@dataclass
class CameraV0:
    version: int
    node: NodeV1
    fov: float
    front_plane: float
    back_plane: float

@dataclass
class AnimationKeyframe:
    frame_id: uint
    transform: list[list[float]]

@dataclass
class AnimationVisibilityframe:
    frame_id: uint
    visibility: float

@dataclass
class AnimationV0:
    version: int
    object_name: str
    fps: int
    is_looping: bool

@dataclass
class KeyframeAnimationV5:
    version: int
    animation: AnimationV0
    parent_name: str
    use_loop_interpolation: bool
    num_total_keyframes: uint
    num_key_frames: uint
    keyframes: list[AnimationKeyframe]
    num_visibility_frames: uint
    visibility_frames: list[AnimationVisibilityframe]
    loop_to_frame: uint
    frame_to_frame_interpolation_method: int
    maintain_matrix_scaling: bool

@dataclass
class MeshV2:
    node: NodeV1
    geometry: GeometryV1
    polygons: PolygonsV1
    polygon_material: PolygonMaterialV1
    uv_mapping: list[UVMappingV1]
    reference_to_data: RefferenceToDataV0
    smoothing: SmoothingChunkV0