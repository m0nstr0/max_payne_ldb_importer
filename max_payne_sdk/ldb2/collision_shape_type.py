from dataclasses import dataclass

from max_payne_sdk.ldb.vertex_type import Vertex


@dataclass
class CollisionShapeMoppData:
    origin_x: float
    origin_y: float
    origin_z: float
    mopp_code: bytes

@dataclass
class CollisionShape:
    vertices: [Vertex]
    indices: [int]
    material_indices: [int]
    is_convex: [bool]
    collision_mask: [int]
    havok_mopp: CollisionShapeMoppData
