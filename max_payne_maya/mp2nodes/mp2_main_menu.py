import maya.cmds as cmds
import maya.mel as mel

from max_payne_maya.mp2nodes.mp2_export_lv2 import export_lv2
from max_payne_maya.mp2nodes.mp2_node_ids import MP2_AIN_NODE_NAME, MP2_ENEMY_NODE_NAME, \
    MP2_DYNAMIC_POINT_LIGHT_NODE_NAME, MP2_LEVEL_ITEM_NODE_NAME, MP2_VOLUME_LIGHTING_BOX_NODE_NAME, MP2_FSM_NODE_NAME, \
    MP2_WORLD_GROUP_NODE_NAME, MP2_TRIGGER_NODE_NAME, MP2_PLAYER_NODE_NAME, MP2_JUMP_POINT_NODE_NAME, \
    MP2_WAY_POINT_NODE_NAME, MP2_FLARE_NODE_NAME

MENU_NAME = "MaxPayne2Tools"


def show_about(*args):
    cmds.confirmDialog(
        title="About",
        message="My Custom Maya Plugin v1.0",
        button=["OK"],
        defaultButton="OK"
    )




def export_lv2_command(*args):
    export_lv2()

    # if sel:
    #     all_children = cmds.listRelatives(sel, allDescendents=True, fullPath=True) or []
    #     is_first = True
    #     for node in all_children:
    #         if is_first and cmds.nodeType(node) != MP2_WORLD_GROUP_NODE_NAME:
    #             cmds.confirmDialog(
    #                 title=f"The first node must be of type '{MP2_WORLD_GROUP_NODE_NAME}'.",
    #                 message="Error",
    #                 button=["OK"]
    #             )
    #             return
    #
    #         if cmds.nodeType(node) == MP2_WORLD_GROUP_NODE_NAME:
    #             if world_group_node is not None:
    #                 cmds.confirmDialog(
    #                     title=f"Only one node of type '{MP2_WORLD_GROUP_NODE_NAME}' is allowed.",
    #                     message="Error",
    #                     button=["OK"]
    #                 )
    #                 return
    #             world_group_node = node
    #
    #         if cmds.nodeType(node) == MP2_PLAYER_NODE_NAME:
    #             if player_node is not None:
    #                 cmds.confirmDialog(
    #                     title=f"Only one node of type '{MP2_PLAYER_NODE_NAME}' is allowed.",
    #                     message="Error",
    #                     button=["OK"]
    #                 )
    #                 return
    #             player_node = node
    #
    #         is_first = False
    #
    #     print(all_children)
    #     print(cmds.nodeType(all_children[2]))



def mp2_create_main_menu():
    main_window = mel.eval('$tempVar=$gMainWindow')

    # Проверяем, существует ли меню (чтобы не создавать дубли)
    if cmds.menu(MENU_NAME, exists=True):
        cmds.deleteUI(MENU_NAME)

    # Создаём меню
    menu = cmds.menu(
        MENU_NAME,
        label="Max Payne 2",
        parent=main_window,
        tearOff=True
    )

    menu_create = cmds.menuItem(
        label="Create",
        parent=MENU_NAME,
        subMenu=True
    )

    cmds.menuItem(label="AIN", parent=menu_create, image=MP2_AIN_NODE_NAME + '.png', command=lambda *_: cmds.createNode(MP2_AIN_NODE_NAME))
    cmds.menuItem(label="Flare", parent=menu_create, image=MP2_FLARE_NODE_NAME + '.png', command=lambda *_: cmds.createNode(MP2_FLARE_NODE_NAME))
    cmds.menuItem(label="Way Point", parent=menu_create, image=MP2_WAY_POINT_NODE_NAME + '.png', command=lambda *_: cmds.createNode(MP2_WAY_POINT_NODE_NAME))
    cmds.menuItem(label="Jump Point", parent=menu_create, image=MP2_JUMP_POINT_NODE_NAME + '.png', command=lambda *_: cmds.createNode(MP2_JUMP_POINT_NODE_NAME))
    cmds.menuItem(label="Player", parent=menu_create, image=MP2_PLAYER_NODE_NAME + '.png', command=lambda *_: cmds.createNode(MP2_PLAYER_NODE_NAME))
    cmds.menuItem(label="Trigger", parent=menu_create, image=MP2_TRIGGER_NODE_NAME + '.png', command=lambda *_: cmds.createNode(MP2_TRIGGER_NODE_NAME))
    cmds.menuItem(label="World Group", parent=menu_create, image=MP2_WORLD_GROUP_NODE_NAME + '.png', command=lambda *_: cmds.createNode(MP2_WORLD_GROUP_NODE_NAME))
    cmds.menuItem(label="FSM", parent=menu_create, image=MP2_FSM_NODE_NAME + '.png', command=lambda *_: cmds.createNode(MP2_FSM_NODE_NAME))
    cmds.menuItem(label="Volume Lighting Box", parent=menu_create, image=MP2_VOLUME_LIGHTING_BOX_NODE_NAME + '.png', command=lambda *_: cmds.createNode(MP2_VOLUME_LIGHTING_BOX_NODE_NAME))
    cmds.menuItem(label="Level Item", parent=menu_create, image=MP2_LEVEL_ITEM_NODE_NAME + '.png', command=lambda *_: cmds.createNode(MP2_LEVEL_ITEM_NODE_NAME))
    cmds.menuItem(label="Dynamic PointLight", parent=menu_create, image=MP2_DYNAMIC_POINT_LIGHT_NODE_NAME + '.png', command=lambda *_: cmds.createNode(MP2_DYNAMIC_POINT_LIGHT_NODE_NAME))
    cmds.menuItem(label="Enemy", parent=menu_create, image=MP2_ENEMY_NODE_NAME + '.png', command=lambda *_: cmds.createNode(MP2_ENEMY_NODE_NAME))
    cmds.menuItem(parent=menu_create, divider=True)
    cmds.menuItem(label="Material", parent=menu_create)

    export_menu = cmds.menuItem(
        label="Export",
        parent=MENU_NAME,
        subMenu=True
    )
    cmds.menuItem(label="Export to LV2", parent=export_menu, command=export_lv2_command)
    cmds.menuItem(label="Export to LDB", parent=export_menu, command=lambda *_: cmds.createNode(MP2_FLARE_NODE_NAME))

    cmds.menuItem(parent=MENU_NAME, divider=True)

    cmds.menuItem(
        label="About",
        parent=MENU_NAME,
        command=show_about
    )


def mp2_delete_main_menu():
    if cmds.menu(MENU_NAME, exists=True):
        cmds.deleteUI(MENU_NAME)
