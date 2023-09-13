import maya.OpenMayaMPx as OpenMayaMPx
import maya.api.OpenMaya as OpenMaya
from maya.OpenMaya import MGlobal
import sys
from max_payne_maya.ldb import LDBImporter
import maya.cmds as mc



PLUGIN_NAME = "Max Payne LDB Import"
PLUGIN_COMPANY = "Bolotaev Sergey"

class MaxPayneLDBFileTranslator(OpenMayaMPx.MPxFileTranslator):
    def __init__(self):
        OpenMayaMPx.MPxFileTranslator.__init__(self)
        self.kwargs = {}

    def haveWriteMethod(self):
        return False

    def haveReadMethod(self):
        return True

    def filter(self):
        return "*.ldb"

    def defaultExtension(self):
        return "ldb"

    def identifyFile(self, file_obj, buffer, size):
        return OpenMayaMPx.MPxFileTranslator.kIsMyFileType

    def calculateItems(self, ldb):
        num_ops = len(ldb.getMaterials().materials)
        num_ops = num_ops + len(ldb.getRooms().rooms)
        num_ops = num_ops + len(ldb.getStaticMeshes().static_meshes)
        num_ops = num_ops + len(ldb.getDynamicMeshes().dynamic_meshes)
        for static_mesh in ldb.getStaticMeshes().static_meshes:
            num_ops = num_ops + len(static_mesh.polygons.polygons)
        for dynamic_mesh in ldb.getDynamicMeshes().dynamic_meshes:
            num_ops = num_ops + len(dynamic_mesh.polygons.polygons)
        return num_ops

    def reader(self, file, options, mode):
        try:
            LDBImporter().doImport(file.expandedFullName())
        except Exception as error:
            MGlobal.displayError(error)
            sys.stderr.write("Failed to import file: %s" % file.expandedFullName())
            mc.confirmDialog(message="Failed to import file: %s" % file.expandedFullName())
            raise

def createMaxPayneLDBFileTranslator():
    return OpenMayaMPx.asMPxPtr(MaxPayneLDBFileTranslator())


def initializePlugin(maya_object):
    plugin = OpenMayaMPx.MFnPlugin(maya_object, PLUGIN_COMPANY, '1.0', "Any")
    try:
        plugin.registerFileTranslator(PLUGIN_NAME, None, createMaxPayneLDBFileTranslator)
    except Exception:
        sys.stderr.write("Failed to register Max Payne LDB file translator: %s" % PLUGIN_NAME)
        raise

def uninitializePlugin(maya_object):
    plugin = OpenMayaMPx.MFnPlugin(maya_object)
    try:
        plugin.deregisterFileTranslator(PLUGIN_NAME)
    except Exception:
        sys.stderr.write("Failed to deregister Max Payne LDB file translator: %s" % PLUGIN_NAME)
        raise
