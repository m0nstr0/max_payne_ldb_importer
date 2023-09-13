from dataclasses import dataclass

from max_payne_sdk.ldb.vertex_type import Vertex


@dataclass
class VolumeLightRGB:
    r: float
    g: float
    b: float

@dataclass
class VolumeLightAABB:
    min_point: Vertex
    max_point: Vertex
@dataclass
class VolumeLight:
    grid_height: int
    grid_width: int
    grid_depth: int
    aabb: VolumeLightAABB
    rgb: [VolumeLightRGB]