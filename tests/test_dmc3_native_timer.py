"""Synthetic disk/decoder faults only; never opens game files or processes."""
import importlib.util
from pathlib import Path
import os
import struct
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
if os.environ.get("DMC3_STATIC_DECODER_PATH"):
    sys.path.insert(0, os.environ["DMC3_STATIC_DECODER_PATH"])
import inspect_dmc3_native_timer as native


class MappingTests(unittest.TestCase):
    def setUp(self):
        self.meta = dict(sections=[dict(rva=0x1000, raw_offset=0, raw_size=128,
                                       virtual_size=120, flags=0x20000000)])
        self.data = bytes(128)

    def test_virtual_tail_not_file_code(self):
        with self.assertRaises(ValueError):
            native.rva_bytes(self.meta, self.data, 0x1078, 1, executable=True)

    def test_nonexecuting_section_refused(self):
        self.meta["sections"][0]["flags"] = 0
        with self.assertRaises(ValueError):
            native.rva_bytes(self.meta, self.data, 0x1000, 1, executable=True)

    def test_partial_disk_range_refused(self):
        with self.assertRaises(ValueError):
            native.rva_bytes(self.meta, b"", 0x1000, 2)

    def test_ambiguous_mapping_refused(self):
        self.meta["sections"] *= 2
        with self.assertRaises(ValueError):
            native.rva_bytes(self.meta, self.data, 0x1000, 2)

    def test_unknown_build_precedes_rva_access(self):
        with self.assertRaisesRegex(ValueError, "Different build"):
            native.require_build_and_anchors({"sha256": "unknown"}, None)

    def test_source_anchor_mismatch_refused(self):
        self.meta["sha256"] = native.BUILD_SHA256  # Synthetic metadata, not a hash collision.
        with patch.object(native, "ANCHORS", [(0x1000, 2, "not-the-fixture-hash")]):
            with self.assertRaisesRegex(ValueError, "source anchor differs"):
                native.require_build_and_anchors(self.meta, self.data)

    def test_missing_exception_directory(self):
        with self.assertRaisesRegex(ValueError, "Missing exception"):
            native.runtime_ranges(dict(pe_offset=0), b"")

    def test_bad_exception_size(self):
        data = bytearray(256)
        struct.pack_into("<II", data, 24 + 112 + 24, 0x1000, 13)
        with self.assertRaisesRegex(ValueError, "Invalid bounded"):
            native.runtime_ranges(dict(pe_offset=0), data)


@unittest.skipUnless(importlib.util.find_spec("capstone"), "Requires optional isolated Capstone")
class DecoderTests(unittest.TestCase):
    def decode(self, hexcode):
        import capstone
        return native.decode_range(bytes.fromhex(hexcode), 0x1000, capstone)

    def test_immediate_bytes_are_not_memory_operand(self):
        refs, complete = self.decode("b8343e0000c3")
        self.assertTrue(complete)
        self.assertEqual(refs, [])

    def test_unreachable_bytes_do_not_become_reachable(self):
        refs, complete = self.decode("eb08f30f1183343e0000c3")
        self.assertTrue(complete)
        self.assertEqual(len(refs), 1)
        self.assertFalse(refs[0]["locally_reachable"])

    def test_negative_immediate_is_preserved_not_validated(self):
        refs, complete = self.decode("c783343e0000000080bfc3")
        self.assertTrue(complete)
        self.assertEqual(refs[0]["immediate_low32_float"], -1.0)
        self.assertFalse(refs[0]["actor_provenance_verified"])
        self.assertTrue(refs[0]["locally_reachable"])

    def test_incomplete_decode_flag(self):
        refs, complete = self.decode("f30f1183343e00000f")
        self.assertFalse(complete)
        self.assertFalse(refs[0]["linear_range_complete"])

    def test_operand_width_retained(self):
        refs, _ = self.decode("48c783343e00000000803fc3")
        self.assertEqual(refs[0]["memory_operands"][0]["size"], 8)


if __name__ == "__main__":
    unittest.main()
