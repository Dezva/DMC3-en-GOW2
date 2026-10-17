"""Synthetic diagnostic faults, including negative timers. No real game access."""
import argparse
import contextlib
import copy
import hashlib
import io
import json
import itertools
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import dmc3_profile as profile
import dmc3_timer_diagnostic as diagnostic
import observe_dmc3 as observer
import analyze_dmc3_timer_diagnostic as analysis
from dmc3_memory import ObservationError
from test_dmc3_observer import FakeMemory, BASE, POOL, ACTOR, EVENT, synthetic_pe
from test_dmc3_temporal import records, write_capture


class DiagnosticTests(unittest.TestCase):
    def setUp(self):
        self.memory = FakeMemory()
        self.memory.put(ACTOR + 0x3E08, "<I4xB", 6, 4)
        self.memory.put(ACTOR + 0x14, "<f", 1)
        self.sampler = diagnostic.TimerDiagnosticSampler(self.memory, BASE)

    def sample_negative(self):
        self.memory.put(ACTOR + 0x3E34, "<f", -1)
        return self.sampler.sample()

    def test_negative_rejected_but_context_rechecked(self):
        result = self.sample_negative()
        self.assertFalse(result["valid"])
        self.assertEqual(result["error"]["stage"], "motion_timer")
        self.assertNotIn("motion", result)
        d = result["timer_diagnostic"]
        self.assertTrue(d["actor_context_rechecked"])
        self.assertTrue(d["event_phase_stable"])
        self.assertEqual((d["event_before"], d["phase_before"], d["speed_f32"]), (6, 4, 1.0))
        self.assertEqual(d["timer_quality"], "rejected_unknown")
        self.assertEqual(d["timer_raw_f32"], -1.0)
        self.assertFalse(d["semantics_verified"])
        self.assertLessEqual(d["read_begin_ns"], d["read_end_ns"])
        json.dumps(result, allow_nan=False)

    def test_nonfinite_timer_remains_unknown_and_json_finite(self):
        self.memory.put(ACTOR + 0x3E34, "<f", float("nan"))
        result = self.sampler.sample()
        self.assertEqual(result["error"]["stage"], "motion_timer")
        self.assertIsNone(result["timer_diagnostic"]["timer_raw_f32"])
        self.assertTrue(result["timer_diagnostic"]["actor_context_rechecked"])
        json.dumps(result, allow_nan=False)

    def changing_on_state(self, action):
        original = self.memory.read
        def read(address, size):
            value = original(address, size)
            if address == ACTOR + 0x3E64:
                action()
            return value
        self.memory.read = read

    def test_scene_change_overrides_negative_without_retained_fields(self):
        self.changing_on_state(lambda: self.memory.put(EVENT + 0x18, "<I", 129))
        result = self.sample_negative()
        self.assertEqual(result["error"]["stage"], "context_changed")
        self.assertNotIn("timer_diagnostic", result)

    def test_actor_disappears_without_retained_fields(self):
        self.changing_on_state(lambda: self.memory.put(POOL + 24, "<Q", 0))
        result = self.sample_negative()
        self.assertEqual(result["error"]["stage"], "actor_unavailable")
        self.assertNotIn("timer_diagnostic", result)

    def test_identity_reuse_at_same_pointer_refused(self):
        self.changing_on_state(lambda: self.memory.put(ACTOR + 0x78, "<I", 3))
        result = self.sample_negative()
        self.assertEqual(result["error"]["stage"], "context_changed")
        self.assertNotIn("timer_diagnostic", result)

    def test_phase_change_is_a_transition_not_a_coherent_negative(self):
        self.changing_on_state(lambda: self.memory.put(ACTOR + 0x3E10, "<B", 3))
        result = self.sample_negative()
        self.assertEqual(result["error"]["stage"], "diagnostic_transition")
        self.assertFalse(result["timer_diagnostic"]["event_phase_stable"])
        self.assertEqual(result["timer_diagnostic"]["motion_state_quality"], "transition_observation_only")

    def test_event_change_is_a_transition(self):
        self.changing_on_state(lambda: self.memory.put(ACTOR + 0x3E08, "<I", 5))
        self.assertEqual(self.sampler.sample()["error"]["stage"], "diagnostic_transition")

    def test_focus_loss_does_not_retain_diagnostic(self):
        self.changing_on_state(lambda: setattr(self.memory, "focused", False))
        result = self.sample_negative()
        self.assertEqual(result["error"]["stage"], "context_changed")
        self.assertNotIn("timer_diagnostic", result)

    def test_process_loss_does_not_retain_diagnostic(self):
        self.changing_on_state(lambda: setattr(self.memory, "active", False))
        self.assertNotIn("timer_diagnostic", self.sample_negative())

    def test_partial_extended_read_refused(self):
        original = self.memory.read
        self.memory.read = lambda a, n: original(a, n)[:-1] if a == ACTOR + 0x3E08 else original(a, n)
        result = self.sampler.sample()
        self.assertEqual(result["error"]["stage"], "read")
        self.assertEqual(result["error"]["transferred"], 8)
        self.assertNotIn("timer_diagnostic", result)

    def test_access_error_in_speed_preserves_winerror(self):
        original = self.memory.read
        def read(a, n):
            if a == ACTOR + 0x14:
                raise ObservationError("read_process_memory", "Synthetic denial", winerror=5, transferred=0)
            return original(a, n)
        self.memory.read = read
        result = self.sampler.sample()
        self.assertEqual(result["error"]["winerror"], 5)
        self.assertNotIn("timer_diagnostic", result)

    def test_nonfinite_speed_is_explicit_unknown_not_nan_json(self):
        self.memory.put(ACTOR + 0x14, "<f", float("inf"))
        result = [self.sampler.sample() for _ in range(3)][-1]
        self.assertTrue(result["valid"])  # Existing timer/motion policy unchanged.
        self.assertIsNone(result["timer_diagnostic"]["speed_f32"])
        self.assertEqual(result["timer_diagnostic"]["speed_quality"], "nonfinite_unknown")
        json.dumps(result, allow_nan=False)

    def test_raw_event_and_phase_not_falsely_named_or_clamped(self):
        self.memory.put(ACTOR + 0x3E08, "<I4xB", 0xFFFFFFFF, 255)
        d = self.sampler.sample()["timer_diagnostic"]
        self.assertEqual((d["event_before"], d["phase_before"]), (0xFFFFFFFF, 255))
        self.assertFalse(d["semantics_verified"])

    def test_bounded_reads_and_warmup_after_rejection(self):
        self.sample_negative()
        self.assertEqual(sum(n for _, n in self.memory.calls), 234)
        self.assertEqual(len(self.memory.calls), 22)
        self.assertLessEqual(max(n for _, n in self.memory.calls), 32)
        self.memory.put(ACTOR + 0x3E34, "<f", 2)
        rows = [self.sampler.sample() for _ in range(3)]
        self.assertEqual([r["valid"] for r in rows], [False, False, True])
        self.assertFalse(any(r["attack_detected"] for r in rows))


class DiagnosticProfileTests(unittest.TestCase):
    def test_tampered_extension_precedes_any_memory_read(self):
        memory = FakeMemory()
        extension = copy.deepcopy(diagnostic.diagnostic_manifest())
        extension["fields"]["phase_u8"] += 1
        with self.assertRaises(ObservationError):
            diagnostic.verify_timer_profile(memory, {}, {"sha256": profile.BUILD_SHA256},
                                            {"timer_diagnostic": extension})
        self.assertEqual(memory.calls, [])

    def test_other_build_precedes_any_memory_read(self):
        memory = FakeMemory()
        with self.assertRaises(ObservationError):
            diagnostic.verify_timer_profile(memory, {}, {"sha256": "other"},
                                            {"timer_diagnostic": diagnostic.diagnostic_manifest()})
        self.assertEqual(memory.calls, [])

    def fixture(self, path):
        data = synthetic_pe()
        data[0x1500:0x1502] = b"\x90\xc3"
        path.write_bytes(data)
        return data, [(0x2100, 2, hashlib.sha256(b"\x90\xc3").hexdigest())]

    def populate_loaded(self, memory, data, derived):
        memory.write(BASE, data[:64])
        memory.write(BASE + 0x80, data[0x80:0x80 + 88])
        for item in derived["signatures"] + derived["source_anchors"] + derived["timer_diagnostic"]["native_anchors"]:
            offset = 0x400 + item["rva"] - 0x1000
            memory.write(BASE + item["rva"], data[offset:offset + item["size"]])

    def test_loaded_native_anchor_tampering_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "synthetic.exe"
            data, anchors = self.fixture(path)
            digest = hashlib.sha256(data).hexdigest()
            with patch.object(profile, "BUILD_SHA256", digest), patch.object(diagnostic, "BUILD_SHA256", digest), \
                    patch.object(diagnostic, "NATIVE_ANCHORS", anchors):
                derived = diagnostic.derive_timer_profile(path)
                memory = FakeMemory()
                self.populate_loaded(memory, data, derived)
                image = dict(base=BASE, size=0xDAC000)
                diagnostic.verify_timer_profile(memory, image, derived["build"], derived)
                memory.write(BASE + 0x2100, b"\x91")
                with self.assertRaises(ObservationError) as error:
                    diagnostic.verify_timer_profile(memory, image, derived["build"], derived)
                self.assertEqual(error.exception.data["stage"], "timer_profile")

    def test_profile_only_never_constructs_sampler_or_reads_actor(self):
        class Backend(FakeMemory):
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
            data, anchors = self.fixture(path)
            digest = hashlib.sha256(data).hexdigest()
            with patch.object(profile, "BUILD_SHA256", digest), patch.object(diagnostic, "BUILD_SHA256", digest), \
                    patch.object(observer, "BUILD_SHA256", digest), patch.object(diagnostic, "NATIVE_ANCHORS", anchors):
                backend = Backend()
                self.populate_loaded(backend, data, diagnostic.derive_timer_profile(path))
                backend.focused = False
                args = argparse.Namespace(exe=path, log_root=tmp, access_only=False, profile_only=True,
                                          timer_diagnostic=True, label="synthetic", hz=10, samples=1,
                                          lead_in_seconds=0, beep=False)
                with patch.object(observer, "WindowsMemory", return_value=backend), \
                        patch.object(observer, "TimerDiagnosticSampler") as sampler, \
                        contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(observer.capture(args), 0)
                    sampler.assert_not_called()
                self.assertFalse(any(ACTOR <= address < ACTOR + 0x8000 for address, _ in backend.calls))
                report = json.loads(next(Path(tmp).glob("*/report.json")).read_text())
                self.assertTrue(report["loaded_profile_gates_verified"])
                self.assertFalse(report["capture_has_coherent_candidates"])

    def test_cli_refuses_conflicting_modes_before_capture(self):
        for flags in (("--timer-diagnostic", "--access-only"), ("--profile-only", "--beep")):
            with self.subTest(flags=flags), patch.object(observer, "capture") as capture, \
                    contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                observer.main(flags)
            capture.assert_not_called()

    def test_synthetic_capture_roundtrip_keeps_negative_rejected(self):
        class Backend(FakeMemory):
            timer_reads = 0
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
            def read(self, address, size):
                if address == ACTOR + 0x3E34:
                    self.timer_reads += 1
                    self.put(address, "<f", -1 if self.timer_reads == 4 else 2)
                return super().read(address, size)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "synthetic.exe"
            data, anchors = self.fixture(path)
            digest = hashlib.sha256(data).hexdigest()
            with patch.object(profile, "BUILD_SHA256", digest), patch.object(diagnostic, "BUILD_SHA256", digest), \
                    patch.object(observer, "BUILD_SHA256", digest), patch.object(diagnostic, "NATIVE_ANCHORS", anchors):
                derived = diagnostic.derive_timer_profile(path)
                backend = Backend()
                self.populate_loaded(backend, data, derived)
                backend.put(ACTOR + 0x3E08, "<I4xB", 6, 4)
                backend.put(ACTOR + 0x14, "<f", 1)
                args = argparse.Namespace(exe=path, log_root=tmp, access_only=False, profile_only=False,
                                          timer_diagnostic=True, label="synthetic", hz=10, samples=4,
                                          lead_in_seconds=0, beep=False)
                clock = itertools.count(1_000_000_000, 100_000_000)
                with patch.object(observer, "WindowsMemory", return_value=backend), \
                        patch.object(observer.time, "sleep"), patch.object(observer.time, "perf_counter", return_value=1), \
                        patch.object(observer.time, "perf_counter_ns", side_effect=lambda: next(clock)), \
                        contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(observer.capture(args), 0)
                run = next(Path(tmp).glob("dmc3-observe-*"))
                # Synthetic hash substitution exists only inside this test.
                with patch.object(analysis, "BUILD_SHA256", digest):
                    result = analysis.analyze(run)
                self.assertEqual(result["accepted_gameplay_samples"], 1)
                self.assertEqual(result["rejected_gameplay_samples"], 3)
                self.assertEqual(result["timer_rejections_with_context"], 1)


class DiagnosticAnalysisTests(unittest.TestCase):
    def capture(self, directory, *, accepted=False, mutate=None):
        memory = FakeMemory()
        memory.put(ACTOR + 0x3E08, "<I4xB", 6, 4)
        memory.put(ACTOR + 0x14, "<f", 1)
        memory.put(ACTOR + 0x3E34, "<f", -1)
        d = diagnostic.TimerDiagnosticSampler(memory, BASE).sample()["timer_diagnostic"]
        report, events = records([{}] if accepted else [{"invalid": "motion_timer", "error": {"value": "-1.0"}}])
        report["timer_diagnostic"] = True
        d["read_begin_ns"] = events[1]["monotonic_ns"] - 200
        d["read_end_ns"] = events[1]["monotonic_ns"] - 1
        events[1]["data"]["timer_diagnostic"] = d
        if mutate:
            mutate(report, events)
        path = Path(directory) / "capture"
        write_capture(path, report, events)
        (path / "candidate-profile.json").write_text(json.dumps(dict(
            build=report["disk_build"], ddmk_commit=profile.DDMK_COMMIT,
            profile_id="dmc3-hdc-4ae4bb5c-candidate-v1", timer_diagnostic=diagnostic.diagnostic_manifest())), encoding="utf-8")
        return path

    def test_qualified_negative_does_not_promote_or_verify_cause(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = analysis.analyze(self.capture(tmp))
            self.assertEqual(result["accepted_gameplay_samples"], 0)
            self.assertEqual(result["rejected_gameplay_samples"], 1)
            self.assertEqual(result["timer_rejections_with_context"], 1)
            self.assertFalse(result["negative_cause_verified"])
            self.assertFalse(result["rows"][0]["sample_valid"])

    def test_inconsistent_phase_quality_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.capture(tmp, mutate=lambda r, e: e[1]["data"]["timer_diagnostic"].update(event_phase_stable=False))
            with self.assertRaises(ValueError):
                analysis.analyze(path)

    def test_window_after_event_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.capture(tmp, mutate=lambda r, e: e[1]["data"]["timer_diagnostic"].update(read_end_ns=e[1]["monotonic_ns"] + 1))
            with self.assertRaises(ValueError):
                analysis.analyze(path)

    def test_promoted_negative_diagnostic_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                analysis.analyze(self.capture(tmp, accepted=True))

    def test_accepted_sample_without_extension_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.capture(tmp, accepted=True, mutate=lambda r, e: e[1]["data"].pop("timer_diagnostic"))
            with self.assertRaises(ValueError):
                analysis.analyze(path)

    def test_unknown_profile_extension_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.capture(tmp)
            item = json.loads((path / "candidate-profile.json").read_text())
            item["timer_diagnostic"]["fields"]["phase_u8"] += 1
            (path / "candidate-profile.json").write_text(json.dumps(item))
            with self.assertRaises(ValueError):
                analysis.analyze(path)

    def test_unknown_build_report_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.capture(tmp, mutate=lambda r, e: r["disk_build"].update(sha256="other-build"))
            with self.assertRaisesRegex(ValueError, "Different diagnostic build"):
                analysis.analyze(path)

    def test_csv_output_new_directory_does_not_modify_capture(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.capture(tmp)
            before = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in path.iterdir()}
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(analysis.main([str(path), "--output-root", tmp]), 0)
            self.assertEqual(before, {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in path.iterdir()})
            output = next(Path(tmp).glob("dmc3-timer-review-*"))
            self.assertTrue((output / "observations.csv").exists())


if __name__ == "__main__":
    unittest.main()
