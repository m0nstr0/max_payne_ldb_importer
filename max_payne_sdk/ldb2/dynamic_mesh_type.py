from dataclasses import dataclass

from max_payne_sdk.ldb2.aabb_type import AABB
from max_payne_sdk.ldb2.collision_shape_type import CollisionShape
from max_payne_sdk.ldb2.static_mesh_type import StaticMesh, StaticMeshContainer

@dataclass
class DynamicMeshAnimation:
    pass

@dataclass
class DynamicMesh:
    fsm_id: int
    use_light_maps: bool
    point_lights_affect: bool
    continuous_update: bool
    bullet_collision: bool
    character_collision: bool
    block_explosions: bool
    no_decals: bool
    elevator: bool
    physical_material: int
    perfab_id: int
    share_collision: bool
    aabb: AABB
    mesh: StaticMeshContainer
    collision: [CollisionShape]
    animations: [DynamicMeshAnimation]

class DynamicMeshContainer:
    def __init__(self) -> None:
        self.dynamic_meshes: list[DynamicMesh] = []

    def __getitem__(self, key):
        return self.dynamic_meshes[key]

    def __setitem__(self, key, value):
        self.dynamic_meshes[key] = value

    def __len__(self):
        return len(self.dynamic_meshes)

    def add(self, dynamic_mesh: DynamicMesh):
        self.dynamic_meshes.append(dynamic_mesh)
