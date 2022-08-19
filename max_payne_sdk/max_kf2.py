
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
   def __parseChunk(self, kf2_chunk: kf2_type.KF2ChunkHeader, f) -> None:
        if kf2_chunk.id == kf2_type.CAMERA:
            self.kf2.addCamera(kf2_camera.CameraChunkReader().create(f, kf2_type.CAMERA, kf2_chunk))
            return
        if kf2_chunk.id == kf2_type.POINT_LIGHT:
            return
        if kf2_chunk.id == kf2_type.DIRECTIONAL_LIGHT:
            return
        if kf2_chunk.id == kf2_type.SPOT_LIGHT:
            return
        if kf2_chunk.id == kf2_type.MESH:
            self.kf2.addMesh(kf2_mesh.MeshChunkReader().create(f, kf2_type.MESH, kf2_chunk))
            return
        if kf2_chunk.id == kf2_type.MATERIAL_LIST:
            self.kf2.addMaterialList(kf2_material_list.MaterialListChunkReader().create(f, kf2_type.MATERIAL_LIST, kf2_chunk))
            return
        if kf2_chunk.id == kf2_type.KEYFRAME_ANIMATION:
            self.kf2.addKeyframeAnimation(kf2_keyframe_animation.KeyframeAnimationChunkReader().create(f, kf2_type.KEYFRAME_ANIMATION, kf2_chunk))
            return
        if kf2_chunk.id == kf2_type.SKIN:
            self.kf2.addSkin(kf2_skin.SkinChunkReader().create(f, kf2_type.SKIN, kf2_chunk))
            return
        if kf2_chunk.id == kf2_type.ENVIRONMENT:
            #self.kf2.addEnvironment(kf2_environment.EnvironmentChunkReader().create(kf2_chunk).parse(f))
            return
        if kf2_chunk.id == kf2_type.HELPER:
            return
        if kf2_chunk.id == kf2_type.POINT_LIGHT_ANIMATION:
            return
        if kf2_chunk.id == kf2_type.DIRECTIONAL_LIGHT_ANIMATION:
            return
        if kf2_chunk.id == kf2_type.SPOT_LIGHT_ANIMATION:
            return
        raise ValueError("Unknown chunk id %s" % hex(kf2_chunk.id))

   def parse(self, file_path) -> MaxKF2:
        self.kf2: MaxKF2 = MaxKF2()        
        try:
            with open(file_path, "rb") as f:
                chunk_tag = f.read(1)
                while chunk_tag != b"":
                    if chunk_tag != kf2_type.CHUNK_HEADER_ID:
                        raise ValueError("Unknown chunk tag id %s" % chunk_tag.hex())
                    kf2_chunk = kf2_type.KF2ChunkHeader(
                        int.from_bytes(f.read(4), byteorder='little', signed=False),
                        int.from_bytes(f.read(4), byteorder='little', signed=False),
                        int.from_bytes(f.read(4), byteorder='little', signed=False))
                    self.__parseChunk(kf2_chunk, f)
                    chunk_tag = f.read(1)
        except IOError:
            print("Error While Opening the file! %s" % file_path)
        return self.kf2