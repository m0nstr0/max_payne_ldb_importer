from max_payne_sdk.max_type import parseType

class Texture:
    def __init__(self, id, name, file_type, file_size, data):
        self.name = name
        self.file_type = file_type
        self.file_size = file_size
        self.data = data
        self.id = id
    
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
    def __init__(self):
        self.textures = []
        self.lightmaps = []
    
    def addTexture(self, name, file_type, file_size, data):
        self.textures.append(Texture(len(self.textures), name, file_type, file_size, data))

    def numTextures(self):
        return len(self.textures)

    def getTextureById(self, id):
        if id < 0 or id >= self.numTextures():
            raise Exception("Texture not found with index %i" % id)
        return self.textures[id]

    def getTextureByName(self, name):
        for texture in self.textures:
            if texture.name == name:
                return texture
        raise Exception("Texture not found with name %s" % name)

    def numLightmaps(self):
        return len(self.lightmaps)

    def addLightMap(self, id, file_type, file_size, data):
        self.lightmaps.append(Texture(id, "lightmap_" + str(id), file_type, file_size, data))
   
    def getLightMapById(self, id):
        for lightmap in self.lightmaps:
            if lightmap.id == id:
                return lightmap
        raise Exception("Lightmap not found with id %i" % id)

class Material:
    def __init__(self, id, category_name, material_name, diffuse_texture, alpha_texture, has_alpha_test, has_adult_content):
        self.id = id
        self.category_name = category_name
        self.material_name = material_name
        self.diffuse_texture = diffuse_texture
        self.alpha_texture = alpha_texture
        self.has_alpha_test = has_alpha_test
        self.has_adult_content = has_adult_content

class MaterialContainer:
    def __init__(self):
        self.materials = []
    
    def addMaterial(self, id, category_name, material_name, diffuse_texture, alpha_texture, has_alpha_test, has_adult_content):
        self.materials.append(Material(id, category_name, material_name, diffuse_texture, alpha_texture, has_alpha_test, has_adult_content))

    def numMaterials(self):
        return len(self.materials)

    def getMaterialById(self, id):
        for material in self.materials:
            if id == material.id:
                return material
        raise Exception("Material not found with index %i" % id)

    def getMaterialByName(self, category_name, material_name):
        for material in self.materials:
            if material.material_name == material_name and material.category_name == category_name:
                return material
        raise Exception("Material not found with category %s and name %s" % (category_name, material_name))

class TextureVertex:
    def __init__(self, vertex_idx, uv, lightmap_uv, is_hidden):
        self.vertex_idx = vertex_idx
        self.uv = uv
        self.lightmap_uv = lightmap_uv
        self.is_hidden = is_hidden

class TexureVertexContainer:
    def __init__(self):
        self.vertices = []
        pass

    def addTextureVertex(self, vertex_idx, uv, lightmap_uv, is_hidden):
        self.vertices.append(TextureVertex(vertex_idx, uv, lightmap_uv, is_hidden))

    def numVertices(self):
        return len(self.vertices)

    def getVertexById(self, id):
        if id < 0 or id >= self.numVertices():
            raise Exception("Texture Vertex not found with index %i" % id)
        return self.vertices[id]

class VerticesContainer:
    def __init__(self):
        self.vertices = []
    
    def addVertex(self, vertex):
        self.vertices.append(vertex)

    def numVertices(self):
        return len(self.vertices)

    def getVertexById(self, id):
        if id < 0 or id >= self.numVertices():
            raise Exception("Vertex not found with index %i" % id)
        return self.vertices[id]

class Geometry:
    def __init__(self):
        self.vertices = []
        self.normals = []
        self.uvs = []
        self.lightmap_uvs = []

    def addPoint(self, vertex, normal, uv, lightmap_uv):
        self.vertices.append(vertex)
        self.normals.append(normal)
        self.uvs.append(uv)
        self.lightmap_uvs.append(lightmap_uv)

    def addMaterial(self, material):
        self.material = material

    def addLightMapTexture(self, lightmap):
        self.lightmap = lightmap

class Polygon:
    def __init__(self, texture_vertex_idx, num_vertices, material, lightmap):
        self.text_vertex_idx = texture_vertex_idx
        self.num_vertices = num_vertices
        self.material = material
        self.lightmap = lightmap
        self.geometry = Geometry()

    def build(self, vertices, normals, texture_vertices):
        for i in range(self.num_vertices):
            texture_vertex = texture_vertices.getVertexById(self.text_vertex_idx + i)
            self.geometry.addPoint(
                vertices.getVertexById(texture_vertex.vertex_idx),           
                normals.getVertexById(texture_vertex.vertex_idx),
                texture_vertex.uv,
                texture_vertex.lightmap_uv)
        self.geometry.addMaterial(self.material)
        self.geometry.addLightMapTexture(self.lightmap)

    def getGeometry(self):
        return self.geometry

class Room:
    def __init__(self, texture_vertices):
        self.vertices = VerticesContainer()
        self.normals = VerticesContainer()
        self.transform = None
        self.polygons = []
        self.texture_vertices = texture_vertices

    def addVertex(self, vertex):
        self.vertices.addVertex(vertex)

    def addNormal(self, normal):
        self.normals.addVertex(normal)

    def addTransform(self, transform):
        self.transform = transform

    def addPolygon(self, polygon):
        polygon.build(self.vertices, self.normals, self.texture_vertices)
        self.polygons.append(polygon)

    def numPolygons(self):
        return len(self.polygons)

    def getPolygonById(self, id):
        if id < 0 or id >= self.numPolygons():
            raise Exception("Polygon not found with index %i" % id)
        return self.polygons[id]

class RoomCointainer:
    def __init__(self):
        self.rooms = []
    
    def addRoom(self, room):
        self.rooms.append(room)

    def numRooms(self):
        return len(self.rooms)

    def getPolygonById(self, id):
        if id < 0 or id >= self.numRooms():
            raise Exception("Room not found with index %i" % id)
        return self.rooms[id]

class MaxLDB:
    #the block contains all the vertices from the level we don't need it
    def skipCollisionVerticesBlock(self, f):
        #Block header
        f.read(1)
        for i in range(parseType(f)):
            parseType(f)

    #the block contains all the polygons from the level we don't need it
    def skipCollisionPolygonsBlock(self, f):
        #Block header
        f.read(1)
        for i in range(parseType(f) * 6):
            parseType(f)

    #the block contains the collision hierarchy and some properties from the level we don't need it
    def skipCollisionHierarchyBlock(self, f):
        #Block header
        f.read(1)
        for i in range(parseType(f) * 8):
            parseType(f)
        #Block header
        f.read(1)
        for i in range(parseType(f)):
            parseType(f)

    #the block contains all the textures from the level
    def parseTextureBlock(self, f):
        #Block header
        parseType(f)
        for i in range(parseType(f)):
            file_name = parseType(f)
            file_type = parseType(f)
            file_size = parseType(f)
            self.textures.addTexture(
                file_name,
                file_type,
                file_size,
                f.read(file_size)
            )

    def parseMaterialsBlock(self, f):
        #Block header
        f.read(1)
        material_properties = []
        materials = []
        for i in range(parseType(f)):
            material_id = parseType(f)
            f.read(1)
            category_name = parseType(f)
            material_name = parseType(f)
            materials.append([category_name, material_name, i])

        #Block header
        f.read(1)
        for i in range(parseType(f)):
            f.read(1)
            category_name = parseType(f)
            material_name = parseType(f)
            material_id = parseType(f)

        for i in range(parseType(f)):
            category_name = parseType(f)
            for j in range(parseType(f)):
                material_name = parseType(f)

                diffuse_texture_name = parseType(f)
                diffuse_texture = None
                if diffuse_texture_name != "":
                    diffuse_texture = self.textures.getTextureByName(diffuse_texture_name)

                alpha_texture_name = parseType(f)
                alpha_texture = None
                if alpha_texture_name != "":
                    alpha_texture = self.textures.getTextureByName(alpha_texture_name)
                
                has_alpha_test = parseType(f)
                has_adult_content = parseType(f)
                material_properties.append([
                    category_name,
                    material_name,
                    diffuse_texture,
                    alpha_texture,
                    has_alpha_test,
                    has_adult_content
                ])

        for material in materials:
            for material_property in material_properties:
                if material[0] == material_property[0] and material[1] == material_property[1]:
                    self.materials.addMaterial(
                        material[2], 
                        material[0], 
                        material[1],
                        material_property[2],
                        material_property[3],
                        material_property[4],
                        material_property[5],
                        )
                    break

        for i in range(parseType(f)):
            lightmap_id = parseType(f)
            lightmap_file_type = parseType(f)
            lightmap_file_size = parseType(f)
            self.textures.addLightMap(
                lightmap_id,
                lightmap_file_type,
                lightmap_file_size,
                f.read(lightmap_file_size)
            )

    #the block contains the exits hierarchy (or visibility portals) and some properties we don't need it
    def skipExitsHierarchyBlock(self, f):
        for i in range(parseType(f)):
            parseType(f)
            for j in range(parseType(f)):
                parseType(f)
            for j in range(5):
                parseType(f)
            f.read(1)
            for j in range(parseType(f)):
                f.read(1)
                for k in range(parseType(f)):
                    parseType(f)

    def parseTexureVerticesBlock(self, f):
        #Block header
        f.read(1)
        for i in range(parseType(f)):
            vertex_idx = parseType(f)
            uv = parseType(f)
            lightmap_uv = parseType(f)
            parseType(f)
            is_hidden = parseType(f)
            self.texture_vertices.addTextureVertex(vertex_idx, uv, lightmap_uv, is_hidden)

    def parseRoomsBlock(self, f):
        for i in range(parseType(f)):
            polygons = []
            parseType(f)
            room = Room(self.texture_vertices)
            for j in range(parseType(f)):
                room.addVertex(parseType(f))
            f.read(1)
            for j in range(parseType(f)):
                room.addNormal(parseType(f))
            room.addTransform(parseType(f))
            for j in range(parseType(f)):
                parseType(f)
                texture_vertex_idx = parseType(f)
                num_vertices = parseType(f)
                normal = parseType(f)
                parseType(f)
                material = self.materials.getMaterialById(parseType(f))
                lightmap = self.textures.getLightMapById(parseType(f))
                for k in range(3):
                    parseType(f)
                room.addPolygon(Polygon(texture_vertex_idx, num_vertices, material, lightmap))
            f.read(1)
            for j in range(parseType(f) * 2):
                parseType(f)
            self.rooms.addRoom(room)

    def __init__(self, file_path):
        self.textures = TextureContainer()
        self.rooms = RoomCointainer()
        self.texture_vertices = TexureVertexContainer()
        self.materials = MaterialContainer()
        try:
            with open(file_path, "rb") as f:
                self.skipCollisionVerticesBlock(f)
                self.skipCollisionPolygonsBlock(f)
                self.skipCollisionHierarchyBlock(f)
                self.parseTextureBlock(f)
                self.parseMaterialsBlock(f)
                self.skipExitsHierarchyBlock(f)
                self.parseTexureVerticesBlock(f)
                self.parseRoomsBlock(f)
        except IOError:
            print('Error While Opening the file!', file_path)  
