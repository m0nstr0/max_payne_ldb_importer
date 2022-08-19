import maya.cmds as mc
import maya.OpenMayaUI as omui
from PySide2 import QtCore, QtGui, QtWidgets
from shiboken2 import wrapInstance
import max_payne_sdk.max_kf2 as max_kf2
import maya.OpenMayaMPx as OpenMayaMPx
import maya.api.OpenMaya as OpenMaya
import maya.api.OpenMayaAnim as OpenMayaAnim
import math

class KF2ImportDialogUI(QtWidgets.QDialog):
    def __init__(self):
        maya_window_ptr = omui.MQtUtil.mainWindow()
        parent = wrapInstance(int(maya_window_ptr), QtWidgets.QWidget)
        super(KF2ImportDialogUI, self).__init__(parent)
        self.setWindowTitle("Max Payne KF2 Importer")
        self.resize(600, 500)
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.setContentsMargins(10, 10, 10, 10)
        self.mainLayout.setSpacing(10)
        self.setLayout(self.mainLayout)
        self.createSkeletonOpts()
        self.createImportOpts()
        self.createMaterialOpts()
        self.createDialogBtns()
        self.configureUI()
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.setModal(True)

    def onIsSkeletonCheckBoxChanged(self, state):
        if state == QtCore.Qt.Checked:
            self.importOptsGroupBox.setDisabled(True)
            self.materialOptsGroupBox.setDisabled(True)
        else:
            self.importOptsGroupBox.setDisabled(False)
            self.materialOptsGroupBox.setDisabled(False)

    def createSkeletonOpts(self):
        self.isSkeletonCheckBox = QtWidgets.QCheckBox("This is a skeleton file", self)
        self.isSkeletonCheckBox.stateChanged.connect(self.onIsSkeletonCheckBoxChanged)

        skeletonOptsVBoxLayout = QtWidgets.QVBoxLayout()
        skeletonOptsVBoxLayout.addWidget(self.isSkeletonCheckBox)
        skeletonOptsGroupBox = QtWidgets.QGroupBox("Is this a skeleton file?")
        skeletonOptsGroupBox.setLayout(skeletonOptsVBoxLayout)
        self.mainLayout.addWidget(skeletonOptsGroupBox)

    def createImportOpts(self):
        self.cameraCheckBox = QtWidgets.QCheckBox("Camera", self)
        self.pointLightCheckBox = QtWidgets.QCheckBox("Point Light", self)
        self.directionalLightCheckBox = QtWidgets.QCheckBox("Directional Light", self)
        self.spotLightCheckBox = QtWidgets.QCheckBox("Spot Light", self)
        self.meshCheckBox = QtWidgets.QCheckBox("Mesh", self)
        self.materialCheckBox = QtWidgets.QCheckBox("Material List", self)
        self.amimationCheckBox = QtWidgets.QCheckBox("Keyframe Animation", self)
        self.skinCheckBox = QtWidgets.QCheckBox("Skin", self)
        self.environmentCheckBox = QtWidgets.QCheckBox("Environment", self)
        self.helperCheckBox = QtWidgets.QCheckBox("Helper", self)
        self.pointLightAnimationCheckBox = QtWidgets.QCheckBox("Point Light Animation", self)
        self.directionalLightAnimationCheckBox = QtWidgets.QCheckBox("Directional Light Animation", self)
        self.spotLightAnimationCheckBox = QtWidgets.QCheckBox("Spot Light Animation", self)

        importOptsVBoxLayout = QtWidgets.QVBoxLayout()
        importOptsVBoxLayout.addWidget(self.cameraCheckBox)
        importOptsVBoxLayout.addWidget(self.pointLightCheckBox)
        importOptsVBoxLayout.addWidget(self.directionalLightCheckBox)
        importOptsVBoxLayout.addWidget(self.spotLightCheckBox)
        importOptsVBoxLayout.addWidget(self.meshCheckBox)
        importOptsVBoxLayout.addWidget(self.materialCheckBox)
        importOptsVBoxLayout.addWidget(self.amimationCheckBox)
        importOptsVBoxLayout.addWidget(self.skinCheckBox)
        importOptsVBoxLayout.addWidget(self.environmentCheckBox)
        importOptsVBoxLayout.addWidget(self.helperCheckBox)
        importOptsVBoxLayout.addWidget(self.pointLightAnimationCheckBox)
        importOptsVBoxLayout.addWidget(self.directionalLightAnimationCheckBox)
        importOptsVBoxLayout.addWidget(self.spotLightAnimationCheckBox)
        importOptsVBoxLayout.addStretch(1)
        self.importOptsGroupBox = QtWidgets.QGroupBox("Select components to import:")
        self.importOptsGroupBox.setLayout(importOptsVBoxLayout)
        self.mainLayout.addWidget(self.importOptsGroupBox)

    def onChooseTextureDirectoy(self):
        self.textureDirectory.insert(QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Directory'))

    def createMaterialOpts(self):
        self.textureDirectory = QtWidgets.QLineEdit()
        self.textureDirectory.setReadOnly(True)
        self.textureDirectory.setPlaceholderText("Select a directory with textures for the materials")

        openDirectoryBtn = QtWidgets.QPushButton("...")
        openDirectoryBtn.released.connect(self.onChooseTextureDirectoy)

        materialOptsHBox = QtWidgets.QHBoxLayout()
        materialOptsHBox.addWidget(self.textureDirectory)
        materialOptsHBox.addWidget(openDirectoryBtn)
        self.materialOptsGroupBox = QtWidgets.QGroupBox("Materials Import Settings:")
        self.materialOptsGroupBox.setLayout(materialOptsHBox)
        self.mainLayout.addWidget(self.materialOptsGroupBox)
        
    def onStartImport(self):
        self.reject()

    def onCancelImport(self):
        self.reject()

    def createDialogBtns(self):
        importButton = QtWidgets.QPushButton("Import")
        importButton.released.connect(self.onStartImport)
        cancelButton = QtWidgets.QPushButton("Cancel")
        cancelButton.released.connect(self.onCancelImport)

        DialogBtnsHBox = QtWidgets.QHBoxLayout()
        DialogBtnsHBox.addWidget(importButton)
        DialogBtnsHBox.addWidget(cancelButton)
        self.mainLayout.addLayout(DialogBtnsHBox)

    def configureUI(self):
        pass

class KF2ImportDialog(KF2ImportDialogUI):
    def __init__(self, kf2: max_kf2.MaxKF2):
        self.kf2 = kf2
        super().__init__()

    def importSkeleton(self):
        joints = []
        nodes = {}
        for mesh in self.kf2.getMeshes():
            matrix4x4 = OpenMaya.MMatrix([
                mesh.node.object_to_parent_transform[0] + [0.0],
                mesh.node.object_to_parent_transform[1] + [0.0],
                mesh.node.object_to_parent_transform[2] + [0.0],
                [mesh.node.object_to_parent_transform[3][0] * 100.0, mesh.node.object_to_parent_transform[3][1] * 100.0, mesh.node.object_to_parent_transform[3][2] * 100.0] + [1.0]
            ])
            if not mesh.node.has_parent:
                nodes[mesh.node.name] = matrix4x4
            else:
                nodes[mesh.node.name] = matrix4x4 * nodes[mesh.node.parent_name]

        for mesh in self.kf2.getMeshes():
            mc.select(clear = True)
            joint = None
            transform = OpenMaya.MTransformationMatrix(nodes[mesh.node.name])
            tr = transform.translation(OpenMaya.MSpace.kTransform)
            ro = transform.rotation(asQuaternion=False)
            if mesh.node.has_parent:
                for i in joints:
                    if mc.getAttr(i + '.mp_node_name', asString = True) == mesh.node.parent_name:
                        joint = mc.joint(i, n = mesh.node.name, position = (-tr[0], tr[1], tr[2]), ax = ro[0] * (180/math.pi), ay = - ro[1] * (180/math.pi), az = -ro[2] * (180/math.pi))
                        break
            else:
                joint = mc.joint(n = mesh.node.name, position = (-tr[0], tr[1], tr[2]), ax = ro[0] * (180/math.pi), ay = -ro[1] * (180/math.pi), az = -ro[2] * (180/math.pi))
            mc.addAttr(joint, longName = 'mp_node_name', storable = True, dataType = 'string')
            mc.setAttr(joint + '.mp_node_name', mesh.node.name, type="string")
            joints.append(joint)
        self.accept()

    def importMaterial(self):
        pass

    def importMesh(self):
        nodes = {}
        for mesh in self.kf2.getMeshes():
            matrix4x4 = OpenMaya.MMatrix([
                mesh.node.object_to_parent_transform[0] + [0.0],
                mesh.node.object_to_parent_transform[1] + [0.0],
                mesh.node.object_to_parent_transform[2] + [0.0],
                [mesh.node.object_to_parent_transform[3][0] * 100.0, mesh.node.object_to_parent_transform[3][1] * 100.0, mesh.node.object_to_parent_transform[3][2] * 100.0] + [1.0]
            ])
            if not mesh.node.has_parent:
                nodes[mesh.node.name] = matrix4x4
            else:
                nodes[mesh.node.name] = matrix4x4 * nodes[mesh.node.parent_name]

        meshes = {}
        for mesh in self.kf2.getMeshes():
            mc.select(clear = True)
            transform = OpenMaya.MTransformationMatrix(nodes[mesh.node.name])
            tr = transform.translation(OpenMaya.MSpace.kTransform)
            ro = transform.rotation(asQuaternion = False)
            s = transform.scale(OpenMaya.MSpace.kWorld)
            #vertices
            vertex_buffers = []
            start_vertex = 0
            for num_vertices in mesh.geometry.vertices_per_primitive:
                vertex_buffers.append([OpenMaya.MFloatPoint(-x[0] * 100.0, x[1] * 100.0, x[2] * 100.0) for x in mesh.geometry.vertices[start_vertex:start_vertex + num_vertices]])
                start_vertex = start_vertex + num_vertices
            #indices
            start_index = 0
            index_buffers = []
            num_points = []
            for num_indices in mesh.polygons.polygons_per_primitive:
                index_buffers.append(mesh.polygons.polygons_indices[start_index:start_index + num_indices * 3])
                num_points.append([3 for x in range(num_indices)])
                start_index = start_index + num_indices * 3
            #uvs
            start_uv = 0
            us_buffer = []
            vs_buffer = []
            if len(mesh.uv_mapping) > 0:
                for uv in mesh.uv_mapping:
                    for num_uvs in uv.coordinates_per_primitive:
                        us_buffer.append([(x[0]) for x in uv.coordinates[start_uv:start_uv + num_uvs]])
                        vs_buffer.append([(1.0 - x[1]) for x in uv.coordinates[start_uv:start_uv + num_uvs]])
                        start_uv = start_uv + num_uvs
                    break
            #generate mesh
            selection = OpenMaya.MSelectionList()
            for primitive_id in range(len(mesh.polygons.polygons_per_primitive)):
                new_mesh = OpenMaya.MFnMesh()
                us = us_buffer[primitive_id] if len(mesh.uv_mapping) > 0 else []
                vs = vs_buffer[primitive_id] if len(mesh.uv_mapping) > 0 else []
                new_mesh.create(vertex_buffers[primitive_id], num_points[primitive_id], index_buffers[primitive_id], us, vs)
                if len(mesh.uv_mapping) > 0:
                    for face_id in range(int(len(index_buffers[primitive_id]) / 3)):
                        new_mesh.assignUV(face_id, 0, index_buffers[primitive_id][face_id * 3 + 0])
                        new_mesh.assignUV(face_id, 1, index_buffers[primitive_id][face_id * 3 + 1])
                        new_mesh.assignUV(face_id, 2, index_buffers[primitive_id][face_id * 3 + 2])
                new_mesh.updateSurface()
                selection.add(new_mesh.getPath())
            #transform
            OpenMaya.MGlobal.setActiveSelectionList(selection)
            if selection.length() > 1:
                transform_node = mc.polyUnite(constructionHistory = False)[0]
            else:
                transform_node = OpenMaya.MFnTransform(OpenMaya.MFnDagNode(OpenMaya.MGlobal.getActiveSelectionList().getDagPath(0)).parent(0)).name()
            mc.addAttr(transform_node, longName = 'mp_node_name', storable = True, dataType = 'string')
            mc.setAttr(transform_node + '.mp_node_name', mesh.node.name, type = "string")
            mesh_node_name = mc.rename(transform_node, mesh.node.name)
            meshes[mesh.node.name] = mesh_node_name
            mc.move(-tr[0], tr[1], tr[2], mesh_node_name, absolute=True)
            mc.rotate(ro[0] * (180 / math.pi), -ro[1] * (180 / math.pi), -ro[2] * (180 / math.pi), mesh_node_name, absolute=True)
            mc.scale(s[0], s[1], s[2], mesh_node_name, absolute=True)
            if mesh.node.has_parent:
                mc.parent(mesh_node_name, meshes[mesh.node.parent_name])

        #, absolute = True
        #new_mesh.assignUVs(poly_num_points, poly_uv_indices)
        #for poly_id, normal_vertex in normals_per_poly.items():
        #    for element in normal_vertex:
        #       new_mesh.setFaceVertexNormal(element[1], poly_id, element[0])
        #mc.hyperShade(assign = self.materials.getMaterialNameById(material_id))
    def importCamera(self):
        pass

    def importAnimation(self):
        pass

    def importSkin(self):
        mp_node_names = mc.ls("*.mp_node_name", o=True)
        for skin in self.kf2.getSkins():
            skeleton_object_names_dict = {}
            skeleton_object_names = []
            for i in range(len(skin.skeleton_object_names)):
                for mp_node_name in mp_node_names:
                    if skin.skeleton_object_names[i].lower() == mc.getAttr(mp_node_name + ".mp_node_name").lower():
                        skeleton_object_names_dict[mp_node_name.lower()] = i
                        skeleton_object_names.append(mp_node_name)
                        break
            skin_object_name = ""
            for mp_node_name in mp_node_names:
                if skin.skin_object_names[0].lower() == mc.getAttr(mp_node_name + ".mp_node_name").lower():
                    skin_object_name = mp_node_name
                    break
            #raise ValueError(skeleton_object_names_dict)
            mc.select(skeleton_object_names)
            mc.select(skin_object_name, add=True)
            skin_cluster_name = mc.skinCluster()
            skin_object_dag = OpenMaya.MGlobal.getSelectionListByName(skin_object_name).getDagPath(0)
            skin_fn = OpenMayaAnim.MFnSkinCluster(OpenMaya.MGlobal.getSelectionListByName(skin_cluster_name[0]).getDependNode(0))
            skin_id_to_cluster_id = {}
            for bone_dag in skin_fn.influenceObjects():
                skin_id_to_cluster_id[skeleton_object_names_dict[bone_dag.partialPathName().lower()]] = skin_fn.indexForInfluenceObject(bone_dag)

            influences = []
            weights = []
            for skin_vertex in skin.skin_vertices:
                bones_set = {*skin_vertex.vertex_bone_indices}
                influences.append(OpenMaya.MIntArray())
                weights.append(OpenMaya.MDoubleArray([0.0 for i in range(len(skin_id_to_cluster_id.values()))]))
                for bone_index in skin_vertex.vertex_bone_indices:
                    influences[skin_vertex.vertex_index].append(skin_id_to_cluster_id[bone_index])
                for i in range(len(skin_vertex.vertex_weights)):
                    weights[skin_vertex.vertex_index][i] = skin_vertex.vertex_weights[i]
                for i in skin_id_to_cluster_id.values():
                    if i not in bones_set:
                        influences[skin_vertex.vertex_index].append(i)

            for component in OpenMaya.MItGeometry(skin_object_dag):
                skin_fn.setWeights(skin_object_dag, component.currentItem(), influences[component.index()], weights[component.index()], normalize = False, returnOldWeights = False)

    def onStartImport(self):
        if self.isSkeletonCheckBox.checkState() == QtCore.Qt.Checked:
            self.importSkeleton()
            return
        if self.materialCheckBox.checkState() == QtCore.Qt.Checked:
            self.importMaterial()
        if self.meshCheckBox.checkState() == QtCore.Qt.Checked:
            self.importMesh()
        if self.cameraCheckBox.checkState() == QtCore.Qt.Checked:
            self.importCamera()
        if self.skinCheckBox.checkState() == QtCore.Qt.Checked:
            self.importSkin()
        if self.amimationCheckBox.checkState() == QtCore.Qt.Checked:
            self.importAnimation()
        self.accept()

    def configureUI(self):
        if not self.kf2.hasCameras():
            self.cameraCheckBox.setDisabled(True)
        if not self.kf2.hasMeshes():
            self.meshCheckBox.setDisabled(True)
        if not self.kf2.hasMaterialList():
            self.materialCheckBox.setDisabled(True)
        if not self.kf2.hasKeyframeAnimations():
            self.amimationCheckBox.setDisabled(True)
        if not self.kf2.hasSkins():
            self.skinCheckBox.setDisabled(True)



        if not self.kf2.hasCameras():
            self.pointLightCheckBox.setDisabled(True)
        if not self.kf2.hasCameras():
            self.directionalLightCheckBox.setDisabled(True)
        if not self.kf2.hasCameras():
            self.spotLightCheckBox.setDisabled(True)

        if not self.kf2.hasEnvironments():
            self.environmentCheckBox.setDisabled(True)
        if not self.kf2.hasCameras():
            self.helperCheckBox.setDisabled(True)
        if not self.kf2.hasCameras():
            self.pointLightAnimationCheckBox.setDisabled(True)
        if not self.kf2.hasCameras():
            self.directionalLightAnimationCheckBox.setDisabled(True)
        if not self.kf2.hasCameras():
            self.spotLightAnimationCheckBox.setDisabled(True)