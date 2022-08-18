import max_payne_sdk.max_type as max_type
import max_payne_sdk.max_kf2_type as kf2_type
import max_payne_sdk.max_kf2_reader as kf2_reader
import max_payne_sdk.max_kf2_reader.material_reader.texture as kf2_texture


class MaterialChunkReader(kf2_reader.KF2ReaderBase):
    def getAllowedVersions(self):
        return [0, 1, 2]

    def parse(self, f, kf2_chunk: kf2_type.KF2ChunkHeader):
        name = max_type.parseType(f)
        is_two_sided = max_type.parseType(f)
        is_fogging = max_type.parseType(f)
        is_diffuse_combined = max_type.parseType(f)
        is_invisible_geometry = max_type.parseType(f)
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
        specular_exponent = max_type.parseType(f)
        diffuse_texture_type = max_type.parseType(f)
        reflection_texture_type = max_type.parseType(f)
        emboss_factor = max_type.parseType(f)

        has_diffuse_texture = max_type.parseType(f)
        diffuse_texture = None
        if has_diffuse_texture > 0:
            kf2_texture_chunk = self.readChunk(f)
            diffuse_texture = kf2_texture.TextureChunkReader().create(f, kf2_type.TEXTURE, kf2_texture_chunk)

        has_reflection_texture = max_type.parseType(f)
        reflection_texture = None
        if has_reflection_texture > 0:
            kf2_texture_chunk = self.readChunk(f)
            reflection_texture = kf2_texture.TextureChunkReader().create(f, kf2_type.TEXTURE, kf2_texture_chunk)

        has_bump_texture = max_type.parseType(f)
        bump_texture = None
        if has_bump_texture > 0:
            kf2_texture_chunk = self.readChunk(f)
            bump_texture = kf2_texture.TextureChunkReader().create(f, kf2_type.TEXTURE, kf2_texture_chunk)

        has_opacity_texture = max_type.parseType(f)
        opacity_texture = None
        if has_bump_texture > 0:
            kf2_texture_chunk = self.readChunk(f)
            opacity_texture = kf2_texture.TextureChunkReader().create(f, kf2_type.TEXTURE, kf2_texture_chunk)

        #version 1
        has_mask_texture = max_type.parseType(f) if kf2_chunk.version > 0 else 0
        mask_texture = None
        if has_mask_texture > 0:
            kf2_texture_chunk = self.readChunk(f)
            mask_texture = kf2_texture.TextureChunkReader().create(f, kf2_type.TEXTURE, kf2_texture_chunk)

        mask_texture_type = max_type.parseType(f) if kf2_chunk.version > 0 else 0x00
        has_lit = max_type.parseType(f) if kf2_chunk.version > 0 else False

        #version 2
        unk1 = max_type.parseType(f) if kf2_chunk.version > 1 else None
        unk2 = max_type.parseType(f) if kf2_chunk.version > 1 else None
        unk3 = max_type.parseType(f) if kf2_chunk.version > 1 else None

        return kf2_type.Material(
            kf2_chunk.version,
            name,
            is_two_sided,
            is_fogging,
            is_diffuse_combined,
            is_invisible_geometry,
            has_vertex_alpha,
            has_diffuse_texture,
            has_reflection_texture,
            has_bump_texture,
            has_opacity_texture,
            has_mask_texture,
            has_lit,
            diffuse_color_type,
            specular_color_type,
            lit_type,
            mask_texture_type,
            diffuse_texture_type,
            reflection_texture_type,
            ambient_color_r,
            ambient_color_g,
            ambient_color_b,
            ambient_color_a,
            diffuse_color_r,
            diffuse_color_g,
            diffuse_color_b,
            diffuse_color_a,
            specular_color_r,
            specular_color_g,
            specular_color_b,
            specular_color_a,
            vertex_alpha,
            specular_exponent,
            emboss_factor,
            diffuse_texture,
            reflection_texture,
            bump_texture,
            opacity_texture,
            mask_texture,
            unk1,
            unk2,
            unk3)
