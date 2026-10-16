"""Exercise the actual PowerShell client against synthetic ISO/PE and TCP PINE.

Windows runtime and game behaviour are intentionally not simulated as successes.
Set PWSH_BIN to a verified portable pwsh if it is not already on PATH.
"""
import hashlib
import json
import os
from pathlib import Path
import shutil
import socket
import struct
import subprocess
import tempfile
import threading
import time
import unittest

from test_inspect_ps2 import SECTOR, fixture, record


ROOT = Path(__file__).resolve().parents[1]
PWSH = os.environ.get("PWSH_BIN") or shutil.which("pwsh") or shutil.which("powershell")
INSTRUCTION = 0x3C080001  # Synthetic MIPS instruction, not game data.


def make_iso():
    image, _ = fixture()
    cnf = b"BOOT2 = cdrom0:\\SCUS_974.81;1\r\nVER = 1.01\r\n"
    elf = bytearray(272)
    elf[:7] = b"\x7fELF\x01\x01\x01"
    struct.pack_into("<HHIIIIIHHHHHH", elf, 16,
                     2, 8, 1, 0x00100000, 52, 0, 0, 52, 32, 1, 0, 0, 0)
    struct.pack_into("<IIIIIIII", elf, 52,
                     1, 256, 0x00100000, 0x00100000, 16, 16, 5, 16)
    struct.pack_into("<I", elf, 256, INSTRUCTION)
    directory = record(b"\0", 20, SECTOR, 2) + record(b"\1", 20, SECTOR, 2)
    directory += record(b"SYSTEM.CNF;1", 21, len(cnf))
    directory += record(b"SCUS_974.81;1", 22, len(elf))
    image[20 * SECTOR:21 * SECTOR] = directory.ljust(SECTOR, b"\0")
    image[21 * SECTOR:22 * SECTOR] = cnf.ljust(SECTOR, b"\0")
    image[22 * SECTOR:23 * SECTOR] = elf.ljust(SECTOR, b"\0")
    return image


def make_pe():
    pe = bytearray(256)
    pe[:2] = b"MZ"
    struct.pack_into("<I", pe, 60, 64)
    pe[64:68] = b"PE\0\0"
    struct.pack_into("<HHIIIHH", pe, 68, 0x8664, 0, 1234, 0, 0, 112, 2)
    struct.pack_into("<H", pe, 88, 0x20B)
    struct.pack_into("<I", pe, 88 + 56, 0x2000)
    return bytes(pe)


def recv_exact(connection, count):
    data = b""
    while len(data) < count:
        chunk = connection.recv(count - len(data))
        if not chunk:
            raise EOFError
        data += chunk
    return data


class PineServer:
    def __init__(self, scenario="normal"):
        self.scenario = scenario
        self.requests = []
        self.errors = []
        self.sock = socket.socket()
        self.sock.bind(("127.0.0.1", 0))
        self.port = self.sock.getsockname()[1]
        self.sock.listen(1)
        self.sock.settimeout(15)
        self.thread = threading.Thread(target=self.serve, daemon=True)

    def __enter__(self):
        if self.scenario == "connection_refused":
            self.sock.close()
        else:
            self.thread.start()
        return self

    def __exit__(self, *args):
        if self.scenario == "connection_refused":
            return
        self.thread.join(5)
        self.sock.close()
        if self.thread.is_alive():
            raise AssertionError("Diagnostic did not close its PINE connection")
        if self.errors:
            raise AssertionError(self.errors)

    def serve(self):
        read_happened = False
        try:
            with self.sock.accept()[0] as connection:
                connection.settimeout(8)
                connection.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                while True:
                    try:
                        length, = struct.unpack("<I", recv_exact(connection, 4))
                    except EOFError:
                        break
                    if not 5 <= length <= 9:
                        raise AssertionError(f"Invalid request size: {length}")
                    request = recv_exact(connection, length - 4)
                    opcode = request[0]
                    self.requests.append(request)
                    if opcode not in (2, 8, 11, 12, 13, 14, 15):
                        raise AssertionError(f"Forbidden opcode {opcode}")
                    expected_size = 5 if opcode == 2 else 1
                    if len(request) != expected_size:
                        raise AssertionError("Wrong opcode argument layout")
                    if self.scenario == "timeout":
                        try:
                            while connection.recv(1):
                                pass
                        except ConnectionResetError:
                            pass
                        break
                    if self.scenario == "oversized":
                        connection.sendall(struct.pack("<I", 450000))
                        break
                    if self.scenario == "truncated":
                        connection.sendall(struct.pack("<I", 9) + b"\0\x01")
                        break
                    if self.scenario == "ipc_fail":
                        connection.sendall(struct.pack("<I", 5) + b"\xff")
                        break
                    if opcode == 2:
                        address, = struct.unpack("<I", request[1:])
                        if address != 0x00100000:
                            raise AssertionError(f"Unexpected address {address:#x}")
                        read_happened = True
                        payload = struct.pack("<I", INSTRUCTION ^ (self.scenario == "mismatch"))
                    elif opcode == 15:
                        payload = struct.pack("<I", 2 if self.scenario == "shutdown" else
                                              1 if self.scenario == "paused" else 0)
                    else:
                        texts = {
                            8: "PCSX2 v2.8.2", 11: "God of War II", 12: "SCUS-97481",
                            13: "2f123fd8", 14: "1.01",
                        }
                        if self.scenario == "wrong_game":
                            texts.update({11: "God of War", 12: "SCES-53133", 13: "fb0e6d72"})
                        if self.scenario == "changed" and read_happened:
                            texts[13] = "00000000"
                        if self.scenario == "wrong_version":
                            texts[8] = "PCSX2 v2.9.0"
                        encoded = texts[opcode].encode() + b"\0"
                        payload = struct.pack("<I", len(encoded)) + encoded
                        if self.scenario == "bad_string":
                            payload = struct.pack("<I", len(encoded) + 1) + encoded
                    frame = struct.pack("<I", 5 + len(payload)) + b"\0" + payload
                    # Force fragmented headers and bodies, including frame boundaries.
                    connection.sendall(frame[:2])
                    time.sleep(0.003)
                    connection.sendall(frame[2:6])
                    time.sleep(0.003)
                    connection.sendall(frame[6:])
        except (BrokenPipeError, ConnectionResetError):
            pass  # Expected when the client refuses a bad frame.
        except Exception as error:
            self.errors.append(repr(error))


@unittest.skipUnless(PWSH, "PowerShell required for real client integration tests; see docs/pine.md")
class PineProbeTests(unittest.TestCase):
    def run_probe(self, scenario="normal", mutate_iso=None, missing_iso=False):
        with tempfile.TemporaryDirectory() as temporary:
            folder = Path(temporary)
            iso = folder / "test.iso"
            image = make_iso()
            if mutate_iso:
                mutate_iso(image)
            if not missing_iso:
                iso.write_bytes(image)
            game = folder / "game"
            game.mkdir()
            executable = game / "dmc3.exe"
            executable.write_bytes(make_pe())
            logs = folder / "logs"
            env = os.environ.copy()
            # Portable pwsh cannot write its defaults under the cloud user's HOME.
            for name in ("XDG_CACHE_HOME", "XDG_CONFIG_HOME", "XDG_DATA_HOME"):
                env[name] = str(folder / name)
            with PineServer(scenario) as pine:
                command = [PWSH, "-NoLogo", "-NoProfile", "-NonInteractive", "-File",
                           str(ROOT / "tools" / "Probe-Pine.ps1"),
                           "-IsoPath", str(iso), "-GameRoot", str(game),
                           "-LogRoot", str(logs), "-PinePort", str(pine.port),
                           "-TimeoutMs", "500"]
                result = subprocess.run(command, capture_output=True, text=True, env=env, timeout=20)
                runs = list(logs.glob("pine-probe-*"))
                self.assertEqual(len(runs), 1, result.stdout + result.stderr)
                report = json.loads((runs[0] / "report.json").read_text(encoding="utf-8-sig"))
                events = [json.loads(line) for line in (runs[0] / "events.jsonl").read_text().splitlines()]
                self.assertEqual([e["sequence"] for e in events], list(range(1, len(events) + 1)))
                self.assertTrue(all(e["session"] == report["session"] for e in events))
                self.assertTrue(all(e["schema_version"] == 1 for e in events))
                self.assertTrue(report["read_only"])
                self.assertFalse(report["game_to_game_communication"])
                self.assertFalse(report["authentic_attacks_detected"])
                self.assertEqual(executable.read_bytes(), make_pe())
                if not missing_iso:
                    self.assertEqual(iso.read_bytes(), image)
            return result, report, pine.requests

    def test_fragmented_protocol_and_verified_code_read(self):
        result, report, requests = self.run_probe()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr + str(report))
        self.assertTrue(report["phase1_verified"])
        self.assertEqual(report["memory_test"]["actual_hex"], f"0x{INSTRUCTION:08X}")
        self.assertEqual(sum(r[0] == 2 for r in requests), 1)
        self.assertEqual(report["dmc3"]["running"], "not_observed")
        fingerprint = report["dmc3"]["fingerprints"][0]
        self.assertEqual(fingerprint["status"], "fingerprinted", fingerprint)
        self.assertEqual(fingerprint["sha256"], hashlib.sha256(make_pe()).hexdigest())
        self.assertEqual(fingerprint["pe_machine"], "0x8664")
        self.assertEqual(fingerprint["pe_size_of_image"], 0x2000)
        self.assertEqual(report["dmc3"]["ddmk_compatibility"], "unverified")

    def test_paused_allows_only_static_code_verification(self):
        result, report, _ = self.run_probe("paused")
        self.assertEqual(result.returncode, 0, result.stderr + str(report))
        self.assertEqual(report["pine"]["status_name"], "paused")

    def test_game_or_version_mismatch_and_shutdown_refuse_memory(self):
        for scenario in ("wrong_game", "wrong_version", "shutdown"):
            with self.subTest(scenario=scenario):
                result, report, requests = self.run_probe(scenario)
                self.assertNotEqual(result.returncode, 0)
                self.assertTrue(report["pine"]["responds"])
                self.assertFalse(report["phase1_verified"])
                self.assertNotIn(2, [r[0] for r in requests])
                self.assertIn("reason", report["memory_test"])

    def test_memory_mismatch_or_game_change_never_claim_success(self):
        for scenario in ("mismatch", "changed"):
            with self.subTest(scenario=scenario):
                result, report, requests = self.run_probe(scenario)
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse(report["phase1_verified"])
                self.assertFalse(report["memory_test"]["matches_iso"])
                self.assertTrue(report["errors"])
                self.assertEqual(sum(r[0] == 2 for r in requests), 1)

    def test_protocol_failures_are_bounded_and_keep_dmc_results(self):
        for scenario in ("ipc_fail", "truncated", "oversized", "bad_string", "timeout"):
            with self.subTest(scenario=scenario):
                result, report, requests = self.run_probe(scenario)
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse(report["phase1_verified"])
                self.assertTrue(report["errors"])
                self.assertLess(report["elapsed_ms"], 8000)
                self.assertEqual(report["dmc3"]["fingerprints"][0]["sha256"], hashlib.sha256(make_pe()).hexdigest())
                self.assertNotIn(2, [r[0] for r in requests])

    def test_missing_iso_prevents_memory_not_metadata(self):
        result, report, requests = self.run_probe(missing_iso=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertTrue(report["pine"]["target_matches"])
        self.assertNotIn(2, [r[0] for r in requests])

    def test_connection_refused_keeps_report_and_executable_fingerprint(self):
        result, report, requests = self.run_probe("connection_refused")
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(report["pine"]["tcp_connected"])
        self.assertFalse(report["pine"]["responds"])
        self.assertEqual(report["dmc3"]["fingerprints"][0]["sha256"], hashlib.sha256(make_pe()).hexdigest())
        self.assertTrue(report["errors"])
        self.assertFalse(requests)

    def test_no_read_for_non_executable_or_mmio_entry(self):
        def no_execute(image):
            struct.pack_into("<I", image, 22 * SECTOR + 52 + 24, 4)

        def mmio_entry(image):
            base = 22 * SECTOR
            struct.pack_into("<I", image, base + 24, 0x10000000)
            struct.pack_into("<I", image, base + 52 + 8, 0x10000000)

        for mutation in (no_execute, mmio_entry):
            with self.subTest(mutation=mutation.__name__):
                result, report, requests = self.run_probe(mutate_iso=mutation)
                self.assertNotEqual(result.returncode, 0)
                self.assertTrue(report["errors"])
                self.assertNotIn(2, [r[0] for r in requests])

    def test_cached_mips_ram_alias_is_normalized(self):
        def kseg0_entry(image):
            base = 22 * SECTOR
            struct.pack_into("<I", image, base + 24, 0x80100000)
            struct.pack_into("<I", image, base + 52 + 8, 0x80100000)

        result, report, requests = self.run_probe(mutate_iso=kseg0_entry)
        self.assertEqual(result.returncode, 0, result.stderr + str(report))
        self.assertEqual(report["memory_test"]["probe"]["elf_entry"], "0x80100000")
        self.assertIn(b"\x02" + struct.pack("<I", 0x00100000), requests)


if __name__ == "__main__":
    unittest.main()
