
import max_payne_sdk.max_kf2_type as kf2_type
import max_payne_sdk.max_kf2_reader.material_reader.material_list as kf2_material_list
import max_payne_sdk.max_kf2_reader.camera_reader.camera as kf2_camera
import max_payne_sdk.max_kf2_reader.animation_reader.keyframe_animation as kf2_keyframe_animation
import max_payne_sdk.max_kf2_reader.mesh_reader.mesh as kf2_mesh
import max_payne_sdk.max_kf2_reader.skin_reader.skin as kf2_skin

class MaxKF2:
    def __init__(self) -> None:
        self.material_list = []
        self.meshes = []
        self.cameras = []
        self.keyframe_animations = []
        self.environments = []
        self.skins = []
        self.unknown_chunks = []

    def hasMaterialList(self) -> bool:
        return True if len(self.material_list) > 0 else False
    
    def numMaterialList(self) -> int:
        return len(self.material_list)

    def addMaterialList(self, material_list) -> None:
        self.material_list.append(material_list)

    def getMaterialList(self):
        return self.material_list

    def hasCameras(self) -> bool:
        return True if len(self.cameras) > 0 else False

    def numCameras(self) -> int:
        return len(self.cameras)

    def addCamera(self, camera) -> None:
        self.cameras.append(camera)

    def getCameras(self):
        return self.cameras

    def hasKeyframeAnimations(self) -> bool:
        return True if len(self.keyframe_animations) > 0 else False

    def numKeyframeAnimations(self) -> int:
        return len(self.keyframe_animations)

    def getKeyframeAnimations(self):
        return self.keyframe_animations

    def addKeyframeAnimation(self, animation) -> None:
        self.keyframe_animations.append(animation)

    def hasMeshes(self) -> bool:
        return True if len(self.meshes) > 0 else False
    
    def numMeshes(self) -> int:
        return len(self.meshes)
    
    def addMesh(self, mesh) -> None:
        self.meshes.append(mesh)

    def getMeshes(self):
        return self.meshes

    def hasSkins(self) -> bool:
        return True if len(self.skins) > 0 else False

    def numSkins(self) -> int:
        return len(self.skins)

    def addSkin(self, skin) -> None:
        self.skins.append(skin)

    def getSkins(self):
        return self.skins





    def hasEnvironments(self) -> bool:
        return True if len(self.environments) > 0 else False

    def numEnvironments(self) -> int:
        return len(self.environments)

    def getEnvironmentVersion(self, idx: int) -> int:
        return self.environments[idx].version

    def addEnvironment(self, environment) -> None:
        self.environments.append(environment)



class MaxKF2Reader:
    # KF2/KFS/SKD share the chunk envelope; extensions do not select a codec.
    _READERS = {
        kf2_type.CAMERA: (kf2_camera.CameraChunkReader, "addCamera"),
        kf2_type.MESH: (kf2_mesh.MeshChunkReader, "addMesh"),
        kf2_type.MATERIAL_LIST: (kf2_material_list.MaterialListChunkReader, "addMaterialList"),
        kf2_type.KEYFRAME_ANIMATION: (kf2_keyframe_animation.KeyframeAnimationChunkReader, "addKeyframeAnimation"),
        kf2_type.SKIN: (kf2_skin.SkinChunkReader, "addSkin"),
    }

    def parse(self, file_path) -> MaxKF2:
        from max_payne_sdk.max_kf2_reader import KF2ReaderBase
        from max_payne_sdk.binary import read_exact, FormatError

        self.kf2 = MaxKF2()
        envelope = KF2ReaderBase()
        with open(file_path, "rb") as stream:
            while True:
                header = envelope.readChunk(stream)
                if header is None:
                    break
                entry = self._READERS.get(header.id)
                if entry is None:
                    self.kf2.unknown_chunks.append((header, read_exact(stream, header.size - 13)))
                    continue
                reader_class, add_method = entry
                reader = reader_class()
                if header.version not in reader.getAllowedVersions():
                    raise FormatError("Unsupported chunk 0x%x version %d" % (header.id, header.version))
                getattr(self.kf2, add_method)(reader.create(stream, header.id, header))
        if not self.kf2.unknown_chunks and not any((self.kf2.material_list, self.kf2.meshes,
                self.kf2.cameras, self.kf2.keyframe_animations, self.kf2.skins)):
            raise FormatError("Empty KF2/KFS/SKD document")
        return self.kf2
