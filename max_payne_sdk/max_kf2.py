
import max_payne_sdk.max_kf2_type as kf2_type
import max_payne_sdk.max_type as max_type
import max_payne_sdk.max_kf2_reader.material_list as kf2_material_list
import max_payne_sdk.max_kf2_reader.keyframe_animation as kf2_keyframe_animation
import max_payne_sdk.max_kf2_reader.mesh as kf2_mesh
import max_payne_sdk.max_kf2_reader.camera as kf2_camera
import max_payne_sdk.max_kf2_reader.point_light as kf2_point_light
import max_payne_sdk.max_kf2_reader.directional_light as kf2_directional_light
import max_payne_sdk.max_kf2_reader.spot_light as kf2_spot_light
import max_payne_sdk.max_kf2_reader.point_light_animation as kf2_point_light_animation
import max_payne_sdk.max_kf2_reader.directional_light_animation as kf2_directional_light_animation
import max_payne_sdk.max_kf2_reader.spot_light_animation as kf2_spot_light_animation
import max_payne_sdk.max_kf2_reader.skin as kf2_skin
import max_payne_sdk.max_kf2_reader.environment as kf2_environment
import max_payne_sdk.max_kf2_reader.helper as kf2_helper

class MaxKF2:
    def __init__(self) -> None:
        self.material_list = []
        self.meshes = []
        self.cameras = []
        self.animations = []
        self.environments = []
        self.skins = []

    def hasMaterialList(self) -> bool:
        return True if len(self.material_list) > 0 else False
    
    def numMaterialList(self) -> int:
        return len(self.material_list)
    
    def getMaterialListVersion(self, idx: int) -> int:
        return self.material_list[idx].version

    def addMaterialList(self, material_list) -> None:
        self.material_list.append(material_list)

    def hasMeshes(self) -> bool:
        return True if len(self.meshes) > 0 else False
    
    def numMeshes(self) -> int:
        return len(self.meshes)
    
    def getMeshVersion(self, idx: int) -> int:
        return self.meshes[idx].version

    def addMesh(self, mesh) -> None:
        self.meshes.append(mesh)

    def hasCameras(self) -> bool:
        return True if len(self.cameras) > 0 else False

    def numCameras(self) -> int:
        return len(self.cameras)

    def getCameraVersion(self, idx: int) -> int:
        return self.cameras[idx].version

    def addCamera(self, camera) -> None:
        self.cameras.append(camera)

    def hasAnimations(self) -> bool:
        return True if len(self.animations) > 0 else False

    def numAnimations(self) -> int:
        return len(self.animations)

    def getAnimationVersion(self, idx: int) -> int:
        return self.animations[idx].version

    def addAnimation(self, animation) -> None:
        self.animations.append(animation)

    def hasEnvironments(self) -> bool:
        return True if len(self.environments) > 0 else False

    def numEnvironments(self) -> int:
        return len(self.environments)

    def getEnvironmentVersion(self, idx: int) -> int:
        return self.environments[idx].version

    def addEnvironment(self, environment) -> None:
        self.environments.append(environment)

    def hasSkins(self) -> bool:
        return True if len(self.skins) > 0 else False

    def numSkins(self) -> int:
        return len(self.skins)

    def getSkinVersion(self, idx: int) -> int:
        return self.skins[idx].version

    def addSkin(self, skin) -> None:
        self.skins.append(skin)

class MaxKF2Reader:
   def __parseChunk(self, kf2_chunk: kf2_type.KF2ChunkHeader, f) -> None:
        if kf2_chunk.id == kf2_type.CAMERA:
            self.kf2.addCamera(kf2_camera.CameraChunkReader().create(kf2_chunk).parse(f))
            return
        if kf2_chunk.id == kf2_type.POINT_LIGHT:
            return
        if kf2_chunk.id == kf2_type.DIRECTIONAL_LIGHT:
            return
        if kf2_chunk.id == kf2_type.SPOT_LIGHT:
            return
        if kf2_chunk.id == kf2_type.MESH:
            self.kf2.addMesh(kf2_mesh.MeshChunkReader().create().create(kf2_chunk).parse(f))
            return
        if kf2_chunk.id == kf2_type.MATERIAL_LIST:
            self.kf2.addMaterialList(kf2_material_list.MaterialListChunkReader().create(kf2_chunk).parse(f))
            return
        if kf2_chunk.id == kf2_type.KEYFRAME_ANIMATION:
            self.kf2.addAnimation(kf2_keyframe_animation.KeyframeAnimationChunkReader().create(kf2_chunk).parse(f))
            return
        if kf2_chunk.id == kf2_type.SKIN:
            self.kf2.addSkin(kf2_skin.SkinChunkReader().create(kf2_chunk).parse(f))
            return
        if kf2_chunk.id == kf2_type.ENVIRONMENT:
            self.kf2.addEnvironment(kf2_environment.EnvironmentChunkReader().create(kf2_chunk).parse(f))
            return
        if kf2_chunk.id == kf2_type.HELPER:
            return
        if kf2_chunk.id == kf2_type.POINT_LIGHT_ANIMATION:
            return
        if kf2_chunk.id == kf2_type.DIRECTIONAL_LIGHT_ANIMATION:
            return
        if kf2_chunk.id == kf2_type.SPOT_LIGHT_ANIMATION:
            return
        raise ValueError("Unknown chunk id %s" % kf2_chunk.id.hex())

   def parse(self, file_path) -> MaxKF2:
        self.kf2: MaxKF2 = MaxKF2()        
        try:
            with open(file_path, "rb") as f:
                chunk_tag = f.read(1)
                while chunk_tag != b"":
                    if chunk_tag != kf2_type.CHUNK_HEADER_ID:
                        raise ValueError("Unknown chunk tag id %s" % chunk_tag.hex())
                    kf2_chunk = kf2_type.KF2ChunkHeader(
                        int.from_bytes(f.read(4), 'little', False), 
                        int.from_bytes(f.read(4), 'little', False), 
                        int.from_bytes(f.read(4), 'little', False))
                    self.__parseChunk(kf2_chunk, f)
                    chunk_tag = f.read(1)
        except IOError:
            print("Error While Opening the file! %s" % file_path)
        return self.ldb