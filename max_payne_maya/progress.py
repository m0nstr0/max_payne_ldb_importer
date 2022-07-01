import maya.cmds as mc

class MayaProgressOps:
    def __init__ (self):
        self.progress_amount = 0
        self.progress_delta = 0

    def setNumOps(self, num_ops):
        self.progress_delta = 100.0 / num_ops

    def endProgressBar(self):
        mc.progressWindow(endProgress=1)

    def updateProgressBar(self, message):
        self.progress_amount = self.progress_amount + self.progress_delta
        window_title = "Importing MaxPayne Level"
        if mc.progressWindow( query=True, isCancelled=True ):
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