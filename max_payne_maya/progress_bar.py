import maya.cmds as mc

__NUM_OPS__: int = 0
__PROGRESS_AMOUNT__: int = 0
__PROGRESS_DELTA__: float = 1.0
__MESSAGE__: str = ""


def init(num_ops: int) -> None:
    global __NUM_OPS__
    global __PROGRESS_AMOUNT__
    global __PROGRESS_DELTA__
    global __MESSAGE__
    __NUM_OPS__ = num_ops
    __PROGRESS_DELTA__ = 100.0 / __NUM_OPS__
    __PROGRESS_AMOUNT__ = 0


def hide():
    mc.progressWindow(endProgress=1)


def set_message(message: str):
    global __MESSAGE__
    __MESSAGE__ = message


def show():
    global __PROGRESS_AMOUNT__
    global __MESSAGE__
    mc.progressWindow(title="Importing MaxPayne Level", progress=0, status=__MESSAGE__, isInterruptable=True)

def update() -> bool:
    global __NUM_OPS__
    global __PROGRESS_AMOUNT__
    global __PROGRESS_DELTA__
    global __MESSAGE__
    __PROGRESS_AMOUNT__ = __PROGRESS_AMOUNT__ + __PROGRESS_DELTA__
    if mc.progressWindow(query=True, isCancelled=True):
        hide()
        mc.confirmDialog(message="File import was canceled")
        return False
    if __PROGRESS_AMOUNT__ == 0:
        mc.progressWindow(title="Importing MaxPayne Level",
                          progress=0,
                          status=__MESSAGE__,
                          isInterruptable=True)
        return True
    if __PROGRESS_AMOUNT__ >= 100:
        hide()
        return True
    mc.progressWindow(edit=True, progress=__PROGRESS_AMOUNT__, status=__MESSAGE__)
    return True
