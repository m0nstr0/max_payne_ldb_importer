from dataclasses import dataclass

from max_payne_sdk.ldb.vertex_type import Vertex


@dataclass
class AABB:
    min_point: [float]
    max_point: [float]
    pivot_point: [float]
