import maya.api.OpenMaya as OpenMaya
from max_payne_maya.mp2nodes.mp2_node_ids import MP2_STATIC_MESH_NODE_ID, MP2_STATIC_MESH_NODE_NAME
from max_payne_maya.mp2nodes.mp2_node_mesh import MP2NodeMesh


class MP2NodeStaticMesh(MP2NodeMesh):
    NODE_ID = OpenMaya.MTypeId(MP2_STATIC_MESH_NODE_ID)
    NODE_NAME = MP2_STATIC_MESH_NODE_NAME
