import math

from max_payne_sdk.lvl2.max_chunk import MaxChunk
from max_payne_sdk.lvl2.max_node import MaxNode
from max_payne_sdk.lvl2.max_pack import packInt, packUInt, packDouble, packFloat, packBool, packULong, packString


class MaxNodeMeshTriangle:
    def __init__(self):
        self.normal = []
        self.indices = []

    def getBytes(self):
        data = [
            packDouble(self.normal[0]),
            packDouble(self.normal[1]),
            packDouble(self.normal[2]),
            packInt(len(self.indices))
        ]

        for i in self.indices:
            data.append(packInt(i))

        return data


class MaxNodeMeshTextureSpace:
    def __init__(self):
        self.normal1 = [0.0, 0.0, 0.0]
        self.normal2 = [0.0, 0.0, 0.0]
        self.matrix3x3 = [1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0]
        self.vec2 = [0.0, 0.0]

    def normalize(self, v):
        x, y, z = v

        sum = x * x + y * y + z * z

        if sum == 0:
            raise ValueError(f"Normal is zero {v} : {self.normal1}")

        length = math.sqrt(sum)
        return [x / length, y / length, z / length]

    def cross_product(self, a, b):
        ax, ay, az = a
        bx, by, bz = b

        cx = ay * bz - az * by
        cy = az * bx - ax * bz
        cz = ax * by - ay * bx
        return [cx, cy, cz]

    def setNormal(self, normal):
        print(f"setted normal {normal}")
        self.normal1 = normal[:]
        self.fillNormals()

    def fillNormals(self):
        helper = []
        ax, ay, az = abs(self.normal1[0]), abs(self.normal1[1]), abs(self.normal1[2])
        if ax <= ay and ax <= az:
            helper = [1, 0, 0]
        elif ay <= az:
            helper = [0, 1, 0]
        else:
            helper = [0, 0, 1]

        print(f"after helper is {helper} normal is {self.normal1}")

        T = self.normalize(self.cross_product(helper, self.normal1))
        B = self.cross_product(self.normal1, T)

        self.matrix3x3[0] = T[0]
        self.matrix3x3[1] = T[1]
        self.matrix3x3[2] = T[2]
        self.matrix3x3[3] = B[0]
        self.matrix3x3[4] = B[1]
        self.matrix3x3[5] = B[2]
        self.matrix3x3[6] = self.normal1[0]
        self.matrix3x3[7] = self.normal1[1]
        self.matrix3x3[8] = self.normal1[2]

    def getBytes(self):
        self.fillNormals()

        data = [
            packDouble(self.normal1[0]),
            packDouble(self.normal1[1]),
            packDouble(self.normal1[2]),
            packDouble(self.normal2[0]),
            packDouble(self.normal2[1]),
            packDouble(self.normal2[2]),
            packDouble(self.matrix3x3[0]),
            packDouble(self.matrix3x3[1]),
            packDouble(self.matrix3x3[2]),
            packDouble(self.matrix3x3[3]),
            packDouble(self.matrix3x3[4]),
            packDouble(self.matrix3x3[5]),
            packDouble(self.matrix3x3[6]),
            packDouble(self.matrix3x3[7]),
            packDouble(self.matrix3x3[8]),
            packDouble(self.vec2[0]),
            packDouble(self.vec2[1])
        ]

        return data


class MaxNodeMeshLightMap:
    def __init__(self):
        self.texture_space = MaxNodeMeshTextureSpace()
        self.light_map_unk1 = 0  # is not used
        self.light_map_resolution = 0
        self.light_map_is_valid = False
        self.light_map_id = 4294967295
        self.light_map_type = 0

    def getBytes(self):
        data = ([packInt(self.light_map_unk1)] +
                self.texture_space.getBytes())
        data = data + [
            packFloat(self.light_map_resolution),
            packBool(self.light_map_is_valid),
            packULong(self.light_map_id),
            packUInt(self.light_map_type)
        ]

        return data


class MaxNodeMeshLightMapUnk:
    def __init__(self):
        self.texture_space = MaxNodeMeshTextureSpace()
        self.light_map_unk1 = 0  # is not used

    def getBytes(self):
        data = [packInt(self.light_map_unk1)]
        data = data + self.texture_space.getBytes()
        return data


class MaxNodeMeshPolygon:
    def __init__(self):
        self.polygon_id = 0
        self.edges = []  # [[from, to]]
        self.normal = []
        self.reverse_normal = []
        self.matrix3x3 = [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0]  # deprecated always identity
        self.texture_space = MaxNodeMeshTextureSpace()
        self.light_map = MaxNodeMeshLightMap()  # MaxNodeMeshLightMap
        self.point_on_plane = []
        self.exit_id = -1
        self.material_category = ''
        self.material_name = ''
        self.triangles = []  # MaxNodeMeshTriangle
        self.light_map_unk = [MaxNodeMeshLightMapUnk()]  # MaxNodeMeshTextureSpace

    def setNormal(self, normal):
        self.normal = [normal[0], normal[1], normal[2]]
        self.reverse_normal = [-normal[0], -normal[1], -normal[2]]
        self.texture_space.setNormal([normal[0], normal[1], normal[2]])
        self.light_map.texture_space.setNormal([-normal[0], -normal[1], -normal[2]])
        for triangle in self.triangles:
            triangle.normal = normal[normal[0], normal[1], normal[2]]
        self.light_map_unk[0].texture_space.setNormal([-normal[0], -normal[1], -normal[2]])

    def setMaterial(self, material_name, material_category):
        self.material_category = material_category
        self.material_name = material_name

    def setPointOnPlane(self, point):
        self.point_on_plane = point[:]

    def getBytes(self):
        max_chunk = MaxChunk(0, 3)

        #self.setNormal(self.normal)

        data = [
            packUInt(self.polygon_id),
            packInt(len(self.edges)),
            packDouble(self.normal[0]),
            packDouble(self.normal[1]),
            packDouble(self.normal[2]),
            packDouble(self.reverse_normal[0]),
            packDouble(self.reverse_normal[1]),
            packDouble(self.reverse_normal[2]),
            packDouble(self.matrix3x3[0]),
            packDouble(self.matrix3x3[1]),
            packDouble(self.matrix3x3[2]),
            packDouble(self.matrix3x3[3]),
            packDouble(self.matrix3x3[4]),
            packDouble(self.matrix3x3[5]),
            packDouble(self.matrix3x3[6]),
            packDouble(self.matrix3x3[7]),
            packDouble(self.matrix3x3[8])
        ]

        data = data + self.texture_space.getBytes()

        data = data + [
            packDouble(self.point_on_plane[0]),
            packDouble(self.point_on_plane[1]),
            packDouble(self.point_on_plane[2])
        ]

        data = data + self.light_map.getBytes()

        data = data + [
            packInt(self.exit_id),
            packString(self.material_category),
            packString(self.material_name),
        ]

        for edge in self.edges:
            data = data + [packInt(edge[0]), packInt(edge[1])]

        data.append(packInt(len(self.triangles)))

        for triangle in self.triangles:
            data = data + triangle.getBytes()

        data.append(packUInt(2))

        for i in self.light_map_unk:
            data = data + i.getBytes()

        return max_chunk.getBytes(data)


class MaxNodeMeshProperties:
    def __init__(self):
        self.character_collisions = True
        self.use_light_maps = False
        self.point_light_affect = False
        self.fsm_cont_update = False
        self.bullet_collisions = True
        self.cast_no_shadow = False
        self.physics_collisions_enable = True
        self.block_explosions = True
        self.do_no_render = False
        self.no_decals = False
        self.sound_environment = ''
        self.generate_convex_hull = False
        self.ray_tracing = False
        self.physical_material = ''
        self.elevator = False
        self.generate_bounding_box_hull = False

    def getBytes(self):
        max_chunk = MaxChunk(0, 6)
        data = [
            packBool(self.character_collisions),
            packBool(self.use_light_maps),
            packBool(self.point_light_affect),
            packBool(self.fsm_cont_update),
            packBool(self.bullet_collisions),
            packBool(self.cast_no_shadow),
            packBool(self.physics_collisions_enable),
            packBool(self.block_explosions),
            packBool(self.do_no_render),
            packBool(self.no_decals),
            packString(self.sound_environment),
            packBool(self.generate_convex_hull),
            packBool(self.ray_tracing),
            packString(self.physical_material),
            packBool(self.elevator),
            packBool(self.generate_bounding_box_hull)
        ]
        return max_chunk.getBytes(data)


class MaxNodeMesh(MaxNode):
    def __init__(self, id, name):
        super().__init__(id, name)
        self.node_type = 100
        self.node_gameplay_critical = True
        self.has_fsm = False
        self.is_flipped = False
        self.vertices = []  # [[x, y, z]]
        self.polygons = []  # [MaxNodeMeshPolygon]
        self.is_dynamic = False
        self.is_trigger = False
        self.has_volume_light = False
        self.volume_light = None
        self.properties = MaxNodeMeshProperties()

    def setFlipped(self, is_flipped):
        self.is_flipped = is_flipped

    def addVertex(self, vertex):
        self.vertices.append(vertex)

    def addVertices(self, vertices):
        self.vertices = self.vertices + vertices

    def addPolygon(self, polygon):
        self.polygons.append(polygon)

    def getChildData(self):
        data = [
            packBool(self.is_flipped),
            packUInt(len(self.vertices))
        ]

        for vertex in self.vertices:
            vertices_chunk = MaxChunk(0, 1)
            vertices_data = [
                packDouble(vertex[0]),
                packDouble(vertex[1]),
                packDouble(vertex[2]),
            ]
            data = data + vertices_chunk.getBytes(vertices_data)

        data.append(packUInt(len(self.polygons)))
        for polygon in self.polygons:
            data = data + polygon.getBytes()

        data.append(packBool(self.is_dynamic))

        data = data + self.properties.getBytes()

        data.append(packBool(self.is_trigger))

        max_mesh_chunk2 = MaxChunk(0, 9)
        data = max_mesh_chunk2.getBytes(data)

        data.append(packBool(self.has_volume_light))
        max_mesh_chunk = MaxChunk(1, 0)

        return max_mesh_chunk.getBytes(data)
