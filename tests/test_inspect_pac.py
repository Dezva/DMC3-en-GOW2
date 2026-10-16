import hashlib
import json
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import unittest

from tools.inspect_pac import PacError, analyze, dds_info, slots


def pac(*entries):
    offset = 8 + 4 * len(entries)
    offsets = []
    payload = bytearray()
    for entry in entries:
        if entry is None:
            offsets.append(0)
        else:
            offsets.append(offset)
            payload.extend(entry)
            offset += len(entry)
    return b"PAC\0" + struct.pack("<I", len(entries)) + struct.pack(f"<{len(entries)}I", *offsets) + payload


def dds(width=4, height=4, levels=1):
    header = bytearray(128)
    header[:4] = b"DDS "
    struct.pack_into("<7I", header, 4, 124, 0xA1007, height, width, 16, 0, levels)
    struct.pack_into("<II", header, 76, 32, 4)
    header[84:88] = b"DXT5"
    size = sum(max(1, (max(1, width >> i) + 3) // 4)
               * max(1, (max(1, height >> i) + 3) // 4) * 16 for i in range(levels))
    return bytes(header) + b"\x42" * size


class PacTests(unittest.TestCase):
    def test_extract_dds_exactly_without_padding(self):
        image = dds(8, 4, 4)
        model = b"MOD " + bytes(128)
        source = pac(b"metadata" + image + b"\0" * 16, model)
        report, files = analyze(source)
        self.assertEqual(files["texture_000.dds"], image)
        self.assertEqual(files["slot_001.mod"], model)
        self.assertEqual(report["textures"][0]["mip_levels"], 4)
        self.assertEqual(report["source_sha256"], hashlib.sha256(source).hexdigest())

    def test_sparse_and_nested_relative_offsets(self):
        nested = pac(None, b"MODEL")
        source = pac(None, nested)
        report, files = analyze(source)
        self.assertTrue(report["blocks"][0]["absent"])
        self.assertEqual(report["blocks"][1]["nested_present_count"], 1)
        self.assertEqual(files["slot_001.pac"], nested)

    def test_bad_offsets_and_count(self):
        for source in (b"PAC\0" + struct.pack("<I", 100),
                       b"PAC\0" + struct.pack("<II", 1, 4),
                       b"PAC\0" + struct.pack("<III", 2, 16, 16) + b"abcd",
                       b"PAC\0" + struct.pack("<II", 1, 999)):
            with self.subTest(source=source), self.assertRaises(PacError):
                slots(source)

    def test_reject_truncated_mips(self):
        image = dds()[:-1]
        with self.assertRaisesRegex(PacError, "exceeds"):
            analyze(pac(image))

    def test_reject_unsupported_dds_and_mip_count(self):
        for offset, replacement in ((84, b"DX10"), (28, struct.pack("<I", 99)),
                                    (112, struct.pack("<I", 0x200))):
            image = bytearray(dds())
            image[offset:offset + 4] = replacement
            with self.subTest(offset=offset), self.assertRaises(PacError):
                dds_info(image, 0, len(image))

    def test_ignore_magic_string_without_dds_header(self):
        report, _ = analyze(pac(b"text containing DDS is not a texture: DDS "))
        self.assertEqual(report["textures"], [])

    def test_cli_manifest_output_and_no_overwrite(self):
        script = Path(__file__).resolve().parents[1] / "tools" / "inspect_pac.py"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = pac(dds(), b"MOD " + bytes(16))
            original = root / "original.pac"
            original.write_bytes(source)
            manifest = root / "informe.json"
            manifest.write_text(json.dumps({"Bytes": len(source),
                                           "SHA256": hashlib.sha256(source).hexdigest().upper()}))
            out = root / "output"
            command = [sys.executable, str(script), str(original), "--manifest", str(manifest),
                       "--output", str(out)]
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual((out / "texture_000.dds").read_bytes(), dds())
            saved_report = (out / "pac-report.json").read_bytes()
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(saved_report, (out / "pac-report.json").read_bytes())
            self.assertEqual(original.read_bytes(), source)

    def test_manifest_mismatch_fails_before_creating_output(self):
        script = Path(__file__).resolve().parents[1] / "tools" / "inspect_pac.py"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.pac"
            source.write_bytes(pac(dds()))
            manifest = root / "informe.json"
            manifest.write_text(json.dumps({"Bytes": source.stat().st_size, "SHA256": "wrong"}))
            out = root / "output"
            result = subprocess.run([sys.executable, str(script), str(source), "--manifest", str(manifest),
                                     "--output", str(out)], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("manifest", result.stderr)
            self.assertFalse(out.exists())


if __name__ == "__main__":
    unittest.main()
