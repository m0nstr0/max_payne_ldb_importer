import io
import struct
import tempfile
import unittest
from pathlib import Path

from max_payne_sdk import max_type
from max_payne_sdk.binary import FormatError
from max_payne_sdk.max_kf2 import MaxKF2Reader
from max_payne_sdk.max_kf2_reader import KF2ReaderBase
from max_payne_sdk.max_kf2_reader.material_reader.material import MaterialChunkReader
from max_payne_sdk.max_kf2_reader.material_reader.material_list import MaterialListChunkReader
from max_payne_sdk.max_kf2_reader.camera_reader.camera import CameraChunkReader
from max_payne_sdk.max_kf2_type import KF2ChunkHeader, SkinVertex
from max_payne_sdk.max_ldb import MaxLDBReader
from max_payne_sdk.max_ldb2 import MaxLDBReader2
from max_payne_sdk.max_ldb_factory import MaxLBDReaderFactory
from max_payne_sdk.file_types import has_extension
from max_payne_maya.skin_weights import dense_weights


def integer(value):
    return b'\x02' + struct.pack('<i', value)


def string(value):
    data = value.encode('latin-1')
    return b'\x0d' + integer(len(data)) + data


def scalar(value):
    return b'\x09' + struct.pack('<f', value)


def chunk(ident, version, data):
    return b'\x0c' + struct.pack('<III', ident, version, len(data) + 13) + data


def vector(values):
    return b'\x1c' + integer(len(values)) + b''.join(values)


def skin_v1(offset=0, count=2, bone=1, marker=b'\x1c'):
    arrays = [[string('mesh')], [string('a'), string('b')], [integer(offset)],
              [integer(count)], [integer(bone), integer(0)], [scalar(.25), scalar(.75)],
              [b'\x03' + struct.pack('<I', 1)], [b'\x03' + struct.pack('<I', 0)]]
    payload = b''.join(vector(values) for values in arrays)
    return chunk(0x10014, 1, marker + payload[1:])


class ReaderTests(unittest.TestCase):
    def parse(self, data):
        with tempfile.TemporaryDirectory(dir=Path.cwd()) as directory:
            path = Path(directory) / 'input.kf2'
            path.write_bytes(data)
            return MaxKF2Reader().parse(path)

    def test_signed_and_unsigned_widths(self):
        for tag, width, signed in ((2, 4, True), (0x12, 3, True), (0x13, 2, True),
                                  (0x14, 1, True), (3, 4, False), (15, 3, False),
                                  (16, 2, False), (17, 1, False)):
            value = -2 if signed else 2 ** (width * 8) - 1
            with self.subTest(tag=tag):
                self.assertEqual(value, max_type.parseType(io.BytesIO(
                    bytes([tag]) + value.to_bytes(width, 'little', signed=signed))))

    def test_truncated_scalars(self):
        for data in (b'', b'\x02\x01', b'\x12\x01', b'\x09\x00', b'\x16\x00'):
            with self.subTest(data=data), self.assertRaises(FormatError):
                max_type.parseType(io.BytesIO(data))

    def test_non_utf8_name_is_reversible(self):
        self.assertEqual('caf\xe9', max_type.parseType(io.BytesIO(string('caf\xe9'))))

    def test_invalid_string_lengths(self):
        for data in (b'\x0d' + integer(-1), b'\x0d\x09' + struct.pack('<f', 2),
                     b'\x0d' + integer(3) + b'ab'):
            with self.subTest(data=data), self.assertRaises(FormatError):
                max_type.parseType(io.BytesIO(data))

    def test_unknown_tag_has_offset(self):
        with self.assertRaisesRegex(FormatError, '0x0'):
            max_type.parseType(io.BytesIO(b'\xff'))

    def test_chunk_header_and_size_validation(self):
        for data in (b'\x0c', b'\x0c' + struct.pack('<III', 7, 0, 12),
                     chunk(0x999, 0, b'a')[:-1], b'wrong', b''):
            with self.subTest(data=data), self.assertRaises(FormatError):
                self.parse(data)

    def test_skipped_payload_does_not_desynchronize(self):
        raw = b'\x0c\xff\x00\x0c'
        model = self.parse(chunk(0x10002, 0, raw) + skin_v1())
        self.assertEqual(raw, model.unknown_chunks[0][1])
        self.assertEqual(1, model.numSkins())

    def test_nested_chunks_are_bounded_and_unknown_children_retained(self):
        model = self.parse(chunk(0x10005, 1, chunk(0x999, 9, b'opaque')) + skin_v1())
        self.assertEqual(b'opaque', model.meshes[0].unknown_chunks[0][1])
        self.assertEqual(1, model.numSkins())
        bad_child = b'\x0c' + struct.pack('<III', 0x999, 0, 100)
        with self.assertRaises(FormatError):
            self.parse(chunk(0x10005, 1, bad_child) + skin_v1())

    def test_known_chunk_cannot_consume_next_sibling(self):
        with self.assertRaises(FormatError):
            self.parse(chunk(0x10014, 1, b'\x1c') + skin_v1())

    def test_unknown_known_version_is_rejected(self):
        with self.assertRaisesRegex(FormatError, 'version 99'):
            self.parse(chunk(0x10014, 99, b''))

    def test_skin_v1_offsets_and_primitive_arrays(self):
        skin = self.parse(skin_v1()).skins[0]
        self.assertEqual([1, 0], skin.skin_vertices[0].vertex_bone_indices)
        self.assertEqual([.25, .75], skin.skin_vertices[0].vertex_weights)
        self.assertEqual([1], skin.primitive_vertex_counts)
        self.assertEqual([0], skin.primitive_vertex_offsets)

    def test_skin_v1_rejects_bad_ranges_bones_and_markers(self):
        for data in (skin_v1(offset=-1), skin_v1(count=3), skin_v1(bone=2),
                     skin_v1(marker=b'\x00')):
            with self.subTest(data=data), self.assertRaises(FormatError):
                self.parse(data)

    def test_skin_v0_aggregates_three_lists_and_retains_vectors(self):
        payload = (integer(1) + integer(4) + integer(0) + scalar(.25)
                   + integer(1) + integer(4) + integer(1) + scalar(.75)
                   + integer(0) + integer(1) + string('mesh')
                   + integer(2) + string('a') + string('b')
                   + integer(1) + b'\x16' + struct.pack('<fff', 1, 2, 3))
        skin = self.parse(chunk(0x10014, 0, payload)).skins[0]
        self.assertEqual([4], [vertex.vertex_index for vertex in skin.skin_vertices])
        self.assertEqual([0, 1], skin.skin_vertices[0].vertex_bone_indices)
        self.assertEqual([[1, 2, 3]], skin.legacy_vertex_vectors)

    def test_negative_skin_count(self):
        with self.assertRaises(FormatError):
            self.parse(chunk(0x10014, 0, integer(-1)))

    def test_mesh_v0_and_degenerate_triangle(self):
        geometry = chunk(0x10006, 0, integer(1) + b'\x16' + struct.pack('<fff', 0, 0, 0))
        polygon = chunk(0x10008, 0, integer(3) + integer(0) * 3)
        polygons = chunk(0x10007, 0, integer(1) + polygon + integer(0) * 2)
        for version in (0, 1):
            model = self.parse(chunk(0x10005, version, geometry + polygons))
            self.assertEqual([0, 0, 0], model.meshes[0].polygons.polygons_indices)

    def test_material_opacity_independent_of_bump(self):
        texture = chunk(0x10011, 1, string('tex') + integer(1) + integer(0)
                        + integer(1) + string('texture.dds'))
        for bump, opacity in ((0, 1), (1, 0), (1, 1), (0, 0)):
            # 5 flags + 3 enums precede the 15 scalar fields.
            payload = (string('mat') + integer(0) * 8 + scalar(1) * 14
                       + integer(0) * 2 + scalar(0) + integer(0) * 2
                       + integer(bump) + (texture if bump else b'')
                       + integer(opacity) + (texture if opacity else b''))
            header = KF2ChunkHeader(0x10010, 0, 13 + len(payload))
            with self.subTest(bump=bump, opacity=opacity):
                material = MaterialChunkReader().create(io.BytesIO(payload), header.id, header)
                self.assertEqual(bool(opacity), material.opacity_texture is not None)
                self.assertEqual(bool(bump), material.bump_texture is not None)

    def test_material_list_keeps_container_version(self):
        # Empty list is a valid v0 container too.
        payload = string('textures') + integer(0)
        result = MaterialListChunkReader().create(io.BytesIO(payload), 0x1000f,
                                                  KF2ChunkHeader(0x1000f, 0, 13 + len(payload)))
        self.assertEqual(0, result.version)

    def test_camera_keeps_container_version(self):
        node = chunk(0x10000, 1, string('camera') + string('')
                     + b'\x1a' + struct.pack('<12f', *([0] * 12)) + b'\x0e\x00' + string(''))
        payload = node + scalar(1) + scalar(.1) + scalar(100)
        camera = CameraChunkReader().create(io.BytesIO(payload), 0x10001,
                                             KF2ChunkHeader(0x10001, 0, 13 + len(payload)))
        self.assertEqual(0, camera.version)
        self.assertEqual(1, camera.node.version)

    def test_io_errors_are_not_suppressed(self):
        for reader in (MaxKF2Reader(), MaxLDBReader('missing.ldb'), MaxLDBReader2('missing.ldb')):
            with self.subTest(reader=reader), self.assertRaises(OSError):
                reader.parse('missing.kf2') if isinstance(reader, MaxKF2Reader) else reader.parse()

    def test_ldb2_header_validation(self):
        for data in (b'BAD!' + integer(34), b'LDB2' + integer(33), b'LD'):
            with self.subTest(data=data), self.assertRaises(ValueError):
                MaxLDBReader2('unused').parseHeader(io.BytesIO(data))

    def test_string_pool_checks(self):
        reader = MaxLDBReader2('unused')
        reader.stringTable = b'ok\x00bad'
        self.assertEqual('ok', reader.getStringFromStringTable(0))
        self.assertEqual('', reader.getStringFromStringTable(-1))
        for index in (-2, 6, 3):
            with self.subTest(index=index), self.assertRaises(FormatError):
                reader.getStringFromStringTable(index)

    def test_translator_extensions_do_not_claim_other_formats(self):
        self.assertTrue(has_extension('MODEL.KFS', {'kf2', 'kfs', 'skd'}))
        self.assertFalse(has_extension('scene.ma', {'ldb'}))

    def test_ldb2_unsigned_render_indices(self):
        # Raw indices use all 16 bits, independently of tagged scalar signedness.
        payload = (integer(1) + integer(0) * 3 + integer(1) + integer(0)
                   + struct.pack('<HHH', 32768, 40000, 65535))
        mesh = MaxLDBReader2('unused').parseRoomStaticMesh(io.BytesIO(payload))
        self.assertEqual([32768, 40000, 65535], mesh.static_meshes[0].indices)

    def test_ldb2_prefab_render_flag_is_independent_of_lightmaps(self):
        def header(lightmaps, unique, midpoint):
            return (integer(0) + integer(lightmaps) + integer(0) * 8
                    + integer(7) + integer(unique)
                    + (b'\x16' + struct.pack('<fff', midpoint, 0, 0)) * 3)

        for lightmaps in (0, 1):
            for unique in (0, 1):
                payload = (integer(2) + header(0, 0, 1) + integer(0) * 3
                           + header(lightmaps, unique, 2)
                           + (integer(0) if unique else b'') + integer(0))
                stream = io.BytesIO(payload)
                reader = MaxLDBReader2('unused')
                with self.subTest(lightmaps=lightmaps, unique=unique):
                    reader.parseDynamicMeshes(stream)
                    self.assertEqual(len(payload), stream.tell())
                    first, second = reader.ldb.getDynamicMeshes().dynamic_meshes
                    self.assertIs(first.collision, second.collision)
                    self.assertEqual(first.mesh is second.mesh, not unique)
                    self.assertIsNot(first.aabb, second.aabb)

    def test_dense_weights_reordered_influences(self):
        vertex = SkinVertex(0, [4, 1, 4], [.2, .5, .3])
        self.assertEqual([.5, 0, .5], dense_weights(vertex, {4: 2, 1: 0, 7: 1}, 3))
        with self.assertRaises(ValueError):
            dense_weights(vertex, {4: 0}, 1)


if __name__ == '__main__':
    unittest.main()
