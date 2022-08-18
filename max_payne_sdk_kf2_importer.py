import maya.OpenMayaMPx as OpenMayaMPx
import sys
import max_payne_sdk.max_kf2 as max_kf2
import maya.cmds as mc
import max_payne_maya.kf2 as maya_kf2

PLUGIN_NAME = "Max Payne KF2 Import"
PLUGIN_COMPANY = "Bolotaev Sergey"
FILE_KF2_EXT = 'kf2'
FILE_KFS_EXT = 'kfs'

class MaxPayneKF2Translator(OpenMayaMPx.MPxFileTranslator):
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
        return "*.{}".format(FILE_KF2_EXT)

    def defaultExtension(self):
        return FILE_KF2_EXT

    def identifyFile(self, file_obj, buffer, size):
        return OpenMayaMPx.MPxFileTranslator.kIsMyFileType

    def reader(self, file, options, mode):
        try:
            kf2 = max_kf2.MaxKF2Reader().parse(file.expandedFullName())
            dialog = maya_kf2.KF2ImportDialog(kf2)
            dialog.show()
        except Exception:
            sys.stderr.write("Failed to import file: %s" % file.expandedFullName())
            mc.confirmDialog(message = "Failed to import file: %s" % file.expandedFullName())
            raise

def createMaxPayneKF2Translator():
    return OpenMayaMPx.asMPxPtr(MaxPayneKF2Translator())


def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject, PLUGIN_COMPANY, '1.0', "Any")
    try:
        mplugin.registerFileTranslator(PLUGIN_NAME, None, createMaxPayneKF2Translator)
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
