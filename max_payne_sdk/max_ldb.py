from __future__ import annotations
from max_payne_sdk.max_type import parseType
from max_payne_sdk.max_ldb_type import Vertex
from max_payne_sdk.max_ldb_type import VertexContainer
from max_payne_sdk.max_ldb_type import BSPVertex
from max_payne_sdk.max_ldb_type import BSPPolygon
from max_payne_sdk.max_ldb_type import BSPNode
from max_payne_sdk.max_ldb_type import BSPPolygonIndex
from max_payne_sdk.max_ldb_type import Texture
from max_payne_sdk.max_ldb_type import LightMapTexture
from max_payne_sdk.max_ldb_type import Material
from max_payne_sdk.max_ldb_type import Exit
from max_payne_sdk.max_ldb_type import VertexUV
from max_payne_sdk.max_ldb_type import TextureVertex
from max_payne_sdk.max_ldb_type import Polygon
from max_payne_sdk.max_ldb_type import PolygonContainer
from max_payne_sdk.max_ldb_type import StaticMesh
from max_payne_sdk.max_ldb_type import EntityProperties
from max_payne_sdk.max_ldb_type import DynamicLight
from max_payne_sdk.max_ldb_type import Waypoint
from max_payne_sdk.max_ldb_type import FSMMessageContainer
from max_payne_sdk.max_ldb_type import FSMStateSpecificMessage
from max_payne_sdk.max_ldb_type import FSMStateSpecificMessageContainer
from max_payne_sdk.max_ldb_type import FSMEvent
from max_payne_sdk.max_ldb_type import FSMEventContainer
from max_payne_sdk.max_ldb_type import FSMStateContainer
from max_payne_sdk.max_ldb_type import FSM
from max_payne_sdk.max_ldb_type import Character
from max_payne_sdk.max_ldb_type import Trigger
from max_payne_sdk.max_ldb_type import Graph
from max_payne_sdk.max_ldb_type import Animation
from max_payne_sdk.max_ldb_type import AnimationContainer
from max_payne_sdk.max_ldb_type import DynamicMeshConfig
from max_payne_sdk.max_ldb_type import DynamicMesh
from max_payne_sdk.max_ldb_type import Item
from max_payne_sdk.max_ldb_type import PointLight
from max_payne_sdk.max_ldb_type import Room
from max_payne_sdk.max_ldb_type import MaxLDB


class MaxLDBReaderInterface:
    def __init__(self, file_path: str):
        self.file_path = file_path
        pass

    def parse(self) -> MaxLDB:
        pass


class MaxLDBReader2(MaxLDBReaderInterface):
    def __init__(self, file_path: str):
        super().__init__(file_path)
        self.stringTable = ""
        self.physicalWorldSize = 0.0

    def parseStringTable(self, f) -> None:
        data = f.read(parseType(f))
        self.stringTable = data.decode()

    def parseMaterials(self, f) -> None:
        #diffuse textures
        for i in range(parseType(f)):
            texture_type_id = parseType(f)
            TextureSizeInBytes = parseType(f)
            StringPositionInStringTable = parseType(f)
            data = f.read(TextureSizeInBytes)

        #lightmaps
        LightMapIsDDS = parseType(f)
        for i in range(parseType(f)):
            data = f.read(parseType(f))

        #DetailTexturesNum
        for i in range(parseType(f)):
            texture_type_id = parseType(f)
            TextureSizeInBytes = parseType(f)
            StringPositionInStringTable = parseType(f)
            data = f.read(TextureSizeInBytes)

        #ReflectionTexturesNum
        for i in range(parseType(f)):
            texture_type_id = parseType(f)
            TextureSizeInBytes = parseType(f)
            StringPositionInStringTable = parseType(f)
            data = f.read(TextureSizeInBytes)

        #GlossTexturesNum
        for i in range(parseType(f)):
            texture_type_id = parseType(f)
            TextureSizeInBytes = parseType(f)
            StringPositionInStringTable = parseType(f)
            data = f.read(TextureSizeInBytes)

        #materials
        for i in range(parseType(f)):
            # Normal - 0, AlphaBlend - 4, AlphaCompare - 1, AlphaCompareEdgeBlend - 2, Additive - 3, WithDetailTexure - 5, WithReflectionTexture - 6, WithGlossTexture - 9, AlphaCompareReflectionGloss - 10, AlphaCompareEdgeBlendReflectionGloss - 11 AlphaCompareEdgeBlendReflection - 8 AlphaCompareReflection - 7
            BlendMode = parseType(f)
            StartTextureID = parseType(f)
            EndTextureID = parseType(f)
            LightMapTextureID = parseType(f)
            DetailTextureID = parseType(f)
            ReflectionTextureID = parseType(f)
            GlossTextureID = parseType(f)
            AlphaCompareReferenceValue = parseType(f)
            # For Z-fighting (for instance: graffity textures)
            SortPriority = parseType(f)
            # For Z-fighting (for instance: graffity textures)
            DetailOffset = parseType(f)
            DualSided = parseType(f)
            # For Z-fighting (for instance: graffity textures)
            WritesZBuffer = parseType(f)
            Framerate = parseType(f)
            VisibleFrame = parseType(f)
    def parse(self) -> MaxLDB:
        try:
            with open(self.file_path, "rb") as f:
                f.read(4)
                if parseType(f) != 0x22:
                    raise Exception("Unsupported file version")
                self.parseStringTable(f)
                self.physicalWorldSize = parseType(f)
                self.parseMaterials(f)
        except IOError:
            print("Error While Opening the file! %s" % self.file_path)
        return MaxLDB()

class MaxLDBReader(MaxLDBReaderInterface):
    # collision things
    def parseBSP(self, f) -> None:
        # Block header
        f.read(1)
        for i in range(parseType(f)):
            self.ldb.getBsp().getVertices().add(BSPVertex(*parseType(f)))
        # Block header
        f.read(1)
        for i in range(parseType(f)):
            self.ldb.getBsp().getPolygons().add(
                BSPPolygon(*[
                    parseType(f),
                    parseType(f),
                    parseType(f),
                    parseType(f),
                    Vertex(*parseType(f)),
                    Vertex(*parseType(f))
                ]))
        # Block header
        f.read(1)
        for i in range(parseType(f)):
            self.ldb.getBsp().getNodes().add(
                BSPNode(*[
                    Vertex(*parseType(f)),
                    Vertex(*parseType(f)),
                    parseType(f),
                    parseType(f),
                    parseType(f),
                    parseType(f),
                    parseType(f),
                    parseType(f)
                ]))
        # Block header
        f.read(1)
        for i in range(parseType(f)):
            self.ldb.getBsp().getIndices().add(BSPPolygonIndex(parseType(f)))

    # textures, lightmaps, material_reader properties etc
    def parseMaterials(self, f) -> None:
        # Textures
        # Block header
        parseType(f)
        for i in range(parseType(f)):
            self.ldb.getTextures().add(
                Texture(*[
                    parseType(f),
                    parseType(f),
                    f.read(parseType(f))
                ]))

        # Block header
        f.read(1)
        # in the order how they are applied to the polygons
        for i in range(parseType(f)):
            material_id = parseType(f)
            f.read(1)
            self.ldb.getMaterials().add(Material(i, material_id, parseType(f), parseType(f)))

        # Block header
        f.read(1)
        # in the order how they were in MAX-ED
        for i in range(parseType(f)):
            f.read(1)
            category_name = parseType(f)
            material_name = parseType(f)
            material_id = parseType(f)

        # material_reader properties, materials properties also contain materials that haven't been used in the level, skip them
        for i in range(parseType(f)):
            category_name = parseType(f)
            for j in range(parseType(f)):
                material = self.ldb.getMaterials().findMaterialByCategoryAndName(category_name, parseType(f))
                # skip unused materials
                if material == None:
                    parseType(f)
                    parseType(f)
                    parseType(f)
                    parseType(f)
                    continue
                material.setDiffuseTexture(self.ldb.getTextures().findTextureByFileName(parseType(f)))
                material.setAlphaTexture(self.ldb.getTextures().findTextureByFileName(parseType(f)))
                material.setProperties(parseType(f), parseType(f))

        # lightmaps
        for i in range(parseType(f)):
            self.ldb.getLightMaps().add(
                LightMapTexture(*[
                    parseType(f),
                    parseType(f),
                    f.read(parseType(f))
                ]))

    # portals aka exits hierarchy
    def parseExits(self, f) -> None:
        for i in range(parseType(f)):
            exit_name = parseType(f)
            # vertices
            vertices = VertexContainer()
            for j in range(parseType(f)):
                vertices.add(Vertex(*parseType(f)))
            normal = parseType(f)
            transform = parseType(f)
            room_id = parseType(f)
            parent_room_id = parseType(f)
            parent_room_name = parseType(f)
            # some bsp info idk how to work with it
            f.read(1)
            for j in range(parseType(f)):
                f.read(1)
                for k in range(parseType(f)):
                    parseType(f)
            self.ldb.getExits().add(
                Exit(exit_name, vertices, normal, transform, room_id, parent_room_id, parent_room_name))

    # static meshes each static mesh is like one room
    def parseStaticMeshes(self, f) -> None:
        # uv attributes
        f.read(1)
        for i in range(parseType(f)):
            self.ldb.getStaticMeshes().getTextureVertices().add(
                TextureVertex(*[
                    parseType(f),
                    VertexUV(*parseType(f)),
                    VertexUV(*parseType(f)),
                    parseType(f),
                    parseType(f)
                ]))
        # geometry
        for i in range(parseType(f)):
            static_mesh_id = parseType(f)
            # vertices
            vertices = VertexContainer()
            for j in range(parseType(f)):
                vertices.add(Vertex(*parseType(f)))
            # normals
            f.read(1)
            normals = VertexContainer()
            for j in range(parseType(f)):
                normals.add(Vertex(*parseType(f)))
            transform = parseType(f)
            # polygons
            polygons = PolygonContainer()
            for j in range(parseType(f)):
                polygons.add(Polygon(
                    parseType(f),
                    parseType(f),
                    parseType(f),
                    parseType(f),
                    parseType(f),
                    self.ldb.getMaterials().getMaterialByIndex(parseType(f)),
                    self.ldb.getLightMaps().getTextureById(parseType(f)),
                    parseType(f),
                    parseType(f),
                    parseType(f)
                ))
            f.read(1)
            # seems another bsp thing
            for j in range(parseType(f)):
                parseType(f)  # int
                parseType(f)  # float
            self.ldb.getStaticMeshes().addStaticMesh(StaticMesh(
                static_mesh_id,
                vertices,
                normals,
                transform,
                polygons
            ))

    def parseDynamicLights(self, f) -> None:
        for i in range(parseType(f)):
            self.ldb.getDynamicLights().add(DynamicLight(
                parseType(f),
                EntityProperties(parseType(f), parseType(f), parseType(f), parseType(f), parseType(f)),
                parseType(f),
                parseType(f),
                parseType(f),
                parseType(f),
                parseType(f),
                parseType(f),
                parseType(f),
                parseType(f),
                parseType(f),
                parseType(f),
                parseType(f)
            ))

    def parseWaypoints(self, f) -> None:
        for i in range(parseType(f)):
            self.ldb.getWaypoints().add(Waypoint(
                parseType(f),
                EntityProperties(parseType(f), parseType(f), parseType(f), parseType(f), parseType(f)),
                parseType(f)))

    def parseFSMs(self, f) -> None:
        for i in range(parseType(f)):
            shared_name = parseType(f)
            properties = EntityProperties(parseType(f), parseType(f), parseType(f), parseType(f), parseType(f))
            # custom states
            f.read(1)
            states = FSMStateContainer()
            for j in range(parseType(f)):
                states.add(parseType(f))
            states.setDefault(parseType(f))
            # startup event before message
            f.read(1)
            startup_before = FSMMessageContainer()
            for j in range(parseType(f)):
                startup_before.add(parseType(f))
            # unk seems startup for state specific
            f.read(1)
            for j in range(parseType(f)):
                parseType(f)
                # startup event after message
            f.read(1)
            startup_after = FSMMessageContainer()
            for j in range(parseType(f)):
                startup_after.add(parseType(f))
            # custom states switch messages
            f.read(1)
            state_switch = FSMEventContainer()
            for j in range(parseType(f)):
                state_name = parseType(f)
                # before
                f.read(1)
                before = FSMMessageContainer()
                for k in range(parseType(f)):
                    before.add(parseType(f))
                # state specific
                f.read(1)
                state_specific = FSMStateSpecificMessageContainer()
                for k in range(parseType(f)):
                    state_name = parseType(f)
                    f.read(1)
                    messages = FSMMessageContainer()
                    for l in range(parseType(f)):
                        messages.add(parseType(f))
                    state_specific.add(FSMStateSpecificMessage(state_name, messages))
                # after
                f.read(1)
                after = FSMMessageContainer()
                for k in range(parseType(f)):
                    after.add(parseType(f))
                state_switch.add(FSMEvent(state_name, before, state_specific, after))
            # custom string messages
            f.read(1)
            custom_string = FSMEventContainer()
            for j in range(parseType(f)):
                state_name = parseType(f)
                # before
                f.read(1)
                before = FSMMessageContainer()
                for k in range(parseType(f)):
                    before.add(parseType(f))
                # state specific
                f.read(1)
                state_specific = FSMStateSpecificMessageContainer()
                for k in range(parseType(f)):
                    state_name = parseType(f)
                    f.read(1)
                    messages = FSMMessageContainer()
                    for l in range(parseType(f)):
                        messages.add(parseType(f))
                    state_specific.add(FSMStateSpecificMessage(state_name, messages))
                # after
                f.read(1)
                after = FSMMessageContainer()
                for k in range(parseType(f)):
                    after.add(parseType(f))
                custom_string.add(FSMEvent(state_name, before, state_specific, after))
            # entity specific messages
            f.read(1)
            entity_specific = FSMEventContainer()
            for j in range(parseType(f)):
                state_name = parseType(f)
                # before
                f.read(1)
                before = FSMMessageContainer()
                for k in range(parseType(f)):
                    before.add(parseType(f))
                # state specific
                f.read(1)
                state_specific = FSMStateSpecificMessageContainer()
                for k in range(parseType(f)):
                    state_name = parseType(f)
                    f.read(1)
                    messages = FSMMessageContainer()
                    for l in range(parseType(f)):
                        messages.add(parseType(f))
                    state_specific.add(FSMStateSpecificMessage(state_name, messages))
                # after
                f.read(1)
                after = FSMMessageContainer()
                for k in range(parseType(f)):
                    after.add(parseType(f))
                entity_specific.add(FSMEvent(state_name, before, state_specific, after))
            self.ldb.getFSMs().add(
                FSM(shared_name, properties, states, startup_before, startup_after, state_switch, custom_string,
                    entity_specific))

    def parseCharacters(self, f) -> None:
        for i in range(parseType(f)):
            shared_name = parseType(f)
            properties = EntityProperties(parseType(f), parseType(f), parseType(f), parseType(f), parseType(f))
            character_name = parseType(f)
            f.read(1)
            startup_before = FSMMessageContainer()
            for j in range(parseType(f)):
                startup_before.add(parseType(f))
            f.read(1)
            on_death_before = FSMMessageContainer()
            for j in range(parseType(f)):
                on_death_before.add(parseType(f))
            f.read(1)
            on_activate_before = FSMMessageContainer()
            for j in range(parseType(f)):
                on_activate_before.add(parseType(f))
            f.read(1)
            on_special_before = FSMMessageContainer()
            for j in range(parseType(f)):
                on_special_before.add(parseType(f))
            self.ldb.getCharacters().add(
                Character(shared_name, properties, character_name, startup_before, on_death_before, on_activate_before,
                          on_special_before))

    def parseTriggers(self, f) -> None:
        for i in range(parseType(f)):
            shared_name = parseType(f)
            properties = EntityProperties(parseType(f), parseType(f), parseType(f), parseType(f), parseType(f))
            radius = parseType(f)
            # 0 - action_button 3 - character_collide 4 - look_at_trigger 1 - player_collide 2 - projectile_collide
            type = parseType(f)
            self.ldb.getTriggers().add(Trigger(shared_name, properties, radius, type))

    def parseDynamicMeshes(self, f) -> None:
        # uv attributes
        f.read(1)
        for i in range(parseType(f)):
            self.ldb.getDynamicMeshes().getTextureVertices().add(
                TextureVertex(*[
                    parseType(f),
                    VertexUV(*parseType(f)),
                    VertexUV(*parseType(f)),
                    parseType(f),
                    parseType(f)
                ]))
        # geometry
        for i in range(parseType(f)):
            shared_name = parseType(f)
            # vertices
            vertices = VertexContainer()
            for j in range(parseType(f)):
                vertices.add(Vertex(*parseType(f)))
            # normals
            f.read(1)
            normals = VertexContainer()
            for j in range(parseType(f)):
                normals.add(Vertex(*parseType(f)))
            transform = parseType(f)
            # polygons
            polygons = PolygonContainer()
            for j in range(parseType(f)):
                polygons.add(Polygon(
                    parseType(f),
                    parseType(f),
                    parseType(f),
                    parseType(f),
                    parseType(f),
                    self.ldb.getMaterials().getMaterialByIndex(parseType(f)),
                    self.ldb.getLightMaps().getTextureById(parseType(f)),
                    parseType(f),
                    parseType(f),
                    parseType(f)
                ))
            f.read(1)
            # radiosity light config value?
            unk1 = parseType(f)
            properties = EntityProperties(parseType(f), parseType(f), parseType(f), parseType(f), parseType(f))
            # animation
            animations = AnimationContainer()
            for j in range(parseType(f)):
                animation_name = parseType(f)
                length_in_secs = parseType(f)
                start_transform = parseType(f)
                end_transform = parseType(f)
                f.read(1)
                leaving_first_frame = FSMMessageContainer()
                for k in range(parseType(f)):
                    leaving_first_frame.add(parseType(f))
                f.read(1)
                returning_first_frame = FSMMessageContainer()
                for k in range(parseType(f)):
                    returning_first_frame.add(parseType(f))
                f.read(1)
                reaching_second_frame = FSMMessageContainer()
                for k in range(parseType(f)):
                    reaching_second_frame.add(parseType(f))
                # translation graph
                parseType(f)  # header
                parseType(f)  # major version
                parseType(f)  # minor version
                sample_rate = parseType(f)
                translation_graph = Graph(sample_rate)
                for k in range(sample_rate):
                    translation_graph.addPoint(parseType(f))
                # rotation graph
                parseType(f)  # header
                parseType(f)  # major version
                parseType(f)  # minor version
                sample_rate = parseType(f)
                rotation_graph = Graph(sample_rate)
                for k in range(sample_rate):
                    rotation_graph.addPoint(parseType(f))
                animations.add(Animation(
                    animation_name,
                    length_in_secs,
                    start_transform,
                    end_transform,
                    leaving_first_frame,
                    returning_first_frame,
                    reaching_second_frame,
                    translation_graph,
                    rotation_graph
                ))
            config = DynamicMeshConfig(parseType(f), parseType(f), parseType(f), parseType(f), parseType(f),
                                       parseType(f))
            # bsp things
            parseType(f)
            parseType(f)
            parseType(f)
            parseType(f)

            self.ldb.getDynamicMeshes().addDynamicMesh(DynamicMesh(
                shared_name,
                properties,
                vertices,
                normals,
                transform,
                polygons,
                animations,
                config
            ))

    def parseItems(self, f) -> None:
        for i in range(parseType(f)):
            self.ldb.getItems().add(Item(
                parseType(f),
                EntityProperties(parseType(f), parseType(f), parseType(f), parseType(f), parseType(f)),
                parseType(f)))

    def parsePointLights(self, f) -> None:
        for i in range(parseType(f)):
            self.ldb.getPointlights().add(PointLight(
                parseType(f),
                EntityProperties(parseType(f), parseType(f), parseType(f), parseType(f), parseType(f)),
                parseType(f),
                parseType(f),
                parseType(f),
                parseType(f),
                parseType(f),
                parseType(f)))

    def parseRooms(self, f) -> None:
        for i in range(parseType(f)):
            id = parseType(f)
            # static meshes ids
            f.read(1)
            static_meshes: list[int] = []
            for j in range(parseType(f)):
                static_meshes.append(parseType(f))
            # dynamic lights
            f.read(1)
            dynamic_lights: list[str] = []
            for j in range(parseType(f)):
                dynamic_lights.append(parseType(f))
            # exits
            f.read(1)
            exits: list[str] = []
            for j in range(parseType(f)):
                exits.append(parseType(f))
            # start points
            f.read(1)
            start_points: list[str] = []
            for j in range(parseType(f)):
                start_points.append(parseType(f))
            # fsms
            f.read(1)
            fsms: list[str] = []
            for j in range(parseType(f)):
                fsms.append(parseType(f))
            # characters
            f.read(1)
            characters: list[str] = []
            for j in range(parseType(f)):
                characters.append(parseType(f))
            # triggers
            f.read(1)
            triggers: list[str] = []
            for j in range(parseType(f)):
                triggers.append(parseType(f))
            # dynamic meshes
            f.read(1)
            dynamic_meshes: list[str] = []
            for j in range(parseType(f)):
                dynamic_meshes.append(parseType(f))
            # items
            f.read(1)
            level_items: list[str] = []
            for j in range(parseType(f)):
                level_items.append(parseType(f))
            # pointlights
            f.read(1)
            point_lights: list[int] = []
            for j in range(parseType(f)):
                point_lights.append(parseType(f))
            room_name = parseType(f)
            ai_net_density = parseType(f)

            self.ldb.getRooms().add(Room(
                id,
                room_name,
                static_meshes,
                dynamic_lights,
                exits,
                start_points,
                fsms,
                characters,
                triggers,
                dynamic_meshes,
                level_items,
                point_lights
            ))

            # bsp
            parseType(f)
            parseType(f)
            parseType(f)
            parseType(f)

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.ldb: MaxLDB = MaxLDB()

    def parse(self) -> MaxLDB:
        self.ldb: MaxLDB = MaxLDB()
        try:
            with open(self.file_path, "rb") as f:
                self.parseBSP(f)
                self.parseMaterials(f)
                self.parseExits(f)
                self.parseStaticMeshes(f)
                self.parseDynamicLights(f)
                self.parseWaypoints(f)
                self.parseFSMs(f)
                self.parseCharacters(f)
                self.parseTriggers(f)
                self.parseDynamicMeshes(f)
                self.parseItems(f)
                self.parsePointLights(f)
                self.parseRooms(f)
        except IOError:
            print("Error While Opening the file! %s" % self.file_path)
        return self.ldb


class MaxLBDReaderFactory:
    @staticmethod
    def createReader(file_path: str) -> MaxLDBReaderInterface:
        is_ldb2: bool = False
        with open(file_path, "rb") as f:
            ldb2_header = int.from_bytes(f.read(4), byteorder='little', signed=False)
            if ldb2_header == 843203660:
                is_ldb2 = True
        if is_ldb2:
            return MaxLDBReader2(file_path)
        else:
            return MaxLDBReader(file_path)
