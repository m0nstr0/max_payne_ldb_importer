import maya.OpenMayaMPx as OpenMayaMPx
import maya.api.OpenMaya as OpenMaya
import sys
import math
import max_payne_sdk.max_ldb as max_ldb
import maya.cmds as mc
import max_payne_maya.ldb.material as material
import max_payne_maya.ldb.mesh as mesh
import max_payne_maya.progress as progress

PLUGIN_NAME = "Max Payne LDB Import"
PLUGIN_COMPANY = "Bolotaev Sergey"
FILE_EXT = 'ldb'


class MaxPayneSDKTranslator(OpenMayaMPx.MPxFileTranslator):
    def __init__(self):
        OpenMayaMPx.MPxFileTranslator.__init__(self)
        self.kwargs = {}
        self.textures = []
        self.materials = []

    def haveWriteMethod(self):
        return False

    def haveReadMethod(self):
        return True

    def filter(self):
        return "*.{}".format(FILE_EXT)

    def defaultExtension(self):
        return FILE_EXT

    def identifyFile(self, file_obj, buffer, size):
        return OpenMayaMPx.MPxFileTranslator.kIsMyFileType

    def specifyDirectoryForTextures(self):
        directory_path = mc.fileDialog2(
            caption="Set texture folder",
            dialogStyle=1,
            fileMode=3
        )
        if directory_path != None and directory_path != "":
            return str(directory_path[0])
        return ""

    def endProgressBar(self):
        mc.progressWindow(endProgress=1)

    def updateProgressBar(self, message):
        self.progress_amount = self.progress_amount + self.progress_delta
        window_title = "Importing MaxPayne Level"
        if mc.progressWindow(query=True, isCancelled=True):
            self.endProgressBar()
            mc.confirmDialog(message="File import was canceled")
            return False
        if self.progress_amount == 0:
            mc.progressWindow(title=window_title,
                              progress=0,
                              status=message,
                              isInterruptable=True)
            return True
        if self.progress_amount >= 100:
            self.endProgressBar()
            return True
        mc.progressWindow(edit=True, progress=self.progress_amount, status=message)
        return True

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
        texture_directory = self.specifyDirectoryForTextures()
        if texture_directory == "":
            mc.confirmDialog(message="File import was canceled")
            return

        progressOps = progress.MayaProgressOps()
        try:
            progressOps.updateProgressBar("Importing: Reading File")
            ldb = max_ldb.MaxLDBReader().parse(file.expandedFullName())
            progressOps.setNumOps(self.calculateItems(ldb))
            mesh.MayaLDBMeshlOps(
                ldb,
                material.MayaLDBMaterialOps(ldb, texture_directory, progressOps),
                progressOps)
        except Exception:
            sys.stderr.write("Failed to import file: %s" % file.expandedFullName())
            mc.confirmDialog(message="Failed to import file: %s" % file.expandedFullName())
            progressOps.endProgressBar()
            raise

        progressOps.endProgressBar()
        mc.confirmDialog(message="File was imported")


def createMaxPayneSDKTranslator():
    return OpenMayaMPx.asMPxPtr(MaxPayneSDKTranslator())


def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject, PLUGIN_COMPANY, '1.0', "Any")
    try:
        mplugin.registerFileTranslator(PLUGIN_NAME, None, createMaxPayneSDKTranslator)
    except:
        sys.stderr.write("Failed to register translator: %s" % PLUGIN_NAME)
        raise


def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterFileTranslator(PLUGIN_NAME)
    except:
        sys.stderr.write("Failed to deregister translator: %s" % PLUGIN_NAME)
        raise
