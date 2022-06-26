import max_payne_sdk.max_type as max_type
import max_payne_sdk.max_kf2_type as kf2_type
import max_payne_sdk.max_kf2_reader as kf2_reader
import max_payne_sdk.max_kf2_reader.texture as kf2_texture
from dataclasses import dataclass

class MaterialChunkReaderV1(kf2_reader.KF2ReaderBase):
    def __parseTextureChunk(self, f):
        kf2_chunk = self.readChunk(f)
        if kf2_chunk.id != kf2_type.TEXTURE:
            raise ValueError("Unknown chunk id %s" % kf2_chunk.id.hex())
        if kf2_chunk.version == 1:
            return kf2_texture.TextureChunkReaderV1().parse(f)
        raise ValueError("Unknown texture chunk version %s" % kf2_chunk.version)

    def parse(self, f) -> kf2_type.MaterialV1:
        name = max_type.parseType(f)
        is_two_sided = max_type.parseType(f)
        is_fogging = max_type.parseType(f)
        is_diffuse_combined = max_type.parseType(f)
        is_invisible_geometry = max_type.parseType(f)
        material_name = max_type.parseType(f)     
        has_vertex_alpha = max_type.parseType(f)
        diffuse_color_type = max_type.parseType(f)
        specular_color_type = max_type.parseType(f)
        lit_type = max_type.parseType(f)
        ambient_color_r = max_type.parseType(f)
        ambient_color_g = max_type.parseType(f)
        ambient_color_b = max_type.parseType(f)
        ambient_color_a = max_type.parseType(f)
        diffuse_color_r = max_type.parseType(f)
        diffuse_color_g = max_type.parseType(f)
        diffuse_color_b = max_type.parseType(f)
        diffuse_color_a = max_type.parseType(f)
        specular_color_r = max_type.parseType(f)
        specular_color_g = max_type.parseType(f)
        specular_color_b = max_type.parseType(f)
        specular_color_a = max_type.parseType(f) 
        vertex_alpha = max_type.parseType(f) 
        sepecular_exponent = max_type.parseType(f) 
        diffuse_texture_type = max_type.parseType(f) 
        reflection_texture_type = max_type.parseType(f) 
        emboss_factor = max_type.parseType(f) 
        has_diffuse_texture = max_type.parseType(f)
        if (has_diffuse_texture > 0):
           diffuse_texture = self.__parseTextureChunk(f)
        has_reflection_texture = max_type.parseType(f)
        if (has_reflection_texture > 0):
            reflection_texture = self.__parseTextureChunk(f)
        has_bump_texture = max_type.parseType(f)
        if (has_bump_texture > 0):
            bump_texture = self.__parseTextureChunk(f)
        has_opacity_texture = max_type.parseType(f)
        if (has_opacity_texture > 0):
            opacity_texture = self.__parseTextureChunk(f)
        has_mask_texture = max_type.parseType(f)
        if (has_mask_texture > 0):
            mask_texture = self.__parseTextureChunk(f)
        mask_texture_type = max_type.parseType(f)
        has_lit = max_type.parseType(f)

class MaterialChunkReaderV2:
    def parse(self, f) -> kf2_type.MaterialV2:
        material_chunk_v1 = MaterialChunkReaderV1.parse(f)
        unk1 = max_type.parseType(f)
        unk2 = max_type.parseType(f) 
        unk3 = max_type.parseType(f)
        material_chunk_v2 = kf2_type.MaterialV2(**dataclass.asdict(material_chunk_v1), unk1, unk2, unk3)
        material_chunk_v2.version = 2
        return material_chunk_v2