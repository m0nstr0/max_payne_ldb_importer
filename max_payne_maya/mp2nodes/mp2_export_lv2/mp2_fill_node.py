import math

import maya.cmds as cmds
import maya.mel as mel
import maya.api.OpenMaya as OpenMaya

from max_payne_maya.mp2nodes.mp2_node_ids import MP2_LEVEL_ITEM_NODE_NAME, MP2_ENEMY_NODE_NAME, MP2_TRIGGER_NODE_NAME, \
    MP2_FLARE_NODE_NAME, MP2_FSM_NODE_NAME, MP2_DYNAMIC_POINT_LIGHT_NODE_NAME, MP2_VOLUME_LIGHTING_BOX_NODE_NAME, \
    MP2_LEVEL_ITEM_NAMES_COMMON, MP2_USE_ACTIVATE_ANIMATIONS, MP2_FLARE_NAMES_COMMON, MP2_ENEMY_NAMES_COMMON, \
    MP2_DEFAULT_PLAYER_GROUPS
from max_payne_sdk.lvl2.max_node_mesh import MaxNodeMesh, MaxNodeMeshPolygon, MaxNodeMeshTriangle


def fill_node_base_data(lv2_node, dg_node):
    lv2_node.node_translate = dg_node["translate"]
    lv2_node.node_matrix33 = dg_node["matrix"]
    lv2_node.aabb_min = dg_node["bb_min"]
    lv2_node.aabb_max = dg_node["bb_max"]
    lv2_node.radius = dg_node["radius"]
    if dg_node['type'] != 'mesh':
        lv2_node.node_is_visible = not cmds.getAttr(dg_node["name"] + ".na_hidden")
        lv2_node.node_exclude_from_game = cmds.getAttr(dg_node["name"] + ".na_excludeFromGame")
        lv2_node.node_exclude_from_lighting = cmds.getAttr(dg_node["name"] + ".na_excludeFromLighting")
        lv2_node.node_enable_export_regrouping = cmds.getAttr(dg_node["name"] + ".na_enableExportRegrouping")
    lv2_node.node_gameplay_critical = True
    lv2_node.node_name = dg_node["name"].split('|')[-1]


def fill_node_level_item(lv2_node, dg_node):
    if cmds.getAttr(dg_node["name"] + ".na_itemNameUseCustom"):
        lv2_node.item_type = cmds.getAttr(dg_node["name"] + ".na_itemNameCustom")
        return

    lv2_node.item_type = MP2_LEVEL_ITEM_NAMES_COMMON[cmds.getAttr(dg_node["name"] + ".na_itemNameCommon")]


def fill_node_trigger(lv2_node, dg_node):
    lv2_node.radius = cmds.getAttr(dg_node["name"] + ".na_radius")
    lv2_node.node_gameplay_critical = True
    lv2_node.activator_player = cmds.getAttr(dg_node["name"] + ".na_player")
    lv2_node.activator_use = cmds.getAttr(dg_node["name"] + ".na_use")
    lv2_node.activator_enemy = cmds.getAttr(dg_node["name"] + ".na_enemy")
    lv2_node.activator_bullet = cmds.getAttr(dg_node["name"] + ".na_bullet")
    lv2_node.activator_look_at = cmds.getAttr(dg_node["name"] + ".na_lookAt")
    lv2_node.activator_visibility = cmds.getAttr(dg_node["name"] + ".na_visibility")

    if cmds.getAttr(dg_node["name"] + ".na_activatorsAnimationUseCustom"):
        lv2_node.activator_use_animation = cmds.getAttr(dg_node["name"] + ".na_activatorsAnimationCustom")
        return

    lv2_node.activator_use_animation = MP2_USE_ACTIVATE_ANIMATIONS[
        cmds.getAttr(dg_node["name"] + ".na_activatorsAnimationCommon")]


def fill_node_enemy(lv2_node, dg_node):
    if cmds.getAttr(dg_node["name"] + ".na_skinUseCustom"):
        lv2_node.enemy_skin = cmds.getAttr(dg_node["name"] + ".na_skinCustom")
    else:
        lv2_node.enemy_skin = MP2_ENEMY_NAMES_COMMON[cmds.getAttr(dg_node["name"] + ".na_skinCommon")]

    lv2_node.enemy_group = MP2_DEFAULT_PLAYER_GROUPS[cmds.getAttr(dg_node["name"] + ".na_enemyGroup")]

    if cmds.getAttr(dg_node["name"] + ".na_activatorsAnimationUseCustom"):
        lv2_node.activator_use_animation = cmds.getAttr(dg_node["name"] + ".na_activatorsAnimationCustom")
    else:
        lv2_node.activator_use_animation = MP2_USE_ACTIVATE_ANIMATIONS[
            cmds.getAttr(dg_node["name"] + ".na_activatorsAnimationCommon")]


def fill_node_flare(lv2_node, dg_node):
    if cmds.getAttr(dg_node["name"] + ".na_flareNameUseCustom"):
        lv2_node.flare_name = cmds.getAttr(dg_node["name"] + ".na_flareNameCustom")
        return

    lv2_node.flare_name = MP2_FLARE_NAMES_COMMON[cmds.getAttr(dg_node["name"] + ".na_flareNameCommon")]


def fill_node_fsm(lv2_node, dg_node):
    pass


def fill_node_dynamic_point_light(lv2_node, dg_node):
    pass


def fill_node_volume_lighting_box(lv2_node, dg_node):
    pass


def get_maya_mesh(dg_node):
    selection_list = OpenMaya.MSelectionList()
    dag_name = dg_node['name']
    try:
        selection_list.add(dag_name)
    except:
        OpenMaya.MGlobal.displayError(f"Не удалось найти узел: {dag_name}")
        return None, None

    mesh_obj = OpenMaya.MObject()
    try:
        mesh_obj = selection_list.getDependNode(0)
    except:
        OpenMaya.MGlobal.displayError("Не удалось получить MObject")
        return None, None

    # Проверяем тип
    if mesh_obj.apiType() != OpenMaya.MFn.kMesh:
        OpenMaya.MGlobal.displayError(f"Узел {dag_name} не является сеткой")
        return None, None

    # Создаём MFnMesh
    try:
        mesh_fn = OpenMaya.MFnMesh(mesh_obj)
        poly_it = OpenMaya.MItMeshPolygon(mesh_obj)
        return mesh_fn, poly_it
    except:
        OpenMaya.MGlobal.displayError("Ошибка при создании MFnMesh")
        return None, None


def should_reverse_edges(p0, p1, p2, poly_norm):
    # Векторное произведение
    nx = (p1[1] - p0[1]) * (p2[2] - p0[2]) - (p1[2] - p0[2]) * (p2[1] - p0[1])
    ny = (p1[2] - p0[2]) * (p2[0] - p0[0]) - (p1[0] - p0[0]) * (p2[2] - p0[2])
    nz = (p1[0] - p0[0]) * (p2[1] - p0[1]) - (p1[1] - p0[1]) * (p2[0] - p0[0])

    dot = nx * poly_norm[0] + ny * poly_norm[1] + nz * poly_norm[2]

    if dot < 0.0:
        return True
    else:
        return False

def fill_node_mesh(lv2_node: MaxNodeMesh, dg_node):
    mesh, poly = get_maya_mesh(dg_node)
    if mesh is None or poly is None:
        return

    vertices = mesh.getPoints()
    for vertex in vertices:
        lv2_node.addVertex([vertex.x, vertex.y, - vertex.z])

    poly_iter = poly #OpenMaya.MItMeshPolygon(dg_node['name'])
    while not poly_iter.isDone():
        poly_normal = poly_iter.getNormal()
        center = poly_iter.center()
        num_triangles = poly_iter.numTriangles()
        poly_edges = poly_iter.getEdges()

        lv2_polygon = MaxNodeMeshPolygon()
        lv2_polygon.setMaterial('Max_Bick', 'Default')
        lv2_polygon.polygon_id = poly_iter.index()

        lv2_polygon.setNormal([poly_normal.x, poly_normal.y, - poly_normal.z])

        triangles = poly_iter.getTriangles()
        for triangle_id in range(num_triangles):
            triangle = MaxNodeMeshTriangle()
            triangle.normal = lv2_polygon.normal[:]
            triangle.indices = [
                triangles[1][triangle_id * 3],
                triangles[1][triangle_id * 3 + 2],
                triangles[1][triangle_id * 3 + 1]
            ]
            lv2_polygon.triangles.append(triangle)

        edges = []
        for edge in poly_edges:
            edges.append(mesh.getEdgeVertices(edge))

        adj = {}
        for edge in edges:
            adj.setdefault(edge[0], []).append(edge[1])
            adj.setdefault(edge[1], []).append(edge[0])

        # Проверяем, что все вершины имеют ровно 2 соседа
        for v, neighbors in adj.items():
            if len(neighbors) != 2:
                raise ValueError(f"Вершина {v} имеет {len(neighbors)} соседей — не цикл")

        start = edges[0][0]  # начинаем с первой вершины первого ребра
        loop = [start]
        current = start
        prev = None

        while True:
            # Находим следующего соседа (не того, откуда пришли)
            next_v = adj[current][0] if adj[current][0] != prev else adj[current][1]
            if next_v == start:  # Замкнули цикл
                break
            loop.append(next_v)
            prev, current = current, next_v

        if should_reverse_edges(lv2_node.vertices[loop[0]], lv2_node.vertices[loop[1]], lv2_node.vertices[loop[2]], lv2_polygon.normal):
            loop.reverse()

        for i in range(1, len(loop), 1):
            lv2_polygon.edges.append([loop[i - 1], loop[i]])
        lv2_polygon.edges.append([loop[-1], loop[0]])

        lv2_polygon.point_on_plane = [center.x, center.y, - center.z]
        lv2_node.addPolygon(lv2_polygon)
        poly_iter.next()


def fill_node_with_data(lv2_node, dg_node):
    fill_node_base_data(lv2_node, dg_node)

    nodes = {
        MP2_LEVEL_ITEM_NODE_NAME: fill_node_level_item,
        MP2_ENEMY_NODE_NAME: fill_node_enemy,
        MP2_TRIGGER_NODE_NAME: fill_node_trigger,
        MP2_FLARE_NODE_NAME: fill_node_flare,
        MP2_FSM_NODE_NAME: fill_node_fsm,
        MP2_DYNAMIC_POINT_LIGHT_NODE_NAME: fill_node_dynamic_point_light,
        MP2_VOLUME_LIGHTING_BOX_NODE_NAME: fill_node_volume_lighting_box
    }

    if dg_node['type'] in nodes:
        nodes[dg_node['type']](lv2_node, dg_node)

    if dg_node['type'] == 'mesh':
        fill_node_mesh(lv2_node, dg_node)
