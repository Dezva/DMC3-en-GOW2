import json
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import unittest

from tools.inspect_gow_toc import TocError, parse_toc, resolve, root_paks


def toc(*files):
    entries, offsets = bytearray(), []
    for name, size, sectors in files:
        entries += struct.pack("<24sIII", name.encode(), size, len(sectors), len(offsets))
        offsets.extend(sectors)
    return struct.pack("<I", len(files)) + entries + struct.pack(f"<{len(offsets)}I", *offsets)


class TocTests(unittest.TestCase):
    def test_parse_indexed_occurrences_and_iso_offsets(self):
        data = toc(("R_HERO00.WAD", 100, [2, 10000003]), ("R_HERO01.WAD", 200, [1]))
        report = resolve(parse_toc(data), {1: {"sector": 100, "bytes": 10000},
                                           2: {"sector": 1000, "bytes": 10000}})
        self.assertEqual(report["file_count"], 2)
        self.assertEqual(report["encounter_count"], 3)
        self.assertEqual(report["unused_offset_slots"], 0)
        self.assertEqual(report["addressing"], "indexed")
        self.assertEqual(report["entries"][0]["locations"][0]["iso_offset"], 102 * 2048)
        self.assertEqual(report["entries"][0]["locations"][1]["iso_offset"], 1003 * 2048)

    def test_absolute_addressing_across_available_paks(self):
        report = resolve(parse_toc(toc(("TEST.WAD", 32, [5]))),
                         {1: {"sector": 50, "bytes": 8192}, 2: {"sector": 100, "bytes": 8192}})
        location = report["entries"][0]["locations"][0]
        self.assertEqual(report["addressing"], "absolute")
        self.assertEqual(location["pak"], "PART2.PAK")
        self.assertEqual(location["iso_offset"], 101 * 2048)

    def test_missing_pak_or_out_of_bounds_stays_unresolved(self):
        report = resolve(parse_toc(toc(("TEST.WAD", 100, [10000001, 3]))),
                         {1: {"sector": 100, "bytes": 4096}})
        self.assertTrue(all(loc["iso_offset"] is None for loc in report["entries"][0]["locations"]))

    def test_bad_tables(self):
        valid = toc(("TEST.WAD", 100, [1]))
        broken_range = bytearray(valid)
        struct.pack_into("<I", broken_range, 4 + 32, 1)
        for data in (b"", struct.pack("<I", 1000), valid[:-1], bytes(broken_range)):
            with self.subTest(data=data), self.assertRaises(TocError):
                parse_toc(data)

    def test_unsafe_and_duplicate_names(self):
        for data in (toc(("../x.WAD", 100, [1])),
                     toc(("X.WAD", 100, [1]), ("x.wad", 100, [2]))):
            with self.subTest(data=data), self.assertRaises(TocError):
                parse_toc(data)

    def test_root_metadata_validation(self):
        row = {"Name": "PART1.PAK", "Sector": "100", "Bytes": "4096", "Directory": "False"}
        self.assertEqual(root_paks([row])[1]["sector"], 100)
        with self.assertRaises(TocError):
            root_paks([row, row])
        with self.assertRaises(TocError):
            root_paks([{**row, "Directory": "True"}])

    def test_cli_report_and_manifest_failure(self):
        script = Path(__file__).resolve().parents[1] / "tools" / "inspect_gow_toc.py"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "GODOFWAR.TOC"
            data = toc(("R_HERO00.WAD", 100, [1]))
            path.write_bytes(data)
            result = subprocess.run([sys.executable, str(script), str(path)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual(report["sample_candidates"][0]["name"], "R_HERO00.WAD")
            manifest = root / "informe.json"
            manifest.write_text(json.dumps({"IndexBytes": len(data), "IndexSHA256": report["sha256"]}))
            command = [sys.executable, str(script), str(path), "--manifest", str(manifest)]
            self.assertEqual(subprocess.run(command, capture_output=True).returncode, 0)
            manifest.write_text(json.dumps({"IndexBytes": len(data), "IndexSHA256": "wrong"}))
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(result.stdout, "")
            self.assertEqual(path.read_bytes(), data)


if __name__ == "__main__":
    unittest.main()
