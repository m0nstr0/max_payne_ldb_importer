from max_payne_sdk.ldb.vertex_type import Vertex, VertexUV
from max_payne_sdk.ldb2.character_type import CharacterEnemyGroup, Character
from max_payne_sdk.ldb2.collision_shape_type import CollisionShape, CollisionShapeMoppData
from max_payne_sdk.ldb2.dynamic_light_type import DynamicLight, DynamicLightColor
from max_payne_sdk.ldb2.dynamic_mesh_type import DynamicMesh, DynamicMeshAnimation
from max_payne_sdk.ldb2.flare_type import Flare
from max_payne_sdk.ldb2.fsm_type import FSM
from max_payne_sdk.ldb2.jump_point_type import JumpPoint
from max_payne_sdk.ldb2.level_item_type import LevelItem
from max_payne_sdk.ldb2.light_map_texture_type import LightMapTexture
from max_payne_sdk.ldb2.material_type import MaterialProperties, Material
from max_payne_sdk.ldb2.max_ldb2_type import MaxLDB2
from max_payne_sdk.ldb2.portal_type import Portal
from max_payne_sdk.ldb2.room_type import Room
from max_payne_sdk.ldb2.aabb_type import AABB
from max_payne_sdk.ldb2.static_mesh_type import StaticMesh, StaticMeshContainer
from max_payne_sdk.ldb2.texture_type import Texture
from max_payne_sdk.ldb2.volume_light_type import VolumeLight, VolumeLightAABB, VolumeLightRGB
from max_payne_sdk.ldb2.way_point_type import WayPoint
from max_payne_sdk.ldb_common.max_ldb_interface import MaxLDBInterface
from max_payne_sdk.ldb_common.max_ldb_reader_interface import MaxLDBReaderInterface
from max_payne_sdk.max_type import parseType
from max_payne_sdk.max_type import parseFloat
from max_payne_sdk.max_type import parseInt

class MaxLDBReader2(MaxLDBReaderInterface):
    def __init__(self, file_path: str):
        super().__init__(file_path)
        self.stringTable: bytes = None
        self.physicalWorldSize = 0.0
        self.ldb: MaxLDB2 = MaxLDB2()

    def parseStringTable(self, f) -> None:
        self.stringTable = f.read(parseType(f))

    def getStringFromStringTable(self, pos: int) -> str:
        return self.stringTable[pos:self.stringTable.find(b'\x00', pos)].decode()

    def getStringArrayFromStringTable(self, pos: int) -> str:
        return self.stringTable[pos:self.stringTable.find(b'\x00', pos)].decode()

    def parseTexture(self, group_id: int, f) -> Texture:
        file_type = parseType(f)
        size = parseType(f)
        file_path = self.getStringFromStringTable(parseType(f))
        data = f.read(size)
        return Texture(group_id, file_path, file_type, data)

    def parseLightMaps(self, f) -> None:
        is_dds = parseType(f)
        file_type = 0
        if is_dds == 1:
            file_type = 5
        for i in range(parseType(f)):
            size = parseType(f)
            data = f.read(size)
            self.ldb.getLightMaps().add(LightMapTexture(i, file_type, data))

    def parseTextures(self, f) -> None:
        # diffuse textures
        for _ in range(parseType(f)):
            self.ldb.getTextures().add(self.parseTexture(0, f))

        # lightmaps
        self.parseLightMaps(f)

        # detail textures
        # reflection textures
        # gloss textures
        for group_id in range(1, 4):
            for _ in range(parseType(f)):
                self.ldb.getTextures().add(self.parseTexture(group_id, f))

    def parseMaterials(self, f) -> None:
        # materials
        for i in range(parseType(f)):
            material = Material(i)
            blend_mode = parseType(f)
            frames = [self.ldb.getTextures().findTextureByGroupAndID(0, i) for i in range(parseType(f), parseType(f) + 1)]
            material.setLightmapTexture(self.ldb.getLightMaps().findLightMapById(parseType(f)))
            material.setDetailTexture(self.ldb.getTextures().findTextureByGroupAndID(1, parseType(f)))
            material.setReflectionTexture(self.ldb.getTextures().findTextureByGroupAndID(2, parseType(f)))
            material.setGlossTexture(self.ldb.getTextures().findTextureByGroupAndID(3, parseType(f)))
            material.setProperties(
                MaterialProperties(
                    parseType(f),
                    parseType(f),
                    parseType(f),
                    parseType(f),
                    parseType(f),
                    parseType(f),
                    parseType(f),
                    frames,
                    blend_mode
                )
            )
            material.setDiffuseTexture(frames[material.properties.visible_frame])
            self.ldb.getMaterials().add(material)

    def parseHeader(self, f) -> None:
        header = f.read(4)
        # if header !=
        if parseType(f) != 0x22:
            raise Exception("Unsupported file version")

    def parseRooms(self, f) -> None:
        for _ in range(parseType(f)):
            room_name = parseType(f)
            transform = parseType(f)
            parseType(f)
            self.ldb.getRooms().add(
                Room(room_name,
                     transform,
                     AABB(parseType(f), parseType(f), parseType(f)),
                     self.parseRoomStaticMesh(f),
                     self.parseRoomCollisions(f),
                     self.parseRoomVolumeLights(f)
                     )
            )

    def parseRoomStaticMesh(self, f) -> StaticMeshContainer:
        static_meshes: StaticMeshContainer = StaticMeshContainer()
        for _ in range(parseType(f)):
            material_id = parseType(f)
            has_lightmaps_uvs = parseType(f)
            has_detail_texture = parseType(f)
            polygons_count = parseType(f)
            vertices_count = parseType(f)
            vertices: list[Vertex] = [Vertex(parseFloat(f), parseFloat(f), parseFloat(f)) for _ in range(vertices_count)]
            normals: list[Vertex] = [Vertex(parseFloat(f), parseFloat(f), parseFloat(f)) for _ in range(vertices_count)]
            uvs: list[VertexUV] = [VertexUV(parseFloat(f), parseFloat(f)) for _ in range(vertices_count)]
            lightmap_uvs: list[VertexUV] = [VertexUV(parseFloat(f), parseFloat(f)) for _ in range(vertices_count)] if has_lightmaps_uvs == 1 else []
            detail_texture_uvs: list[VertexUV] = [VertexUV(parseFloat(f), parseFloat(f)) for _ in range(vertices_count)] if has_detail_texture == 1 else []
            indices: list[int] = [parseInt(f, 2, False) for _ in range(polygons_count * 3)]
            static_meshes.add(StaticMesh(vertices, normals, indices, material_id, uvs, lightmap_uvs, detail_texture_uvs))
        return static_meshes

    def parseRoomCollisions(self, f) -> list[CollisionShape]:
        collsion_shapes: list[CollisionShape] = []
        for _ in range(parseType(f)):
            collision_vetices_num = parseType(f)
            collision_polygons_num = parseType(f)
            vertices = [Vertex(parseFloat(f), parseFloat(f), parseFloat(f)) for _ in range(collision_vetices_num)]
            indices = [parseInt(f, 2, False) for _ in range(collision_polygons_num * 3)]
            material_indices = [parseInt(f, 1, False) for _ in range(collision_polygons_num)]
            is_convex = parseType(f)
            collision_mask = parseType(f)
            # havoc data
            origin_x = parseFloat(f)
            origin_y = parseFloat(f)
            origin_z = parseFloat(f)
            f.read(4)
            mopp_code = f.read(parseInt(f, 4, True))
            collsion_shapes.append(CollisionShape(vertices, indices, material_indices, is_convex, collision_mask, CollisionShapeMoppData(origin_x, origin_y, origin_z, mopp_code)))
        return collsion_shapes

    def parseRoomVolumeLights(self, f) -> list[VolumeLight]:
        volume_lights: list[VolumeLight] = []
        for _ in range(parseType(f)):
            grid_width = parseType(f)
            grid_height = parseType(f)
            grid_depth = parseType(f)
            min_point = parseType(f)
            max_point = parseType(f)
            colors: list[VolumeLightRGB] = []
            for _ in range(grid_width * grid_height * grid_depth):
                colors.append(VolumeLightRGB(parseFloat(f), parseFloat(f), parseFloat(f)))
            volume_lights.append(VolumeLight(grid_width, grid_width, grid_depth, VolumeLightAABB(min_point, max_point), colors))
        return volume_lights

    def parseDynamicLights(self, f):
        for _ in range(parseType(f)):
            self.ldb.getDynamicLights().add(
                DynamicLight(parseType(f), parseType(f), DynamicLightColor(parseType(f), parseType(f), parseType(f), parseType(f)), parseType(f))
            )

    def parseFlares(self, f):
        for _ in range(parseType(f)):
            self.ldb.getFlares().add(
                Flare(self.getStringFromStringTable(parseType(f)), parseType(f), parseType(f))
            )

    def parseLevelItems(self, f):
        for _ in range(parseType(f)):
            self.ldb.getLevelItems().add(
                LevelItem(self.getStringFromStringTable(parseType(f)), self.getStringFromStringTable(parseType(f)), parseType(f), parseType(f))
            )

    def parsePortals(self, f):
        for _ in range(parseType(f)):
            self.ldb.getPortals().add(
                Portal(parseType(f), parseType(f), parseType(f), parseType(f), [parseType(f) for _ in range(parseType(f))])
            )

    def parseJumpPoints(self, f):
        for _ in range(parseType(f)):
            self.ldb.getJumpPoints().add(
                JumpPoint(parseType(f), parseType(f), parseType(f))
            )

    def parseWayPoints(self, f):
        for _ in range(parseType(f)):
            self.ldb.getWayPoints().add(
                WayPoint(parseType(f), parseType(f), parseType(f), parseType(f))
            )

    def parseCharacters(self, f):
        f.read(1)
        for _ in range(parseType(f)):
            self.ldb.getCharacterEnemyGroups().add(CharacterEnemyGroup(parseType(f), parseType(f)))

        for _ in range(parseType(f)):
            self.ldb.getCharacters().add(Character(self.getStringFromStringTable(parseType(f)), self.getStringFromStringTable(parseType(f)), parseType(f), parseType(f), parseType(f), parseType(f)))

    def parseFSMs(self, f):
        for _ in range(parseType(f)):
            name = self.getStringFromStringTable(parseType(f))
            transform = parseType(f)
            parent_id = parseType(f)
            local_transform = parseType(f)
            room_id = parseType(f)

            self.ldb.getFSMS().add(FSM(name, transform, parent_id, local_transform, room_id))

            default_state = self.getStringFromStringTable(parseType(f))
            f.read(1)
            custom_states = [parseType(f) for _ in range(parseType(f))]
            #startup code
            startup_code_offset = parseType(f)
            custom_event_offset = parseType(f)
            custom_states_offset = parseType(f)
            entity_fsms_offset = parseType(f)
            #timers
            for _ in range(parseType(f)):
                timer_name = self.getStringFromStringTable(parseType(f))
                is_real_time = parseType(f)
                length = parseType(f)
                start_timer_fsm_offset = parseType(f)
                end_timer_fsm_offset = parseType(f)

    def parseTriggers(self, f):
        for _ in range(parseType(f)):
            fms_id = parseType(f)
            radius = parseType(f)
            ActivationPlayer = parseType(f)
            ActivationUse = parseType(f)
            ActivationEnemy = parseType(f)
            ActivationBullet = parseType(f)
            ActivationLookAt = parseType(f)
            ActivationVisibility = parseType(f)
            ActivatorsUseAnimation = parseType(f)
            HasCollisionShape = parseType(f)
            if HasCollisionShape == 1:
                parent = parseType(f)
                if parent == -1:
                    self.parseRoomCollisions(f)

    def paseAnimationGraph(self, f):
        pass

    def parseDynamicMeshAnimation(self, f) -> list[DynamicMeshAnimation]:
        animations: list[DynamicMeshAnimation] = []
        for _ in range(parseType(f)):
            anim_name = self.getStringFromStringTable(parseType(f))
            AnimationLength = parseType(f)
            StartTransform = parseType(f)
            EndTransform = parseType(f)
            # translation
            parseType(f)
            parseType(f)
            parseType(f)
            tsample_rate = parseType(f)
            tnum_points = parseType(f)
            ttime = [parseFloat(f) for _ in range(tnum_points)]
            tvalue = [parseFloat(f) for _ in range(tnum_points)]
            # rotation
            parseType(f)
            parseType(f)
            parseType(f)
            rsample_rate = parseType(f)
            rnum_points = parseType(f)
            rtime = [parseFloat(f) for _ in range(rnum_points)]
            rvalue = [parseFloat(f) for _ in range(rnum_points)]
            LeavingFirstFrameFSMStart = parseType(f)
            ReturningToFirstFrameFSMStart = parseType(f)
            ReachingSecondFrameFSMStart = parseType(f)
        return animations

    def parseDynamicMeshes(self, f):
        groups = []
        perfab_master = {}
        for _ in range(parseType(f)):
            fsm_id = parseType(f)
            use_light_maps = parseType(f)
            point_lights_affect = parseType(f)
            continuous_update = parseType(f)
            bullet_collision = parseType(f)
            character_collision = parseType(f)
            block_explosions = parseType(f)
            no_decals = parseType(f)
            elevator = parseType(f)
            physical_material = parseType(f)
            perfab_id = parseType(f)
            share_collision = parseType(f)
            aabb = AABB(parseType(f), parseType(f), parseType(f))
            mesh: StaticMeshContainer = None
            collision_shapes: list[CollisionShape] = []
            if perfab_id == -1:
                mesh = self.parseRoomStaticMesh(f)
                collision_shapes = self.parseRoomCollisions(f)
            if perfab_id >= 0:
                if perfab_id not in groups:
                    mesh = self.parseRoomStaticMesh(f)
                    collision_shapes = self.parseRoomCollisions(f)
                    groups.append(perfab_id)
                    perfab_master[perfab_id] = [mesh, collision_shapes, aabb]
                else:
                    if use_light_maps != 0:
                        mesh = self.parseRoomStaticMesh(f)
                        if share_collision == 0:
                            collision_shapes = self.parseRoomCollisions(f)
                        else:
                            collision_shapes = perfab_master[perfab_id][1]
                    else:
                        collision_shapes = perfab_master[perfab_id][1]
                        mesh = perfab_master[perfab_id][0]
                        aabb = perfab_master[perfab_id][2]

            self.ldb.getDynamicMeshes().add(DynamicMesh(
                fsm_id,
                use_light_maps,
                point_lights_affect,
                continuous_update,
                bullet_collision,
                character_collision,
                block_explosions,
                no_decals,
                elevator,
                physical_material,
                perfab_id,
                share_collision,
                aabb,
                mesh,
                collision_shapes,
                self.parseDynamicMeshAnimation(f)
            ))

    def parseMirrors(self, f):
        for _ in range(parseType(f)):
            PlaneNormal = parseType(f)
            PlanePoint = parseType(f)
            BoundingSphereRadius = parseType(f)
            BoundingBoxMin = parseType(f)
            BoundingBoxMax = parseType(f)
            unk = parseType(f)
            NumTriangles = parseType(f)
            for _ in range(NumTriangles):
                MaterialID = parseType(f)
                TriangleVertex1 = parseType(f)
                TriangleVertex2 = parseType(f)
                TriangleVertex3 = parseType(f)
                UVForVertex1 = parseType(f)
                UVForVertex2 = parseType(f)
                UVForVertex3 = parseType(f)
            RoomID = parseType(f)

    def parse(self) -> MaxLDBInterface:
        try:
            with open(self.file_path, "rb") as f:
                self.parseHeader(f)
                self.parseStringTable(f)
                self.physicalWorldSize = parseType(f)
                self.parseTextures(f)
                self.parseMaterials(f)
                self.parseRooms(f)
                self.parseDynamicLights(f)
                self.parseFlares(f)
                self.parseLevelItems(f)
                self.parsePortals(f)
                self.parseJumpPoints(f)
                self.parseWayPoints(f)
                self.parseCharacters(f)
                self.parseFSMs(f)
                self.parseTriggers(f)
                self.parseDynamicMeshes(f)
                self.parseMirrors(f)
        except IOError:
            print("Error While Opening the file! %s" % self.file_path)
        return self.ldb
