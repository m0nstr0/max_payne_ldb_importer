import maya.cmds as mc
import max_payne_sdk.max_ldb as max_ldb

from max_payne_maya.ldb.ldb_proxy import MayaLDBProxy
from max_payne_maya.ldb.mesh import MayaLDBMeshlOps
import max_payne_maya.ldb.material as material
import max_payne_maya.progress_bar as progress_bar

class LDBImporter:
    def __init__(self):
        pass

    @staticmethod
    def setDirectoryPathForTextures() -> str:
        directory_path = mc.fileDialog2(
            caption="Select a folder for textures",
            dialogStyle=1,
            fileMode=3
        )
        if directory_path is not None and directory_path != "":
            return str(directory_path[0])
        return ""

    def calcAmountOfActions(self, ldb_proxy) -> int:
        return ldb_proxy.getMaterialsNum() + ldb_proxy.getRoomsNum() + ldb_proxy.getDynamicMeshesNum() + ldb_proxy.getStaticMeshesNum()

    def doImport(self, file_path: str) -> None:
        texture_directory = self.setDirectoryPathForTextures()
        if texture_directory == "":
            mc.confirmDialog(message="File import was canceled")
            return

        progress_bar.set_message("Importing: Parsing File")
        progress_bar.init(1)
        progress_bar.show()

        try:
            ldb_proxy = MayaLDBProxy(max_ldb.MaxLBDReaderFactory.createReader(file_path).parse())
            progress_bar.init(self.calcAmountOfActions(ldb_proxy))
            materials_dict = material.processMaterials(ldb_proxy, texture_directory)
            MayaLDBMeshlOps(ldb_proxy, materials_dict).processGeometry()
        except Exception as error:
            progress_bar.hide()
            raise error

        progress_bar.hide()
        mc.confirmDialog(message="File was imported")
        return
