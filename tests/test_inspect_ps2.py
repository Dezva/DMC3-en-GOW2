import hashlib
import io
import json
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import unittest

from tools.inspect_ps2 import Disc, DiscError, SECTOR


def both32(value):
    return struct.pack("<I", value) + struct.pack(">I", value)


def record(name, sector, length, flags=0):
    size = 33 + len(name) + (len(name) % 2 == 0)
    data = bytearray(size)
    data[0] = size
    data[2:10] = both32(sector)
    data[10:18] = both32(length)
    data[25] = flags
    data[28:32] = b"\x01\x00\x00\x01"
    data[32] = len(name)
    data[33:33 + len(name)] = name
    return data


def fixture(nested=False):
    """Construct only ISO metadata, a boot config and a synthetic ELF header."""
    image = bytearray(SECTOR * 32)
    primary = bytearray(SECTOR)
    primary[:7] = b"\x01CD001\x01"
    primary[40:72] = b"SYNTHETIC_TEST".ljust(32)
    primary[80:88] = both32(32)
    primary[128:132] = struct.pack("<H", SECTOR) + struct.pack(">H", SECTOR)
    primary[156:190] = record(b"\0", 20, SECTOR, 2)
    image[16 * SECTOR:17 * SECTOR] = primary
    image[17 * SECTOR:17 * SECTOR + 7] = b"\xffCD001\x01"
    boot = b"BIN\\TEST_123.45;1" if nested else b"TEST_123.45;1"
    cnf = b"BOOT2 = cdrom0:\\" + boot + b"\r\nVER = 1.00\r\n"
    elf = bytearray(52)
    elf[:7] = b"\x7fELF\x01\x01\x01"
    struct.pack_into("<HHII", elf, 16, 2, 8, 1, 0x100000)
    directory = record(b"\0", 20, SECTOR, 2) + record(b"\1", 20, SECTOR, 2)
    directory += record(b"SYSTEM.CNF;1", 21, len(cnf))
    executable = record(b"TEST_123.45;1", 22, len(elf))
    if nested:
        directory += record(b"BIN", 23, SECTOR, 2)
        image[23 * SECTOR:23 * SECTOR + len(executable)] = executable
    else:
        directory += executable
    image[20 * SECTOR:20 * SECTOR + len(directory)] = directory
    image[21 * SECTOR:21 * SECTOR + len(cnf)] = cnf
    image[22 * SECTOR:22 * SECTOR + len(elf)] = elf
    return image, elf


class InspectTests(unittest.TestCase):
    def test_identity_and_read_only_behavior(self):
        image, elf = fixture()
        stream = io.BytesIO(image)
        result = Disc(stream).report()
        self.assertEqual(result["volume_label"], "SYNTHETIC_TEST")
        self.assertEqual(result["disc_serial"], "TEST-12345")
        self.assertEqual(result["elf_entry_address"], "0x00100000")
        self.assertEqual(result["elf_sha256"], hashlib.sha256(elf).hexdigest())
        self.assertEqual(stream.getvalue(), bytes(image))

    def test_nested_boot_path(self):
        image, _ = fixture(nested=True)
        self.assertEqual(Disc(io.BytesIO(image)).report()["disc_serial"], "TEST-12345")

    def test_truncated_image(self):
        image, _ = fixture()
        with self.assertRaisesRegex(DiscError, "truncada"):
            Disc(io.BytesIO(image[:-SECTOR]))

    def test_inconsistent_extent(self):
        image, _ = fixture()
        image[16 * SECTOR + 80:16 * SECTOR + 84] = struct.pack("<I", 31)
        with self.assertRaisesRegex(DiscError, "inconsistente"):
            Disc(io.BytesIO(image))

    def test_missing_boot_executable(self):
        image, _ = fixture()
        image = image.replace(b"cdrom0:\\TEST", b"cdrom0:\\LOST")
        with self.assertRaisesRegex(DiscError, "ausente"):
            Disc(io.BytesIO(image)).report()

    def test_wrong_elf_machine(self):
        image, _ = fixture()
        struct.pack_into("<H", image, 22 * SECTOR + 18, 62)
        with self.assertRaisesRegex(DiscError, "MIPS"):
            Disc(io.BytesIO(image)).report()

    def test_cli_and_file_unchanged(self):
        image, _ = fixture()
        script = Path(__file__).resolve().parents[1] / "tools" / "inspect_ps2.py"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "test.iso"
            path.write_bytes(image)
            result = subprocess.run([sys.executable, str(script), str(path)],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["disc_serial"], "TEST-12345")
            self.assertEqual(path.read_bytes(), bytes(image))
            path.write_bytes(b"not an ISO")
            result = subprocess.run([sys.executable, str(script), str(path)],
                                    capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(result.stdout, "")
            self.assertIn("Error:", result.stderr)


if __name__ == "__main__":
    unittest.main()
