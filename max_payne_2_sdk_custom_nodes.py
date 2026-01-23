import maya.api.OpenMaya as OpenMaya
from max_payne_maya.mp2nodes.mp2_main_menu import mp2_create_main_menu, mp2_delete_main_menu
from max_payne_maya.mp2nodes.mp2_node_list import registerNodes, deregisterNodes

PLUGIN_NAME = "Max Payne 2 Custom Nodes For LDB Import"
PLUGIN_COMPANY = "Bolotaev Sergey"

def maya_useNewAPI():
    """Tells Maya to use Python API 2.0."""
    pass

def initializePlugin(maya_object):
    mp2_create_main_menu()
    plugin = OpenMaya.MFnPlugin(maya_object, PLUGIN_COMPANY, '1.0')
    registerNodes(plugin)


def uninitializePlugin(maya_object):
    mp2_delete_main_menu()
    plugin = OpenMaya.MFnPlugin(maya_object)
    deregisterNodes(plugin)
