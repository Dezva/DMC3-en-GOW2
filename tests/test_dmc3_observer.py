"""Synthetic fault tests plus a Windows self-read. Never touches user games."""
import argparse
import contextlib
import ctypes
import hashlib
import io
import json
import os
from pathlib import Path
import struct
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import dmc3_memory as mem
import dmc3_profile as profile
import observe_dmc3 as observer
import analyze_dmc3_capture as analyzer


BASE = 0x140000000
POOL, EVENTS, ACTOR, EVENT = 0x200000, 0x210000, 0x300000, 0x400000


class FakeMemory:
    def __init__(self):
        self.data = {}
        self.calls = []
        self.active = True
        self.focused = True
        self.fault = None
        self.partial = False
        self.guarded = False
        self.put(BASE + profile.ROOTS["actor_pool"], "<Q", POOL)
        self.put(BASE + profile.ROOTS["event_pool"], "<Q", EVENTS)
        self.put(POOL + 24, "<Q", ACTOR)
        self.put(EVENTS + 64, "<Q", EVENT)
        self.write(BASE + profile.ROOTS["session"], bytes(32))
        self.put(BASE + profile.ROOTS["session"], "<I", 7)
        self.put(EVENT + 0x18, "<6I", 127, 2, 1, 0, 0, 0)
        self.put(ACTOR + 0x78, "<I", 0)
        self.put(ACTOR + 0x118, "<II", 0, 0)
        self.put(ACTOR + 0x39B0, "<4B", 3, 0, 3, 0)
        self.put(ACTOR + 0x3E34, "<f", 2)
        self.put(ACTOR + 0x3E64, "<I", 1)

    def write(self, address, data):
        # Fixture bytes only; the production API has no write method.
        self.data.update((address + i, value) for i, value in enumerate(data))

    def put(self, address, fmt, *values):
        self.write(address, struct.pack(fmt, *values))

    def alive(self):
        return self.active

    def foreground(self):
        return self.focused

    def query(self, address):
        return mem.Page(address & ~4095, 4096, 0x1000, 0x104 if self.guarded else 4)

    def read(self, address, size):
        self.calls.append((address, size))
        if self.fault:
            raise mem.ObservationError("read_process_memory", "Synthetic access denied", winerror=5,
                                       requested=size, transferred=0)
        data = bytes(self.data.get(address + i, 0) for i in range(size))
        return data[:-1] if self.partial else data

    @property
    def read_calls(self):
        return len(self.calls)

    @property
    def read_bytes(self):
        return sum(size for _, size in self.calls)


class CandidateTests(unittest.TestCase):
    def setUp(self):
        self.memory = FakeMemory()
        self.sampler = profile.CandidateSampler(self.memory, BASE)

    def coherent(self):
        result = [self.sampler.sample() for _ in range(3)]
        self.assertEqual([r["valid"] for r in result], [False, False, True])
        self.assertFalse(result[-1]["attack_detected"])
        self.assertFalse(result[-1]["actor_semantics_verified"])
        return result[-1]

    def test_three_stable_samples_are_candidates_only(self):
        result = self.coherent()
        self.assertEqual(result["motion"][0], {"index": 3, "group": 0})
        self.assertEqual(sum(n for _, n in self.memory.calls), 600)
        self.assertLessEqual(max(n for _, n in self.memory.calls), 32)

    def test_access_error_clears_cached_actor_and_preserves_winerror(self):
        self.coherent()
        self.memory.fault = True
        result = self.sampler.sample()
        self.assertFalse(result["valid"])
        self.assertNotIn("actor", result)
        self.assertEqual(result["error"]["winerror"], 5)
        self.memory.fault = False
        self.assertEqual(self.sampler.sample()["status"], "warming_up")

    def test_partial_read_invalidates_entire_sample(self):
        self.coherent()
        self.memory.partial = True
        result = self.sampler.sample()
        self.assertEqual(result["error"]["stage"], "read")
        self.assertNotIn("motion", result)
        self.assertEqual(result["error"]["transferred"], 7)

    def test_null_misaligned_and_kernel_pointer_rejected(self):
        for address in (0, ACTOR + 1, 0xFFFF800000000000):
            with self.subTest(address=address):
                self.memory.put(POOL + 24, "<Q", address)
                result = self.sampler.sample()
                self.assertFalse(result["valid"])
                self.assertEqual(result["error"]["stage"], "actor_unavailable")

    def test_lost_actor_then_reappearance_requires_warmup(self):
        self.coherent()
        self.memory.put(POOL + 24, "<Q", 0)
        self.assertFalse(self.sampler.sample()["valid"])
        self.memory.put(POOL + 24, "<Q", ACTOR)
        self.coherent()

    def test_process_exit_stops_using_old_values(self):
        self.coherent()
        self.memory.active = False
        calls = len(self.memory.calls)
        result = self.sampler.sample()
        self.assertEqual(result["error"]["stage"], "process_lost")
        self.assertEqual(len(self.memory.calls), calls)

    def test_guard_page_is_rejected_before_read(self):
        self.memory.guarded = True
        result = self.sampler.sample()
        self.assertEqual(result["error"]["stage"], "page")
        self.assertFalse(self.memory.calls)

    def test_focus_loss_invalidates_cached_actor_without_gameplay_reads(self):
        self.coherent()
        self.memory.focused = False
        calls = len(self.memory.calls)
        result = self.sampler.sample()
        self.assertEqual(result["error"]["stage"], "foreground_lost")
        self.assertNotIn("actor", result)
        self.assertEqual(len(self.memory.calls), calls)
        self.memory.focused = True
        self.assertEqual(self.sampler.sample()["status"], "warming_up")

    def test_room_change_starts_new_generation(self):
        before = self.coherent()
        self.memory.put(EVENT + 0x18, "<I", 128)
        after = self.sampler.sample()
        self.assertFalse(after["valid"])
        self.assertGreater(after["generation"], before["generation"])

    def test_context_change_during_read_rejects_sample(self):
        original = self.memory.read
        def changing(address, size):
            result = original(address, size)
            if address == ACTOR + 0x3E64:
                self.memory.put(EVENT + 0x18, "<I", 129)
            return result
        self.memory.read = changing
        self.assertEqual(self.sampler.sample()["error"]["stage"], "context_changed")

    def test_pause_menu_is_invalid_context(self):
        self.coherent()
        self.memory.put(EVENT + 0x20, "<I", 3)
        result = self.sampler.sample()
        self.assertFalse(result["valid"])
        self.assertEqual(result["error"]["stage"], "context_unknown")

    def test_wrong_character_clone_and_motion_group_are_rejected(self):
        for address, fmt, value in ((ACTOR + 0x78, "<I", 3), (ACTOR + 0x11C, "<I", 1),
                                    (ACTOR + 0x39B1, "<B", 34)):
            with self.subTest(address=address):
                self.memory = FakeMemory()
                self.sampler = profile.CandidateSampler(self.memory, BASE)
                self.memory.put(address, fmt, value)
                self.assertEqual(self.sampler.sample()["error"]["stage"], "actor_identity")

    def test_nonfinite_timer_rejected(self):
        self.memory.put(ACTOR + 0x3E34, "<f", float("nan"))
        self.assertEqual(self.sampler.sample()["error"]["stage"], "motion_timer")

    def test_negative_timer_is_preserved_as_unknown_not_silently_accepted(self):
        self.memory.put(ACTOR + 0x3E34, "<f", -1)
        result = self.sampler.sample()
        self.assertFalse(result["valid"])
        self.assertEqual(result["error"]["value"], "-1.0")

    def test_timer_loop_or_motion_change_never_means_attack(self):
        self.coherent()
        self.memory.put(ACTOR + 0x3E34, "<f", 0)
        self.assertTrue(self.sampler.sample()["timer_reset_same_motion"])
        self.memory.put(ACTOR + 0x39B0, "<B", 99)
        self.assertFalse(self.sampler.sample()["attack_detected"])


def synthetic_pe():
    data = bytearray(0x240800)
    data[:2] = b"MZ"
    struct.pack_into("<I", data, 60, 0x80)
    data[0x80:0x84] = b"PE\0\0"
    struct.pack_into("<HHI", data, 0x84, 0x8664, 2, 1234)
    struct.pack_into("<H", data, 0x94, 0xF0)
    struct.pack_into("<H", data, 0x98, 0x20B)
    struct.pack_into("<I", data, 0xD0, 0xDAC000)
    for offset, name, rva, vsize, rawsize, rawoffset, flags in (
        (0x188, b".text", 0x1000, 0x240000, 0x240000, 0x400, 0x60000020),
        (0x1B0, b".data", 0x500000, 0x800000, 0x400, 0x240400, 0xC0000040)):
        struct.pack_into("<8sIIII", data, offset, name, vsize, rva, rawsize, rawoffset)
        struct.pack_into("<I", data, offset + 36, flags)
    rva = 0x2000
    displacement = profile.ROOTS["actor_pool"] - rva - 7
    data[0x1400:0x1407] = b"\x48\x8b\x05" + struct.pack("<i", displacement)
    for rva, code in profile.SOURCE_ANCHORS:
        start = 0x400 + rva - 0x1000
        data[start:start + len(code)] = code
    return data


class ProfileTests(unittest.TestCase):
    def test_access_only_never_derives_profile_or_reads_candidate_roots(self):
        class SelfFixture(FakeMemory):
            def discover(self, path):
                return dict(pid=777, path=str(path), creation_filetime=134000000000000000)
            def open(self, *args):
                return None
            def attach(self, identity):
                pass
            def image(self):
                return dict(base=BASE, size=0xDAC000)
            def close(self):
                pass
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "synthetic.exe"
            data = synthetic_pe()
            path.write_bytes(data)
            backend = SelfFixture()
            backend.write(BASE, data[:64])
            backend.write(BASE + 0x80, data[0x80:0x80 + 88])
            args = argparse.Namespace(exe=path, log_root=tmp, label="access", access_only=True,
                                      hz=10, samples=3, lead_in_seconds=0, beep=False)
            with patch.object(observer, "WindowsMemory", return_value=backend), \
                    patch.object(observer, "derive_profile") as derive, contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(observer.capture(args), 0)
                derive.assert_not_called()
            self.assertEqual(backend.calls, [(BASE, 64), (BASE + 0x80, 88)])

    def test_unknown_build_capture_never_attaches_gameplay_backend(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "other-build.exe"
            path.write_bytes(synthetic_pe())
            args = argparse.Namespace(exe=path, log_root=tmp, label="other", access_only=False,
                                      hz=10, samples=3, lead_in_seconds=0, beep=False)
            with patch.object(observer, "WindowsMemory") as backend, contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(observer.capture(args), 1)
                backend.assert_not_called()
            report = json.loads(next(Path(tmp).glob("*/report.json")).read_text())
            self.assertNotEqual(report["disk_build"]["sha256"], profile.BUILD_SHA256)
            self.assertEqual(report["errors"][0]["stage"], "profile_incompatible")

    def test_open_requests_query_information_and_read_without_all_access(self):
        backend = object.__new__(mem.WindowsMemory)
        calls = []
        backend.open = lambda access, inherit, pid: calls.append((access, inherit, pid)) or None
        backend.fail = lambda stage, **details: (_ for _ in ()).throw(
            mem.ObservationError(stage, "Synthetic denied", winerror=5, **details))
        with self.assertRaises(mem.ObservationError) as error:
            backend.attach(dict(pid=777, path="fixture", creation_filetime=1))
        self.assertEqual(calls, [(0x410, False, 777)])
        self.assertEqual(error.exception.data["winerror"], 5)

    def test_unknown_build_rejected_before_candidate_reads(self):
        memory = FakeMemory()
        with self.assertRaises(mem.ObservationError) as error:
            profile.verify_profile(memory, {}, {"sha256": "other"}, {})
        self.assertEqual(error.exception.data["stage"], "profile_incompatible")
        self.assertFalse(memory.calls)

    def test_static_derivation_and_loaded_code_tamper_gate(self):
        data = synthetic_pe()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "synthetic.exe"
            path.write_bytes(data)
            # Test-only fixture hash injection; production CLI has no bypass flag.
            with patch.object(profile, "BUILD_SHA256", hashlib.sha256(data).hexdigest()):
                derived = profile.derive_profile(path)
                memory = FakeMemory()
                memory.write(BASE, data[:64])
                memory.write(BASE + 0x80, data[0x80:0x80 + 88])
                for item in derived["signatures"] + derived["source_anchors"]:
                    offset = 0x400 + item["rva"] - 0x1000
                    memory.write(BASE + item["rva"], data[offset:offset + item["size"]])
                image = dict(base=BASE, size=0xDAC000)
                profile.verify_profile(memory, image, derived["build"], derived)
                signature = derived["signatures"][0]
                memory.write(BASE + signature["rva"], b"\x90")
                with self.assertRaises(mem.ObservationError) as error:
                    profile.verify_profile(memory, image, derived["build"], derived)
                self.assertEqual(error.exception.data["stage"], "static_profile")

    def test_source_anchor_mismatch_rejected_even_if_hash_gate_matches(self):
        data = synthetic_pe()
        data[0x400 + profile.SOURCE_ANCHORS[0][0] - 0x1000] ^= 1
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "synthetic.exe"
            path.write_bytes(data)
            with patch.object(profile, "BUILD_SHA256", hashlib.sha256(data).hexdigest()):
                with self.assertRaises(mem.ObservationError) as error:
                    profile.derive_profile(path)
                self.assertEqual(error.exception.data["stage"], "static_profile")

    def test_denied_access_is_saved_without_memory_calls(self):
        class Denied:
            read_calls = read_bytes = 0
            closed = False
            def discover(self, path):
                return dict(pid=777, path=path, creation_filetime=134000000000000000)
            def open(self, *args):
                return None
            def attach(self, identity):
                raise mem.ObservationError("open_query_read", "Synthetic denial", winerror=5,
                                           requested_access=mem.QUERY_READ)
            def close(self):
                self.closed = True
        backend = Denied()
        with tempfile.TemporaryDirectory() as tmp:
            args = argparse.Namespace(exe="synthetic", log_root=tmp, label="test", access_only=True,
                                      hz=10, samples=3, lead_in_seconds=0, beep=False)
            with patch.object(observer, "inspect_pe", return_value=({"sha256": "fixture"}, b"")), \
                    patch.object(observer, "WindowsMemory", return_value=backend), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(observer.capture(args), 1)
            report = json.loads(next(Path(tmp).glob("*/report.json")).read_text())
            self.assertEqual(report["errors"][0]["winerror"], 5)
            self.assertEqual(report["read_calls"], 0)
            self.assertFalse(report["phase2_verified"])
            self.assertTrue(backend.closed)


class LogTests(unittest.TestCase):
    def fixture(self, path):
        stamp = time.perf_counter_ns()
        report = dict(protocol="dmc3-read-only-observer", schema_version=1, session="synthetic",
                      started_monotonic_ns=stamp, candidate_samples=0, invalid_samples=1,
                      manual_label="manual attack label is not evidence")
        events = [dict(protocol=report["protocol"], schema_version=1, session="synthetic", sequence=i + 1,
                       monotonic_ns=stamp + i, stage=stage, data=data)
                  for i, (stage, data) in enumerate([
                      ("session.start", {}),
                      ("candidate.sample", dict(valid=False, status="warming_up")),
                      ("session.result", {})])]
        (path / "report.json").write_text(json.dumps(report))
        (path / "events.jsonl").write_text("\n".join(json.dumps(e) for e in events))
        return events

    def test_manual_attack_label_never_becomes_detection(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.fixture(Path(tmp))
            summary = analyzer.analyze(tmp)
            self.assertFalse(summary["attack_detector"])
            self.assertFalse(summary["phase2_verified"])

    def test_missing_event_and_backwards_clock_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)
            for fault in ("sequence", "clock", "session"):
                with self.subTest(fault=fault):
                    events = self.fixture(path)
                    if fault == "sequence":
                        events[1]["sequence"] = 3
                    elif fault == "clock":
                        events[1]["monotonic_ns"] = 0
                    else:
                        events[1]["session"] = "other"
                    (path / "events.jsonl").write_text("\n".join(json.dumps(e) for e in events))
                    with self.assertRaises(ValueError):
                        analyzer.analyze(path)

    def test_manual_annotation_uses_monotonic_time_and_refuses_closed_capture(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)
            session = dict(protocol="dmc3-read-only-observer", session="synthetic",
                           started_monotonic_ns=time.perf_counter_ns())
            (path / "session.json").write_text(json.dumps(session))
            args = argparse.Namespace(annotate=tmp, action="operator reports jump")
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(observer.annotate(args), 0)
            item = json.loads((path / "annotations.jsonl").read_text())
            self.assertGreaterEqual(item["elapsed_ns"], 0)
            self.assertEqual(item["provenance"], "manual_report_unverified")
            (path / "report.json").write_text("{}")
            with self.assertRaises(ValueError):
                observer.annotate(args)


@unittest.skipUnless(os.name == "nt" and ctypes.sizeof(ctypes.c_void_p) == 8, "Windows x64 required")
class WindowsSelfReadTests(unittest.TestCase):
    def test_query_read_self_buffer_and_real_image(self):
        memory = mem.WindowsMemory()
        limited = memory.open(mem.QUERY_LIMITED, False, os.getpid())
        try:
            identity = dict(pid=os.getpid(), path=memory.path(limited), creation_filetime=memory.creation(limited))
        finally:
            memory.close_handle(limited)
        try:
            memory.attach(identity)
            image = memory.image()
            self.assertEqual(mem.read_exact(memory, image["base"], 2), b"MZ")
            buffer = ctypes.create_string_buffer(b"synthetic-self-read")
            self.assertEqual(mem.read_exact(memory, ctypes.addressof(buffer), len(buffer)), buffer.raw)
            self.assertTrue(memory.alive())
        finally:
            memory.close()


if __name__ == "__main__":
    unittest.main()
