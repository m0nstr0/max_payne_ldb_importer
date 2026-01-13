from PySide2 import QtCore, QtGui, QtWidgets
# from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance
# import maya.cmds as cmds
#
def get_ae_parent():
    ptr = omui.MQtUtil.getCurrentParent()
    return wrapInstance(int(ptr), QtWidgets.QWidget)


import maya.cmds as cmds
import maya.OpenMayaUI as omui
# from PySide6 import QtWidgets
# from shiboken6 import wrapInstance


def myLocatorAE_create(nodeName):
    #layout_name = cmds.columnLayout(adjustableColumn=True)

    # Получаем Qt widget
    #ptr = omui.MQtUtil.findLayout(layout_name)
    #widget = wrapInstance(int(ptr), QtWidgets.QWidget)

    layout_name = cmds.columnLayout(adjustableColumn=True)

    ptr = omui.MQtUtil.findLayout(layout_name)
    widget = wrapInstance(int(ptr), QtWidgets.QWidget)

    # ВАЖНО: использовать существующий layout
    qt_layout = widget.layout()
    if qt_layout is None:
        qt_layout = QtWidgets.QVBoxLayout(widget)

    label = QtWidgets.QLabel(f"Node: {nodeName}")
    button = QtWidgets.QPushButton("Test Button")

    qt_layout.addWidget(label)
    qt_layout.addWidget(button)

    button.clicked.connect(lambda: print("Clicked:", nodeName))

    widget._my_locator_ui = (label, button)

    # widget = get_ae_parent()
    # qt_layout = QtWidgets.QVBoxLayout(widget)
    # qt_layout.setContentsMargins(4, 4, 4, 4)
    #
    # label = QtWidgets.QLabel(f"Node: {nodeName}")
    # button = QtWidgets.QPushButton("Test Button")
    #
    # qt_layout.addWidget(label)
    # qt_layout.addWidget(button)
    #
    # button.clicked.connect(lambda: print("Clicked:", nodeName))
    #
    # # Защита от GC
    # widget._my_locator_ui = (label, button)

def myLocatorAE_update(nodeName):
    # Можно обновлять UI при смене selection / attr
    pass

# def create_ui():
#     # parent = get_ae_layout()
#     #
#     # # Create layout for the parent widget
#     # layout = QtWidgets.QVBoxLayout(parent)
#     # layout.setContentsMargins(2, 2, 2, 2)
#     #
#     # # Example: A Button
#     # btn = QtWidgets.QPushButton("PySide2 Button", parent)
#     # btn.setObjectName("myUniqueAEButton")
#     #
#     # btn.clicked.connect(lambda: print("Clicked on: "))
#     # layout.addWidget(btn)
#
#     parent = get_ae_parent()
#     if not parent:
#         return
#
#     # Add a layout to the parent provided by Maya
#     layout = QtWidgets.QVBoxLayout(parent)
#
#     # Create an editable Combobox (PySide2)
#     combo = QtWidgets.QComboBox(parent)
#     combo.setObjectName("myCustomEditableCombo")
#     combo.setEditable(True)  # Make it editable
#     combo.addItems(["Default A", "Default B", "Default C"])
#
#     # Sync with attribute on change
#     combo.currentTextChanged.connect(lambda text: cmds.setAttr(f".myAttr", text, type="string"))
#
#     layout.addWidget(combo)
#
# def update_ui(node_name):
#     # """Updates the widget when selection changes to a new node."""
#     # parent = get_ae_layout()
#     # btn = parent.findChild(QtWidgets.QPushButton, "myUniqueAEButton")
#     #
#     # if btn:
#     #     # Re-map the signal to the new node name
#     #     btn.clicked.disconnect()
#     #     btn.clicked.connect(lambda: print("Updated node focus: "))
#     parent = get_ae_parent()
#     if parent:
#         combo = parent.findChild(QtWidgets.QComboBox, "myCustomEditableCombo")
#         if combo:
#             # Refresh logic for new node selection
#             combo.blockSignals(True)
#             current_val = cmds.getAttr(f".myAttr")
#             combo.setEditText(current_val or "")
#             combo.blockSignals(False)
