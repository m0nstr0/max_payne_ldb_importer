import importlib.util
from pathlib import Path
import struct
import unittest
from max_payne_sdk.binary import FormatError

spec = importlib.util.spec_from_file_location(
    "helper_audit", Path(__file__).resolve().parents[1] / "tools/audit_helpers.py")
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


def chunk(ident, version, payload):
    return b"\x0c" + struct.pack("<III", ident, version, len(payload) + 13) + payload


def string(raw):
    return b"\x0d\x02" + struct.pack("<i", len(raw)) + raw


def helper(name=b"SyntheticClass", version=1):
    node = (string(b"HelperNode") + string(b"Parent") + b"\x1a"
            + struct.pack("<12f", 1, 0, 0, 0, 1, 0, 0, 0, 1, 10, 20, 30)
            + b"\x0e\x01" + (string(b"user data") if version else b""))
    return chunk(0x10016, 0, chunk(0x10000, version, node) + string(name))


class HelperAuditTests(unittest.TestCase):
    def test_helper_found_and_class_bytes_preserved(self):
        for version in (0, 1):
            found = audit.helpers_in_bytes(helper(b"\xffClass", version))
            self.assertEqual(1, len(found))
            self.assertEqual("ff436c617373", found[0]["className_hex"])
            self.assertEqual("HelperNode", found[0]["node"]["name"])
            self.assertEqual(version, found[0]["node"]["version"])
            self.assertEqual("", found[0]["trailing_hex"])

    def test_nested_offset_and_opaque_false_positive(self):
        raw = helper()
        self.assertEqual([], audit.helpers_in_bytes(chunk(0x77777, 0, raw)))
        found = audit.helpers_in_bytes(chunk(0x10005, 2, raw))
        self.assertEqual(13, found[0]["offset"])
        self.assertEqual(1, found[0]["depth"])

    def test_bad_chunk_bounds(self):
        for data in (b"", helper()[:-1], b"\x0c", b"\x0c" + struct.pack("<III", 0x10016, 0, 12)):
            with self.subTest(data=data), self.assertRaises(FormatError):
                audit.helpers_in_bytes(data)

    def test_class_name_cannot_cross_helper_boundary(self):
        raw = helper()
        malformed = bytearray(raw)
        offset = raw.index(string(b"SyntheticClass"))
        malformed[offset + 2:offset + 6] = struct.pack("<i", 1000)
        with self.assertRaises(FormatError):
            audit.helpers_in_bytes(bytes(malformed) + chunk(0x77777, 0, b"x" * 1000))
