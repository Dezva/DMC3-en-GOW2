"""Offline synthetic fixtures only. Never imports a Windows/game backend."""
import contextlib
import copy
import csv
import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import dmc3_temporal as temporal
import analyze_dmc3_timeline as cli

FIXTURES = json.loads((Path(__file__).parent / "fixtures/dmc3-temporal-cases.json").read_text())


def records(specs, session="synthetic"):
    report = dict(protocol=temporal.PROTOCOL, schema_version=1, session=session,
                  started_monotonic_ns=1_000_000_000, candidate_samples=0, invalid_samples=0,
                  disk_build=dict(sha256=temporal.BUILD_SHA256), loaded_profile_gates_verified=True)
    events = []
    clock = report["started_monotonic_ns"]

    def event(stage, data):
        events.append(dict(protocol=temporal.PROTOCOL, schema_version=1, session=session,
                           sequence=len(events) + 1, monotonic_ns=clock, stage=stage, data=data))

    event("session.start", dict(hz=10))
    generation, context, actor = 1, [7, 0, 127, 1, 1, 0, 0, 0], 0x400000
    for spec in specs:
        generation = spec.get("generation", generation)
        context = spec.get("context", context)
        actor = spec.get("actor", actor)
        for _ in range(spec.get("repeat", 1)):
            clock += spec.get("delta_ns", 100_000_000)
            if "stage" in spec:
                event(spec["stage"], spec.get("data", {}))
                continue
            if "invalid" in spec:
                data = dict(valid=False, status="invalid", generation=generation,
                            error=dict(stage=spec["invalid"], **spec.get("error", {})))
            else:
                lower = spec.get("lower", spec.get("upper", [0, 0]))
                upper = spec.get("upper", [0, 0])
                data = dict(valid=True, status="candidate_coherent", generation=generation,
                            actor=actor, actor_id=0, character=0, context=list(context),
                            motion=[dict(group=g, index=i) for g, i in (lower, upper)],
                            state=spec.get("state", 1), motion_timer=spec.get("timer", 2.0))
            report["candidate_samples" if data["valid"] else "invalid_samples"] += 1
            event("candidate.sample", data)
    clock += 1_000_000
    event("session.result", dict(exit_success=True))
    return report, events


def fixture(name):
    return records(FIXTURES["cases"][name])


def write_capture(path, report, events):
    path.mkdir()
    (path / "report.json").write_text(json.dumps(report), encoding="utf-8")
    (path / "events.jsonl").write_text("\n".join(json.dumps(e) for e in events), encoding="utf-8")


class TemporalTests(unittest.TestCase):
    def analyze(self, name):
        return temporal.analyze_records(*fixture(name))

    def test_separated_candidates_are_not_chained_or_authenticated(self):
        result = self.analyze("separated_candidates")
        self.assertEqual(result["counts"]["candidate_kinds"], {"melee_motion_candidate": 2})
        self.assertFalse(result["authentic_attacks_detected"])
        self.assertFalse(result["phase2_verified"])
        self.assertEqual(result["authenticated_actions"], [])
        self.assertEqual(result["impact_events"], [])
        for event in result["candidate_events"]:
            self.assertFalse(event["authentic_attack"])
            self.assertFalse(event["impact_generated"])
            self.assertIsNone(event["action_name"])
            self.assertEqual(event["evidence_level"], "movement_hypothesis")

    def test_distinct_adjacent_motions_form_only_chain_hypothesis(self):
        result = self.analyze("chained_candidates")
        chains = [c for c in result["candidate_events"] if c["kind"] == "chained_motion_candidate"]
        self.assertEqual(len(chains), 1)
        self.assertEqual(len(chains[0]["member_ids"]), 3)
        self.assertIsNone(chains[0]["combo_completed"])

    def test_rest_jump_busy_lower_body_and_source_excluded_gun_idle_do_not_trigger(self):
        result = self.analyze("nonoffensive")
        self.assertEqual(result["candidate_events"], [])

    def test_invalid_boundaries_never_join_chains(self):
        for name in ("lost_actor", "pause_room_generation", "unknown_timer", "focus_loss"):
            with self.subTest(name=name):
                result = self.analyze(name)
                self.assertNotIn("chained_motion_candidate", result["counts"]["candidate_kinds"])
                self.assertGreater(result["counts"]["blocks"], 1)

    def test_same_address_recovery_is_censored(self):
        result = self.analyze("lost_actor")
        events = result["candidate_events"]
        self.assertEqual(len(events), 2)
        self.assertTrue(all(e["left_censored"] and e["right_censored"] for e in events))
        self.assertNotEqual(events[0]["generation"], events[1]["generation"])

    def test_timer_unknown_is_retained_not_used(self):
        result = self.analyze("unknown_timer")
        self.assertEqual(result["timer_diagnostics"]["rejected_value_counts"], {"-1.0": 1})
        self.assertFalse(result["timer_diagnostics"]["elapsed_animation_time_verified"])

    def test_negative_or_nonfinite_or_missing_timer_in_claimed_valid_sample_is_rejected(self):
        for value in (-1, float("nan"), float("inf"), None, True):
            report, events = records([{"upper": [3, 3]}])
            events[1]["data"]["motion_timer"] = value
            result = temporal.analyze_records(report, events)
            self.assertEqual(result["counts"]["accepted"], 0)
            self.assertEqual(result["candidate_events"], [])

    def test_timer_decrease_records_observation_not_restart_or_extra_attack(self):
        result = temporal.analyze_records(*records([
            {"upper": [3, 3], "timer": 5}, {"upper": [3, 3], "timer": 2}]))
        self.assertEqual(len(result["candidate_events"]), 1)
        drops = [t for t in result["transitions"] if t["kind"] == "timer_decrease_same_motion"]
        self.assertEqual(len(drops), 1)
        self.assertFalse(drops[0]["animation_restart_verified"])

    def test_constant_timer_does_not_split_identical_motions_or_mean_stopped_game(self):
        result = self.analyze("separated_candidates")
        self.assertTrue(result["timer_diagnostics"]["constant_in_accepted_samples"])
        self.assertEqual(result["counts"]["segments"], 5)

    def test_context_actor_generation_each_split_without_invalid_marker(self):
        for field, value in (("context", [7, 0, 114, 1, 1, 0, 0, 0]),
                             ("actor", 0x500000), ("generation", 2)):
            result = temporal.analyze_records(*records([{"upper": [3, 1]}, {"upper": [3, 2], field: value}]))
            self.assertEqual(result["counts"]["blocks"], 2)
            self.assertNotIn("chained_motion_candidate", result["counts"]["candidate_kinds"])

    def test_delayed_sample_or_skipped_tick_breaks_continuity(self):
        scenarios = [[{"upper": [3, 1]}, {"upper": [3, 2], "delta_ns": 500_000_000}],
                     [{"upper": [3, 1]}, {"stage": "sampling.skipped"}, {"upper": [3, 2]}]]
        for specs in scenarios:
            result = temporal.analyze_records(*records(specs))
            self.assertEqual(result["counts"]["blocks"], 2)
            self.assertNotIn("chained_motion_candidate", result["counts"]["candidate_kinds"])

    def test_implausibly_close_sample_rejected(self):
        result = temporal.analyze_records(*records([{}, {"upper": [3, 3], "delta_ns": 1}]))
        self.assertEqual(result["timeline"][1]["rejected_reason"], "sample_too_close_to_previous")
        self.assertEqual(result["candidate_events"], [])

    def test_duplicate_reordered_and_missing_sequence_rejected_not_sorted(self):
        for mutation in ("duplicate", "reorder", "missing"):
            report, events = fixture("separated_candidates")
            if mutation == "duplicate": events.insert(2, copy.deepcopy(events[1]))
            elif mutation == "reorder": events[1], events[2] = events[2], events[1]
            else: del events[2]
            with self.assertRaises(temporal.CaptureError): temporal.analyze_records(report, events)

    def test_duplicate_and_backward_sample_clocks_rejected(self):
        for difference in (0, -1):
            report, events = fixture("separated_candidates")
            events[2]["monotonic_ns"] = events[1]["monotonic_ns"] + difference
            with self.assertRaises(temporal.CaptureError): temporal.analyze_records(report, events)

    def test_incomplete_capture_and_counter_mismatch_rejected(self):
        report, events = fixture("separated_candidates")
        with self.assertRaises(temporal.CaptureError): temporal.analyze_records(report, events[:-1])
        report["candidate_samples"] += 1
        with self.assertRaises(temporal.CaptureError): temporal.analyze_records(report, events)

    def test_incomplete_sample_does_not_bridge_candidates(self):
        for field in ("state", "motion", "context", "actor", "actor_id", "generation", "character"):
            report, events = fixture("chained_candidates")
            del events[4]["data"][field]
            result = temporal.analyze_records(report, events)
            self.assertFalse(result["timeline"][3]["accepted"])

    def test_unknown_profile_still_has_raw_timeline_but_no_source_hypotheses(self):
        report, events = fixture("chained_candidates")
        report["disk_build"]["sha256"] = "other-build"
        result = temporal.analyze_records(report, events)
        self.assertGreater(len(result["segments"]), 0)
        self.assertFalse(result["compatible_source_rules"])
        self.assertEqual(result["candidate_events"], [])

    def test_manual_claims_and_cues_never_change_candidates(self):
        report, events = fixture("separated_candidates")
        original = temporal.analyze_records(report, events)
        report["manual_label"] = "100 authenticated hits and a complete combo"
        report["phase2_verified"] = True
        result = temporal.analyze_records(report, events, associations=[{"claim": "attack at t=0"}])
        self.assertEqual(original["candidate_events"], result["candidate_events"])
        self.assertFalse(result["phase2_verified"])
        self.assertFalse(result["authentic_attacks_detected"])

    def test_unknown_state_bits_preserved_without_attack_promotion(self):
        result = temporal.analyze_records(*records([{"state": 524289}]))
        self.assertEqual(result["segments"][0]["state_bits"]["unknown_bits"], 524288)
        self.assertEqual(result["candidate_events"], [])

    def test_unknown_or_malformed_error_never_becomes_valid(self):
        report, events = records([{"invalid": "motion_timer"}])
        events[1]["data"]["error"]["stage"] = None
        with self.assertRaises(temporal.CaptureError): temporal.analyze_records(report, events)
        events[1]["data"].pop("error")
        events[1]["data"]["status"] = None
        self.assertEqual(temporal.analyze_records(report, events)["counts"]["accepted"], 0)

    def test_generation_regression_cannot_rejoin_previous_actor(self):
        result = temporal.analyze_records(*records([
            {"upper": [3, 1], "generation": 2}, {"upper": [3, 2], "generation": 1}]))
        self.assertEqual(result["timeline"][1]["rejected_reason"], "generation_missing_or_regressed")
        self.assertNotIn("chained_motion_candidate", result["counts"]["candidate_kinds"])

    def test_warmup_data_cannot_generate_candidate_and_cues_are_not_actions(self):
        report, events = records([{"upper": [3, 3]}, {"stage": "sampling.begin", "data": {"action": "attack"}}, {}])
        events[1]["data"].update(valid=False, status="warming_up")
        report.update(candidate_samples=1, invalid_samples=1)
        result = temporal.analyze_records(report, events)
        self.assertEqual(result["candidate_events"], [])
        self.assertFalse(result["cues"][0]["observed_action_time"])

    def test_lower_and_upper_body_independent_and_upper_run_preserves_state_changes(self):
        result = temporal.analyze_records(*records([
            {"upper": [3, 3], "lower": [0, 0]},
            {"upper": [3, 3], "lower": [0, 3], "state": 65537}]))
        self.assertEqual(len(result["candidate_events"]), 1)
        self.assertEqual(len(result["segments"]), 2)
        self.assertEqual(result["upper_runs"][0]["state_values"], [1, 65537])
        self.assertEqual(result["upper_runs"][0]["lower_motion_values"], [[0, 0], [0, 3]])

    def test_comparison_motifs_never_cross_lost_actor(self):
        result = self.analyze("lost_actor")
        self.assertEqual(temporal.compare_captures([result])["repeated_motifs"], [])

    def test_comparison_keeps_distinct_lower_body_and_state_signatures(self):
        result = temporal.analyze_records(*records([
            {"upper": [0, 0], "lower": [0, 1]}, {"upper": [0, 0], "lower": [0, 2], "state": 65537}]))
        comparison = temporal.compare_captures([result])
        self.assertEqual(len(comparison["segment_signatures"]), 2)
        self.assertEqual(len(comparison["signatures"]), 1)

    def test_repeated_process_identity_event_breaks_continuity(self):
        result = temporal.analyze_records(*records([
            {"stage": "process.identity"}, {"upper": [3, 1]},
            {"stage": "process.identity"}, {"upper": [3, 2]}]))
        self.assertEqual(result["counts"]["blocks"], 2)
        self.assertNotIn("chained_motion_candidate", result["counts"]["candidate_kinds"])

    def test_hypothetical_event_output_order_is_temporal_and_has_identity(self):
        result = self.analyze("chained_candidates")
        candidates = result["candidate_events"]
        self.assertEqual([c["start_ns"] for c in candidates], sorted(c["start_ns"] for c in candidates))
        self.assertTrue(all("actor" in c and "generation" in c for c in candidates))

    def test_deterministic_and_input_not_mutated(self):
        report, events = fixture("chained_candidates")
        saved = copy.deepcopy((report, events))
        a = temporal.analyze_records(report, events)
        self.assertEqual(a, temporal.analyze_records(report, events))
        self.assertEqual((report, events), saved)

    def test_comparison_no_cross_boundary_or_build_motifs_and_duplicate_session_rejected(self):
        a = temporal.analyze_records(*fixture("chained_candidates"), name="a")
        report, events = records(FIXTURES["cases"]["chained_candidates"], session="other")
        b = temporal.analyze_records(report, events, name="b")
        self.assertTrue(temporal.compare_captures([a, b])["repeated_motifs"])
        b["build_sha256"] = "different"
        comparison = temporal.compare_captures([a, b])
        self.assertEqual(comparison["repeated_motifs"], [])
        with self.assertRaises(temporal.CaptureError): temporal.compare_captures([a, a])


class FileTests(unittest.TestCase):
    def test_hash_check_and_export_preserve_source_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "capture"
            write_capture(source, *fixture("chained_candidates"))
            original = {p.name: p.read_bytes() for p in source.iterdir()}
            hashes = {k: hashlib.sha256(v).hexdigest() for k, v in original.items()}
            result = temporal.load_capture(source, expected_hashes=hashes)
            run = cli.export_analysis([result], Path(tmp) / "out")
            for name in ("analysis.json", "timeline.csv", "segments.csv", "transitions.csv", "candidate_events.csv", "boundaries.csv", "transitions.md"):
                self.assertTrue((run / name).is_file())
            with (run / "timeline.csv").open(encoding="utf-8-sig", newline="") as stream:
                self.assertEqual(len(list(csv.DictReader(stream))), result["counts"]["samples"])
            self.assertEqual(original, {p.name: p.read_bytes() for p in source.iterdir()})
            hashes["events.jsonl"] = "0" * 64
            with self.assertRaises(temporal.CaptureError): temporal.load_capture(source, expected_hashes=hashes)
            with self.assertRaises(temporal.CaptureError): temporal.load_capture(source, expected_hashes={})

    def test_export_is_reproducible_and_creates_distinct_directories(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = temporal.analyze_records(*fixture("chained_candidates"))
            first = cli.export_analysis([result], tmp)
            second = cli.export_analysis([result], tmp)
            self.assertNotEqual(first, second)
            self.assertEqual((first / "analysis.json").read_bytes(), (second / "analysis.json").read_bytes())

    def test_duplicate_json_keys_and_nonfinite_json_rejected(self):
        for text in ('{"valid": true, "valid": false}', '{"timer":NaN}', '{"timer":1e309}'):
            with self.assertRaises(temporal.CaptureError): temporal.parse_json(text)
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "capture"
            write_capture(source, *fixture("nonoffensive"))
            (source / "events.jsonl").write_text("", encoding="utf-8")
            (source / "annotations.jsonl").write_text('{"session":"synthetic"}', encoding="utf-8")
            with self.assertRaises(temporal.CaptureError): temporal.load_capture(source)

    def test_cli_refuses_output_inside_input_and_leaves_no_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "capture"
            write_capture(source, *fixture("nonoffensive"))
            original = sorted(p.name for p in source.iterdir())
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(cli.main([str(source), "--output-root", str(source)]), 1)
            self.assertEqual(sorted(p.name for p in source.iterdir()), original)

    def test_csv_formula_text_escaped(self):
        for text in ("=A1", " @something", "+A1", "-cmd"):
            self.assertTrue(cli._csv_cell(text).startswith("'"))
        self.assertEqual(cli._csv_cell(-2), -2)


if __name__ == "__main__":
    unittest.main()
