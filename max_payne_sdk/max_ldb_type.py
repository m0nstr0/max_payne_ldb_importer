from __future__ import annotations

class Vertex:
    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z

class VertexContainer:
    def __init__(self) -> None:
        self.vertices: list[Vertex] = []

    def add(self, vertex: Vertex) -> None:
        self.vertices.append(vertex)

class BSPVertex(Vertex):
    pass

class BSPPolygon:
    def __init__(self, vertex_idx: int, num_vertices: int, polygon_id: int, static_mesh_id: int, normal: Vertex, pivot: Vertex) -> None:
        self.vertex_idx : int = vertex_idx
        self.num_vertices : int = num_vertices
        self.polygon_id : int = polygon_id
        self.static_mesh_id : int = static_mesh_id
        self.normal : Vertex = normal
        self.pivot : Vertex = pivot

class BSPNode:
    def __init__(self, normal: Vertex, pivot: Vertex, unk1: int, unk2 : int, unk3 : int, unk4 : int, unk5 : int, unk6: int) -> None:
        self.normal : Vertex = normal
        self.pivot : Vertex = pivot       
        self.unk1 : int = unk1
        self.unk2 : int = unk2
        self.unk3 : int = unk3
        self.unk4 : int = unk4
        self.unk5 : int = unk5
        self.unk6 : int = unk6

class BSPPolygonIndex:
    def __init__(self, polygon_id: int) -> None:
        self.polygon_id: int = polygon_id

class BSPVertexContainer:
    def __init__(self) -> None:
        self.vertices: list[BSPVertex] = []

    def add(self, vertex: BSPVertex) -> None:
        self.vertices.append(vertex)

class BSPPolygonsContainer:
    def __init__(self) -> None:
        self.polygons: list[BSPPolygon] = []

    def add(self, polygon: BSPPolygon) -> None:
        self.polygons.append(polygon)

class BSPNodesContainer:
    def __init__(self) -> None:
        self.nodes: list[BSPNode] = []

    def add(self, node: BSPNode) -> None:
        self.nodes.append(node)

class BSPPolygonIndicesContainer:
    def __init__(self) -> None:
        self.indices: list[BSPPolygonIndex] = []

    def add(self, index: BSPPolygonIndex) -> None:
        self.indices.append(index)

class BSPContainer:
    def __init__(self) -> None:
        self.vertices: BSPVertexContainer = BSPVertexContainer()
        self.polygons: BSPPolygonsContainer = BSPPolygonsContainer()
        self.nodes: BSPNodesContainer = BSPNodesContainer()
        self.indices: BSPPolygonIndicesContainer = BSPPolygonIndicesContainer()

    def getVertices(self) -> BSPVertexContainer:
        return self.vertices

    def getPolygons(self) -> BSPPolygonsContainer:
        return self.polygons

    def getNodes(self) -> BSPNodesContainer:
        return self.nodes

    def getIndices(self) -> BSPPolygonIndicesContainer:
        return self.indices

class Texture:
    def __init__(self, file_path: str, file_type: int, data : bytes) -> None:
        self.file_path : str = file_path
        self.file_type : int = file_type
        self.data : bytes = data

    def getFileTypeName(self):
        if self.file_type == 0:
            return "tga" 
        if self.file_type == 2:
            return "scx" 
        if self.file_type == 3:
            return "pcx"  
        if self.file_type == 4:
            return "jpg"
        if self.file_type == 5:
            return "dds" 
        raise Exception("Unknown texture file type %i" % self.file_type)

class TextureContainer:
    def __init__(self) -> None:
        self.textures : list[Texture] = []

    def add(self, texture: Texture) -> None:
        self.textures.append(texture)

    def findTextureByFileName(self, file_path: str) -> Texture:
        for texture in self.textures:
            if texture.file_path == file_path:
                return texture
        return None

class LightMapTexture:
    def __init__(self, id: int, file_type: int, data : bytes) -> None:
        self.id : int = id
        self.file_type : int = file_type
        self.data : bytes = data

    def getFileTypeName(self):
        if self.file_type == 0:
            return "tga" 
        if self.file_type == 2:
            return "scx" 
        if self.file_type == 3:
            return "pcx"  
        if self.file_type == 4:
            return "jpg"
        if self.file_type == 5:
            return "dds" 
        raise Exception("Unknown texture file type %i" % self.file_type)

class LightMapTextureContainer:
    def __init__(self) -> None:
        self.textures : list[LightMapTexture] = []

    def add(self, texture: LightMapTexture) -> None:
        self.textures.append(texture)

    def getTextureById(self, id: int) -> LightMapTexture:
        for texture in self.textures:
            if texture.id == id:
                return texture
        if id == -1:
            return None
        raise Exception("LightmapTexture not found with id %i" % id)

class MaterialProperties:
    def __init__(self, has_alpha_test: int = 0, has_adult_content: int = 0) -> None:
        self.has_alpha_test: int  = has_alpha_test
        self.has_adult_content: int = has_adult_content

class Material:
    def __init__(self, idx: int, id: int, category_name: str, material_name: str) -> None:
        self.idx: int = idx
        self.id: int = id
        self.category_name: str = category_name
        self.material_name: str = material_name
        self.diffuse_texture: Texture = None
        self.alpha_texture: Texture = None
        self.properties: MaterialProperties = MaterialProperties()
    
    def setDiffuseTexture(self, texture: Texture):
        self.diffuse_texture = texture
        
    def setAlphaTexture(self, texture: Texture):
        self.alpha_texture = texture

    def setProperties(self, has_alpha_test: int, has_adult_content: int):
        self.properties.has_alpha_test = has_alpha_test
        self.properties.has_adult_content = has_adult_content
        
class MaterialContainer:
    def __init__(self) -> None:
        self.materials: list[Material] = []

    def add(self, material: Material) -> None:
        self.materials.append(material)

    def findMaterialByCategoryAndName(self, category_name: str, material_name: str) -> Material:
        for material in self.materials:
            if material.category_name == category_name and material.material_name == material_name:
                return material
        return None

    def getMaterialByIndex(self, idx: int) -> Material:
        for material in self.materials:
            if material.idx == idx:
                return material
        raise Exception("Material not found with index %i" % idx)

class Exit:
    def __init__(self, exit_name: str, vertices: VertexContainer, normal: Vertex, transform, room_id: int, parent_room_id: int, parent_room_name: str) -> None:
        self.exit_name = exit_name
        self.vertices: VertexContainer = vertices
        self.normal: Vertex = normal
        self.transform = transform
        self.room_id: int = room_id
        self.parent_room_id: int = parent_room_id
        self.parent_room_name: str = parent_room_name

class ExitContainer:
    def __init__(self) -> None:
        self.exits: list[Exit] = []

    def add(self, exit: Exit) -> None:
        self.exits.append(exit)

class VertexUV:
    def __init__(self, u: float, v: float) -> None:
        self.u: float = u
        self.v: float = v

class TextureVertex:
    def __init__(self, vertex_idx: int, uv: VertexUV, lightmap_uv: VertexUV, flags: uint, is_hidden: int) -> None:
        self.vertex_idx: int = vertex_idx
        self.uv: VertexUV = uv
        self.lightmap_uv: VertexUV = lightmap_uv
        self.flags: uint = flags
        self.is_hidden: int = is_hidden

class TextureVertexContainer:
    def __init__(self) -> None:
        self.texture_vertices: list[TextureVertex] = []

    def add(self, texture_vertex: TextureVertex) -> None:
        self.texture_vertices.append(texture_vertex)

class Polygon:
    def __init__(self, id: int, texture_vertex_idx: int, num_vertices: int, normal: int, type: uint, material: Material, lightmap: LightMapTexture, max_edge_length: float, max_angle: float, smoothing_group: int) -> None:
        self.id: int = id
        self.texture_vertex_idx: int = texture_vertex_idx
        self.num_vertices: int = num_vertices
        self.normal: int = normal
        self.type: uint = type
        self.material: Material = material
        self.lightmap: LightMapTexture = lightmap
        self.max_edge_length: float = max_edge_length
        self.max_angle: float = max_angle
        self.smoothing_group: int = smoothing_group

class PolygonContainer:
    def __init__(self) -> None:
        self.polygons: list[Polygon] = []

    def add(self, polygon: Polygon):
        self.polygons.append(polygon)

class Geometry:
    def __init__(self, vertices: list[Vertex], normals: list[Vertex], uv: list[VertexUV], material: Material) -> None:
        self.vertices: list[Vertex] = vertices
        self.normals: list[Vertex] = normals
        self.uv: list[VertexUV] = uv
        self.material: Material = material

class StaticMesh:
    def __init__(self, static_mesh_id: int, vertices: VertexContainer, normals: VertexContainer, transform, polygons: PolygonContainer) -> None:
        self.static_mesh_id: int = static_mesh_id
        self.vertices: VertexContainer = vertices 
        self.normals: VertexContainer = normals
        self.transform = transform
        self.polygons: PolygonContainer = polygons
        self.texture_vertices: TextureContainer = None
    
    def numPolygons(self):
        return len(self.polygons.polygons)

    def constructPolygon(self, id: int) -> Geometry:
        polygon = self.polygons.polygons[id]
        vertices: list[Vertex] = []
        normals: list[Vertex] = []
        uv: list[VertexUV] = []

        for i in range(polygon.num_vertices):
            texture_vertex = self.texture_vertices.texture_vertices[polygon.texture_vertex_idx + i]
            vertices.append(self.vertices.vertices[texture_vertex.vertex_idx])
            normals.append(self.normals.vertices[texture_vertex.vertex_idx])
            uv.append(texture_vertex.uv)
        
        return Geometry(vertices, normals, uv, polygon.material)

class StaticMeshContainer:
    def __init__(self) -> None:
        self.texture_vertices: TextureVertexContainer = TextureVertexContainer()
        self.static_meshes: list[StaticMesh] = []
    
    def getById(self, static_mesh_id: int) -> StaticMesh:
        for static_mesh in self.static_meshes:
            if static_mesh.static_mesh_id == static_mesh_id:
                return static_mesh
        raise Exception("Static Mesh not found with id %i" % static_mesh_id)

    def getTextureVertices(self) -> TextureVertexContainer:
        return self.texture_vertices

    def addStaticMesh(self, static_mesh: StaticMesh) -> None:
        static_mesh.texture_vertices = self.texture_vertices
        self.static_meshes.append(static_mesh)

class EntityProperties:
    def __init__(self, name: str, object_to_room_transform, object_to_parent_transform, room_id : int, parent_dynamic_mesh_name: str) -> None:
        self.name: str = name
        self.object_to_room_transform = object_to_room_transform
        self.object_to_parent_transform = object_to_parent_transform
        self.room_id : int = room_id
        self.parent_dynamic_mesh_name: str = parent_dynamic_mesh_name

class DynamicLight:
    def __init__(self, shared_name: str, object_properties: EntityProperties, transform, unk1: float, unk2: float, unk3: float, unk4: float, unk5: float, unk6: float, unk7: float, unk8: float, unk9: float, unk10: float) -> None:
        self.shared_name: str = shared_name
        self.object_properties: EntityProperties = object_properties
        self.transform = transform
        self.unk1: float = unk1
        self.unk2: float = unk2
        self.unk3: float = unk3
        self.unk4: float = unk4
        self.unk5: float = unk5
        self.unk6: float = unk6
        self.unk7: float = unk7
        self.unk8: float = unk8
        self.unk9: float = unk9
        self.unk10: float = unk10

class DynamicLightContainer:
    def __init__(self) -> None:
        self.lights: list[DynamicLight] = []

    def add(self, light: DynamicLight):
        self.lights.append(light)

class Waypoint:
    def __init__(self, shared_name: str, object_properties: EntityProperties, type: int) -> None:
        self.shared_name: str = shared_name
        self.object_properties: EntityProperties = object_properties
        self.type: int = type #0 - waypoint 1 - startpoint

class WaypointContainer:
    def __init__(self) -> None:
        self.waypoints: list[Waypoint] = []

    def add(self, waypoint: Waypoint):
        self.waypoints.append(waypoint)

class FSMMessageContainer:
    def __init__(self) -> None:
        self.messages: list[str] = []
    
    def add(self, message: str):
        self.messages.append(message)

class FSMStateSpecificMessage:
    def __init__(self, state_name: str, messages: FSMMessageContainer) -> None:
        self.state_name: str = state_name
        self.messages: FSMMessageContainer = messages

class FSMStateSpecificMessageContainer:
    def __init__(self) -> None:
        self.messages: list[FSMStateSpecificMessage] = []
    
    def add(self, message: FSMStateSpecificMessage) -> None:
        self.messages.append(message)

class FSMEvent:
    def __init__(self, state_name: str, before: FSMMessageContainer, state_specific: FSMStateSpecificMessageContainer, after: FSMMessageContainer) -> None:
        self.state_name: str = state_name
        self.before: FSMMessageContainer = before
        self.state_specific: FSMStateSpecificMessageContainer = state_specific
        self.after : FSMMessageContainer = after

class FSMEventContainer:
    def __init__(self) -> None:
        self.events: list[FSMEvent] = []
    
    def add(self, event: FSMEvent) -> None:
        self.events.append(event)

class FSMStateContainer:
    def __init__(self) -> None:
        self.states: list[str] = []
        self.default: str = ""

    def setDefault(self, name: str):
        self.default = name

    def add(self, name: str):
        self.states.append(name)

class FSM:
    def __init__(self, shared_name: str, properties: EntityProperties, states: FSMStateContainer, startup_before: FSMMessageContainer, startup_after: FSMMessageContainer, state_switch: FSMEventContainer, string_specific: FSMEventContainer, entity_specific: FSMEventContainer) -> None:
        self.shared_name: str = shared_name
        self.properties: EntityProperties = properties
        self.states: FSMStateContainer = states
        self.startup_before: FSMMessageContainer = startup_before
        self.startup_after: FSMMessageContainer = startup_after
        self.state_switch: FSMEventContainer = state_switch
        self.string_specific: FSMEventContainer = string_specific
        self.entity_specific: FSMEventContainer = entity_specific
    
class FSMContainer:
    def __init__(self) -> None:
        self.fsms: list[FSM] = []

    def add(self, fsm: FSM):
        self.fsms.append(fsm)

class Character:
    def __init__(self, shared_name: str, properties: EntityProperties, character_name: str, startup_before: FSMMessageContainer, on_death_before: FSMMessageContainer, on_activate_before: FSMMessageContainer, on_special_before: FSMMessageContainer) -> None:
        self.shared_name: str = shared_name
        self.properties: EntityProperties = properties
        self.character_name: str = character_name
        self.startup_before: FSMMessageContainer = startup_before
        self.on_death_before: FSMMessageContainer = on_death_before
        self.on_activate_before: FSMMessageContainer = on_activate_before
        self.on_special_before: FSMMessageContainer = on_special_before

class CharacterContainer:
    def __init__(self) -> None:
        self.characters: list[Character] = []

    def add(self, character: Character):
        self.characters.append(character)

class Trigger:
    def __init__(self, shared_name: str, properties: EntityProperties, radius: float, type: int) -> None:
        self.shared_name: str = shared_name
        self.properties: EntityProperties = properties
        self.radius: float = radius
        self.type: int = type

class TriggerContainer:
    def __init__(self) -> None:
        self.triggers: list[Trigger] = []

    def add(self, trigger: Trigger):
        self.triggers.append(trigger)

class Graph:
    def __init__(self, sample_rate: int) -> None:
        self.sample_rate: int = sample_rate
        self.points: list[float] = []

    def addPoint(self, f: float) -> None:
        self.points.append(f)

class Animation:
    def __init__(self, animation_name: str, length_in_secs: float, start_transform, end_transform, leaving_first_frame: FSMMessageContainer, returning_first_frame: FSMMessageContainer, reaching_second_frame: FSMMessageContainer, translation_graph: Graph, rotation_graph: Graph) -> None:
        self.animation_name: str = animation_name
        self.length_in_secs: float = length_in_secs
        self.start_transform = start_transform
        self.end_transform = end_transform
        self.leaving_first_frame: FSMMessageContainer = leaving_first_frame
        self.returning_first_frame: FSMMessageContainer = returning_first_frame
        self.reaching_second_frame: FSMMessageContainer = reaching_second_frame
        self.translation_graph: Graph = translation_graph
        self.rotation_graph: Graph = rotation_graph

class AnimationContainer:
    def __init__(self) -> None:
        self.animations: list[Animation] = []

    def add(self, animation: Animation):
        self.animations.append(animation)

class DynamicMeshConfig:
    def __init__(self, dynamic_collisions: int, bullet_collisions: int, light_mapped: int, cont_update: int, pointlight_affected: int, block_explosions: int) -> None:
        self.dynamic_collisions: int = dynamic_collisions
        self.bullet_collisions: int = bullet_collisions
        self.light_mapped: int = light_mapped
        self.cont_update: int = cont_update
        self.pointlight_affected: int = pointlight_affected
        self.block_explosions: int = block_explosions

class DynamicMesh:
    def __init__(self, shared_name: str, properties: EntityProperties, vertices: VertexContainer, normals: VertexContainer, transform, polygons: PolygonContainer, animations: AnimationContainer, config: DynamicMeshConfig) -> None:
        self.shared_name: str = shared_name
        self.properties: EntityProperties = properties
        self.vertices: VertexContainer = vertices
        self.normals: VertexContainer = normals
        self.transform = transform
        self.polygons: PolygonContainer = polygons
        self.animations: AnimationContainer = animations
        self.config: DynamicMeshConfig = config
        self.texture_vertices: TextureContainer = None
    
    def numPolygons(self):
        return len(self.polygons.polygons)

    def constructPolygon(self, id: int) -> Geometry:
        polygon = self.polygons.polygons[id]
        vertices: list[Vertex] = []
        normals: list[Vertex] = []
        uv: list[VertexUV] = []

        for i in range(polygon.num_vertices):
            texture_vertex = self.texture_vertices.texture_vertices[polygon.texture_vertex_idx + i]
            vertices.append(self.vertices.vertices[texture_vertex.vertex_idx])
            normals.append(self.normals.vertices[texture_vertex.vertex_idx])
            uv.append(texture_vertex.uv)
        
        return Geometry(vertices, normals, uv, polygon.material)

class DynamicMeshContainer:
    def __init__(self) -> None:
        self.texture_vertices: TextureVertexContainer = TextureVertexContainer()
        self.dynamic_meshes: list[DynamicMesh] = []

    def addDynamicMesh(self, dynamic_mesh: DynamicMesh):
        dynamic_mesh.texture_vertices = self.texture_vertices
        self.dynamic_meshes.append(dynamic_mesh)

    def getTextureVertices(self) -> TextureVertexContainer:
        return self.texture_vertices

    def getBySharedName(self, name: str) -> DynamicMesh:
        for dynamic_mesh in self.dynamic_meshes:
            if dynamic_mesh.shared_name == name:
                return dynamic_mesh
        raise Exception("Dynamic Mesh not found with name %s" % name)

class Item:
    def __init__(self, shared_name: str, object_properties: EntityProperties, item_name: str) -> None:
        self.shared_name: str = shared_name
        self.object_properties: EntityProperties = object_properties
        self.item_name: str = item_name

class ItemContainer:
    def __init__(self) -> None:
        self.items: list[Item] = []

    def add(self, item: Item):
        self.items.append(item)

class PointLight:
    def __init__(self, id: int, object_properties: EntityProperties, r: float, g: float, b: float, a: float, falloff: float, intensity: float) -> None:
        self.id: int = id
        self.object_properties: EntityProperties = object_properties
        self.r: str = r
        self.g: str = g
        self.b: str = b
        self.a: str = a
        self.falloff: str = falloff
        self.intensity: str = intensity

class PointLightContainer:
    def __init__(self) -> None:
        self.pointlights: list[PointLight] = []

    def add(self, pointlight: PointLight):
        self.pointlights.append(pointlight)

class Room:
    def __init__(self, id: int, name: str, static_meshes: list[int], dynamic_lights: list[str], exits: list[str], start_points: list[str], fsms: list[str], characters: list[str], triggers: list[str], dynamic_meshes: list[str], level_items: list[str], point_lights: list[int]) -> None:
        self.id: int = id
        self.name: str = name
        self.static_meshes: list[int] = static_meshes
        self.dynamic_lights: list[str] = dynamic_lights
        self.exits: list[str] = exits
        self.start_points: list[str] = start_points
        self.fsms: list[str] = fsms
        self.characters: list[str] = characters
        self.triggers: list[str] = triggers
        self.dynamic_meshes: list[str] = dynamic_meshes
        self.level_items: list[str] = level_items
        self.point_lights: list[int] = point_lights

class RoomContainer:
    def __init__(self) -> None:
        self.rooms: list[Room] = []

    def add(self, room: Room):
        self.rooms.append(room)

class MaxLDB:
    def __init__(self) -> None:
        self.bsp: BSPContainer = BSPContainer()
        self.materials: MaterialContainer = MaterialContainer()
        self.textures: TextureContainer = TextureContainer()
        self.lightmaps: LightMapTextureContainer = LightMapTextureContainer()
        self.exits: ExitContainer = ExitContainer()
        self.static_meshes: StaticMeshContainer = StaticMeshContainer()
        self.dynamic_lights: DynamicLightContainer = DynamicLightContainer()
        self.waypoints: WaypointContainer = WaypointContainer()
        self.fsms: FSMContainer = FSMContainer()
        self.characters: CharacterContainer = CharacterContainer()
        self.triggers: TriggerContainer = TriggerContainer()
        self.dynamic_meshes: DynamicMeshContainer = DynamicMeshContainer()
        self.items: ItemContainer = ItemContainer()
        self.pointlights: PointLightContainer = PointLightContainer()
        self.rooms: RoomContainer = RoomContainer()

    def getBsp(self) -> BSPContainer:
        return self.bsp

    def getTextures(self) -> TextureContainer:
        return self.textures
    
    def getMaterials(self) -> MaterialContainer:
        return self.materials

    def getLightMaps(self) -> LightMapTextureContainer:
        return self.lightmaps

    def getExits(self) -> ExitContainer:
        return self.exits

    def getStaticMeshes(self) -> StaticMeshContainer:
        return self.static_meshes

    def getDynamicLights(self) -> DynamicLightContainer:
        return self.dynamic_lights

    def getWaypoints(self) -> WaypointContainer:
        return self.waypoints

    def getFSMs(self) -> FSMContainer:
        return self.fsms

    def getCharacters(self) -> CharacterContainer:
        return self.characters

    def getTriggers(self) -> TriggerContainer:
        return self.triggers

    def getDynamicMeshes(self) -> DynamicMeshContainer:
        return self.dynamic_meshes

    def getItems(self) -> ItemContainer:
        return self.items

    def getPointlights(self) -> PointLightContainer:
        return self.pointlights

    def getRooms(self) -> RoomContainer:
        return self.rooms