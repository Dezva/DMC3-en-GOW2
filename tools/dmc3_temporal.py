"""Deterministic offline analysis of observer v1 records. No process/IPC access.

Memory values, user declarations and movement hypotheses remain separate.
This module cannot authenticate an attack or produce a damage/impact event.
"""
from collections import Counter, defaultdict
import hashlib
import json
import math
from pathlib import Path

PROTOCOL = "dmc3-read-only-observer"
BUILD_SHA256 = "4ae4bb5c83c19a649fc60edc5ca40e7f3ceee6337e4e4275025bfa9caa40c0a0"
RULE_VERSION = "ddmk-upper-family-hypotheses-v1"
DDMK_COMMIT = "0319ae7132a6a822fd4dede2fb7cad484900169f"
MAX_BYTES = 16 * 1024 * 1024


class CaptureError(ValueError):
    """Malformed/ambiguous input is refused, never silently repaired/sorted."""


def _integer(value, low=0, high=2**63 - 1):
    return type(value) is int and low <= value <= high


def _number(value, low=0, high=1_000_000):
    return type(value) in (int, float) and math.isfinite(value) and low <= value <= high


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise CaptureError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def parse_json(text):
    def finite_float(value):
        number = float(value)
        if not math.isfinite(number):
            raise CaptureError("JSON float exceeds finite range")
        return number

    try:
        return json.loads(text, object_pairs_hook=_unique_object,
                          parse_float=finite_float,
                          parse_constant=lambda x: (_ for _ in ()).throw(CaptureError(f"Nonfinite JSON: {x}")))
    except (ValueError, TypeError) as error:
        raise CaptureError(str(error)) from error


def _read(path, limit=MAX_BYTES):
    path = Path(path)
    if path.stat().st_size > limit:
        raise CaptureError(f"File exceeds budget: {path.name}")
    data = path.read_bytes()
    if len(data) > limit:
        raise CaptureError(f"File grew beyond budget: {path.name}")
    return data


def load_capture(run, *, expected_hashes=None, reviews=()):
    """Only reads files. Expected hashes come from a previously retained audit."""
    run = Path(run)
    if expected_hashes is not None and (not isinstance(expected_hashes, dict)
            or not {"report.json", "events.jsonl"} <= expected_hashes.keys()):
        raise CaptureError("Integrity manifest must cover report.json and events.jsonl")
    sources = {}
    contents = {}
    for name in ("report.json", "events.jsonl", "session.json", "candidate-profile.json", "manual-review.json",
                 "annotations.jsonl"):
        path = run / name
        if not path.exists() and name not in ("report.json", "events.jsonl"):
            continue
        data = _read(path)
        sources[name] = hashlib.sha256(data).hexdigest()
        contents[name] = data.decode("utf-8-sig")
    for name, expected in (expected_hashes or {}).items():
        if name not in {"report.json", "events.jsonl", "session.json", "candidate-profile.json",
                        "manual-review.json", "candidate-summary.json", "annotations.jsonl"}:
            raise CaptureError("Unexpected integrity-manifest filename")
        actual = sources.get(name)
        if actual is None:
            actual = hashlib.sha256(_read(run / name)).hexdigest()
            sources[name] = actual
        if actual != expected:
            raise CaptureError(f"Historical hash mismatch: {run.name}/{name}")
    report = parse_json(contents["report.json"])
    events = [parse_json(line) for line in contents["events.jsonl"].splitlines()]
    if not isinstance(report, dict):
        raise CaptureError("Report must be an object")
    # Validate boundaries before sidecars can reference events[-1] or the clock.
    _validate_envelope(report, events)
    if "session.json" in contents:
        session = parse_json(contents["session.json"])
        if not isinstance(session, dict) or any(session.get(k) != report.get(k) for k in ("session", "protocol", "schema_version")):
            raise CaptureError("session.json and report.json disagree")
    associations = []
    if "manual-review.json" in contents:
        associations.append(dict(evidence_level="user_declaration", source="manual-review.json",
                                 content=parse_json(contents["manual-review.json"])))
    for path in reviews:
        data = _read(path, 2 * 1024 * 1024)
        associations.append(dict(evidence_level="retrospective_review_context", source=Path(path).name,
                                 sha256=hashlib.sha256(data).hexdigest(), content=parse_json(data)))
    if "annotations.jsonl" in contents:
        for line in contents["annotations.jsonl"].splitlines():
            item = parse_json(line)
            if (not isinstance(item, dict) or item.get("session") != report.get("session")
                    or item.get("provenance") != "manual_report_unverified"
                    or not _integer(item.get("monotonic_ns"))
                    or not report["started_monotonic_ns"] <= item["monotonic_ns"] <= events[-1]["monotonic_ns"]):
                raise CaptureError("Manual annotation outside capture/session")
            associations.append(dict(evidence_level="user_declaration", source="annotations.jsonl", content=item))
    result = analyze_records(report, events, name=run.name, associations=associations)
    if "candidate-profile.json" in contents:
        profile = parse_json(contents["candidate-profile.json"])
        if (not isinstance(profile, dict) or not isinstance(profile.get("build"), dict)
                or profile["build"].get("sha256") != report.get("disk_build", {}).get("sha256")
                or profile.get("ddmk_commit") != DDMK_COMMIT
                or profile.get("profile_id") != "dmc3-hdc-4ae4bb5c-candidate-v1"):
            raise CaptureError("Historical profile identity mismatch")
    result["source_hashes"] = sources
    result["integrity"] = dict(structural_checks_passed=True,
                               historical_hashes_checked=sorted(expected_hashes or {}),
                               hashes_are_not_action_authentication=True)
    return result


def _validate_envelope(report, events):
    if (not isinstance(report, dict) or report.get("protocol") != PROTOCOL
            or type(report.get("schema_version")) is not int or report["schema_version"] != 1):
        raise CaptureError("Unsupported report protocol/schema")
    if not isinstance(report.get("session"), str) or not report["session"]:
        raise CaptureError("Missing session")
    if not _integer(report.get("started_monotonic_ns")):
        raise CaptureError("Missing capture clock origin")
    if not isinstance(events, list) or not 2 <= len(events) <= 20000:
        raise CaptureError("Event budget/shape invalid")
    if (not isinstance(events[0], dict) or not isinstance(events[-1], dict)
            or events[0].get("stage") != "session.start" or events[-1].get("stage") != "session.result"):
        raise CaptureError("Capture is incomplete")
    last = report["started_monotonic_ns"]
    samples = []
    starts = results = 0
    for index, event in enumerate(events, 1):
        if (not isinstance(event, dict) or type(event.get("schema_version")) is not int
                or any(event.get(k) != report[k] for k in ("session", "protocol", "schema_version"))):
            raise CaptureError("Mixed protocol/schema/session")
        if type(event.get("sequence")) is not int or event["sequence"] != index:
            raise CaptureError("Duplicate, missing or out-of-order sequence")
        stamp = event.get("monotonic_ns")
        if not _integer(stamp) or stamp < last or not isinstance(event.get("data"), dict):
            raise CaptureError("Invalid clock/order/data")
        if not isinstance(event.get("stage"), str):
            raise CaptureError("Missing stage")
        starts += event["stage"] == "session.start"
        results += event["stage"] == "session.result"
        if "error" in event["data"] and (not isinstance(event["data"]["error"], dict)
                or not isinstance(event["data"]["error"].get("stage"), str)):
            raise CaptureError("Invalid error record")
        last = stamp
        if event["stage"] == "candidate.sample":
            if type(event["data"].get("valid")) is not bool:
                raise CaptureError("Missing/ambiguous validity flag")
            if samples and stamp <= samples[-1]["monotonic_ns"]:
                raise CaptureError("Duplicate or out-of-order sample time")
            samples.append(event)
    if len(samples) > 6000:
        raise CaptureError("Sample budget exceeded")
    if starts != 1 or results != 1:
        raise CaptureError("Repeated session boundary")
    count = sum(e["data"]["valid"] for e in samples)
    if (not _integer(report.get("candidate_samples"), 0, 6000)
            or not _integer(report.get("invalid_samples"), 0, 6000)
            or (count, len(samples) - count) != (report["candidate_samples"], report["invalid_samples"])):
        raise CaptureError("Report counters differ")
    hz = events[0]["data"].get("hz")
    if not _number(hz, 1, 20):
        raise CaptureError("Unknown sampling cadence; no implicit 10 Hz assumption")
    if not isinstance(report.get("disk_build", {}), dict):
        raise CaptureError("Invalid build record")
    return samples, round(1e9 / hz)


def _invalid_candidate(data):
    if data.get("status") != "candidate_coherent":
        return "inconsistent_status"
    if (not _integer(data.get("generation")) or not _integer(data.get("actor"), 0x10000, 0x7FFFFFFFFFFF)
            or data["actor"] % 8 or data.get("character") != 0
            or type(data.get("character")) is not int or not _integer(data.get("actor_id"), 0, 3)):
        return "identity_incomplete_or_invalid"
    context = data.get("context")
    if (not isinstance(context, list) or len(context) != 8 or not all(_integer(v, 0, 4096) for v in context)
            or context[0] > 20 or context[1] != 0 or context[4] != 1):
        return "context_incomplete_or_invalid"
    motion = data.get("motion")
    if (not isinstance(motion, list) or len(motion) != 2 or any(not isinstance(m, dict)
            or not _integer(m.get("group"), 0, 33) or not _integer(m.get("index"), 0, 255) for m in motion)):
        return "motion_incomplete_or_invalid"
    if not _integer(data.get("state"), 0, 0xFFFFFFFF):
        return "state_incomplete_or_invalid"
    if not _number(data.get("motion_timer")):
        return "timer_unknown_or_invalid"
    return None


def _motion(row):
    return tuple((m["group"], m["index"]) for m in row["motion"])


def _state_bits(state):
    return dict(source_floor_bit=bool(state & 1), source_air_bit=bool(state & 2),
                source_busy_bit=bool(state & 0x10000), unknown_bits=state & ~0x10003)


def _segments(rows, *, upper_only=False):
    segments = []
    previous = None
    for row in rows:
        key = (row["block"], _motion(row)[1]) if upper_only else (row["block"], _motion(row), row["state"])
        if key != previous:
            segments.append(dict(block=row["block"], generation=row["generation"], actor=row["actor"],
                                 actor_id=row["actor_id"], context=row["context"], motion=row["motion"],
                                 state=row["state"], state_bits=_state_bits(row["state"]),
                                 start_ns=row["monotonic_ns"], end_ns=row["monotonic_ns"],
                                 start_seconds=row["t_seconds"], end_seconds=row["t_seconds"],
                                 start_sequence=row["sequence"], end_sequence=row["sequence"], samples=0,
                                 timer_min=row["motion_timer"], timer_max=row["motion_timer"],
                                 state_values=[], lower_motion_values=[],
                                 evidence_level="memory_observation"))
        item = segments[-1]
        item.update(end_ns=row["monotonic_ns"], end_seconds=row["t_seconds"], end_sequence=row["sequence"])
        item["samples"] += 1
        if row["state"] not in item["state_values"]:
            item["state_values"].append(row["state"])
        if list(_motion(row)[0]) not in item["lower_motion_values"]:
            item["lower_motion_values"].append(list(_motion(row)[0]))
        item["timer_min"] = min(item["timer_min"], row["motion_timer"])
        item["timer_max"] = max(item["timer_max"], row["motion_timer"])
        previous = key
    for index, item in enumerate(segments):
        before = segments[index - 1] if index else None
        after = segments[index + 1] if index + 1 < len(segments) else None
        item["segment_id"] = index + 1
        item["left_censored"] = before is None or before["block"] != item["block"]
        item["right_censored"] = after is None or after["block"] != item["block"]
        item["onset_bracket_ns"] = None if item["left_censored"] else [before["end_ns"], item["start_ns"]]
        item["end_bracket_ns"] = None if item["right_censored"] else [item["end_ns"], after["start_ns"]]
        item["observed_span_seconds"] = (item["end_ns"] - item["start_ns"]) / 1e9
    return segments


def _family(group, index):
    # DDMK Vars enum + IsWeaponActive upper-body heuristic, NOT attack semantics.
    # Conservative extra index>0 gate also applied to style families.
    if index == 0:
        return None
    if group in range(3, 8) or group in range(13, 18):
        return "melee_motion_candidate"
    if (group in range(8, 13) or group in range(18, 23)) and not (group == 8 and index in (2, 4, 5)):
        return "ranged_motion_candidate"
    return None


def detect_candidates(upper_runs, *, compatible_profile):
    """Offline hypothesis API. Inputs are trusted output of analyze_records only.

    No names of moves, button detection, completion, hit counts or damage.
    Chaining requires adjacent distinct upper motions without a missing sample.
    """
    if not compatible_profile:
        return []
    result = []
    chain = []

    def finish_chain():
        if len(chain) >= 2:
            result.append(dict(kind="chained_motion_candidate", member_ids=[v["id"] for v in chain],
                               id="chain-" + chain[0]["id"], generation=chain[0]["generation"], actor=chain[0]["actor"],
                               block=chain[0]["block"], context=chain[0]["context"],
                               start_ns=chain[0]["start_ns"], end_ns=chain[-1]["end_ns"],
                               evidence_level="movement_hypothesis", combo_completed=None,
                               uncertainty="Adjacent source-family motions; not a validated combo",
                               alternatives=["weapon/style transition", "interrupted sequence", "missed intervening motion"],
                               authentic_attack=False, impact_generated=False))
        chain.clear()

    for run in upper_runs:
        group, index = _motion(run)[1]
        family = _family(group, index)
        if not family:
            finish_chain()
            continue
        if chain and (run["block"] != chain[-1]["block"] or family != chain[-1]["kind"] or len(chain) >= 32):
            finish_chain()
        candidate = dict(id=f"motion-{run['segment_id']}", kind=family,
                         block=run["block"], generation=run["generation"], context=run["context"],
                         actor=run["actor"],
                         start_ns=run["start_ns"], end_ns=run["end_ns"],
                         start_seconds=run["start_seconds"], end_seconds=run["end_seconds"],
                         source_sequences=[run["start_sequence"], run["end_sequence"]],
                         upper_motion_group_index=[group, index], samples=run["samples"],
                         left_censored=run["left_censored"], right_censored=run["right_censored"],
                         onset_bracket_ns=run["onset_bracket_ns"], end_bracket_ns=run["end_bracket_ns"],
                         evidence_level="movement_hypothesis", confidence="unvalidated",
                         rule_version=RULE_VERSION, action_name=None, authentic_attack=False, impact_generated=False,
                         uncertainty="Source weapon-family heuristic; no independent action timing or impact",
                         alternatives=["weapon handling/recovery", "nonoffensive animation in same family",
                                       "sampling missed a transition", "actor/profile semantics still candidate"])
        result.append(candidate)
        chain.append(candidate)
    finish_chain()
    result.sort(key=lambda item: (item["start_ns"], item["kind"], item.get("id", "")))
    return result


def analyze_records(report, events, *, name="capture", associations=()):
    """Strict input order, deterministic result, no I/O. Never consumes labels as features."""
    samples, period = _validate_envelope(report, events)
    origin = samples[0]["monotonic_ns"] if samples else report["started_monotonic_ns"]
    rows, accepted, boundaries, transitions, cues = [], [], [], [], []
    previous = None
    previous_sample = None
    max_generation = -1
    block = 0
    pending = []
    process_seen = False
    for event in events:
        stage, data, stamp = event["stage"], event["data"], event["monotonic_ns"]
        if stage.startswith("sampling.") or stage == "operator.annotation":
            cues.append(dict(sequence=event["sequence"], monotonic_ns=stamp, stage=stage,
                             evidence_level="operator_cue_or_declaration", data=data,
                             observed_action_time=False))
        if stage == "sampling.skipped":
            pending.append("skipped_tick")
        if stage == "process.identity":
            if process_seen:
                pending.append("process_identity_event")
            process_seen = True
        if stage != "candidate.sample":
            continue
        generation = data.get("generation")
        row = dict(sequence=event["sequence"], monotonic_ns=stamp, t_seconds=(stamp - origin) / 1e9,
                   status=data.get("status"), generation=generation, block=None,
                   evidence_level="memory_observation", accepted=False, raw=data)
        reasons = list(pending)
        pending.clear()
        if previous_sample is not None and stamp - previous_sample > 2.5 * period:
            reasons.append("sampling_gap")
        if not _integer(generation) or generation < max_generation:
            invalid = "generation_missing_or_regressed"
        elif not data["valid"]:
            invalid = data.get("error", {}).get("stage", data.get("status", "invalid"))
            if not isinstance(invalid, str) or not invalid:
                invalid = "unusable_invalid_sample"
        else:
            invalid = _invalid_candidate(data)
        if previous_sample is not None and stamp - previous_sample < period / 4:
            invalid = "sample_too_close_to_previous"
        if _integer(generation):
            max_generation = max(max_generation, generation)
        previous_sample = stamp
        if invalid:
            row["rejected_reason"] = invalid
            reasons.append(invalid)
            previous = None
        else:
            row.update({k: data[k] for k in ("actor", "actor_id", "character", "context", "motion", "motion_timer", "state")})
            key = (generation, data["actor"], data["actor_id"], tuple(data["context"]))
            old_key = None if previous is None else (previous["generation"], previous["actor"],
                                                     previous["actor_id"], tuple(previous["context"]))
            if key != old_key:
                reasons.append("context_actor_or_generation" if previous else "start_or_recovery")
            if reasons:
                block += 1
                previous = None
            row.update(accepted=True, block=block, state_bits=_state_bits(row["state"]))
            if previous is not None:
                fields = [k for k in ("motion", "state") if row[k] != previous[k]]
                if fields:
                    transitions.append(dict(kind="observed_change", fields=fields, block=block,
                                            previous_sequence=previous["sequence"], sequence=row["sequence"],
                                            time_bracket_ns=[previous["monotonic_ns"], stamp],
                                            before_motion=previous["motion"], after_motion=row["motion"],
                                            before_state=previous["state"], after_state=row["state"],
                                            evidence_level="memory_observation"))
                if _motion(previous) == _motion(row) and row["motion_timer"] < previous["motion_timer"]:
                    transitions.append(dict(kind="timer_decrease_same_motion", block=block,
                                            previous_sequence=previous["sequence"], sequence=row["sequence"],
                                            time_bracket_ns=[previous["monotonic_ns"], stamp],
                                            before=previous["motion_timer"], after=row["motion_timer"],
                                            evidence_level="memory_observation", animation_restart_verified=False))
            accepted.append(row)
            previous = row
        if reasons:
            boundaries.append(dict(sequence=row["sequence"], monotonic_ns=stamp, reasons=reasons,
                                   generation=generation, block=row["block"], context=data.get("context"),
                                   error=data.get("error"), evidence_level="memory_observation"))
        rows.append(row)
    segments = _segments(accepted)
    upper_runs = _segments(accepted, upper_only=True)
    compatible = (report.get("disk_build", {}).get("sha256") == BUILD_SHA256
                  and report.get("loaded_profile_gates_verified") is True)
    candidates = detect_candidates(upper_runs, compatible_profile=compatible)
    timers = Counter(str(row["motion_timer"]) for row in accepted)
    rejected_timers = Counter(row["raw"].get("error", {}).get("value", "not_recorded") for row in rows
                             if row.get("rejected_reason") in ("motion_timer", "timer_unknown_or_invalid"))
    hypotheses = []
    if len(timers) == 1 and accepted:
        hypotheses.append(dict(kind="timer_semantics_unresolved", evidence_level="movement_hypothesis",
                               evidence=dict(constant_value=next(iter(timers)), samples=len(accepted)),
                               statement="A constant field cannot establish elapsed animation progress here",
                               alternatives=["control/sentinel value", "timer unrelated to these motions",
                                             "source layout or semantic mismatch on native build"],
                               elapsed_animation_time_verified=False))
    if rejected_timers:
        hypotheses.append(dict(kind="rejected_timer_semantics_unresolved", evidence_level="movement_hypothesis",
                               evidence=dict(values=dict(rejected_timers)),
                               statement="Rejected values are preserved; neither attacks nor actor loss are inferred",
                               alternatives=["native sentinel", "transient read between frames", "field semantic mismatch"],
                               sentinel_meaning_verified=False))
    return dict(protocol="dmc3-offline-temporal-analysis", schema_version=1, name=name,
                session=report["session"], build_sha256=report.get("disk_build", {}).get("sha256"),
                historical_process_identity=report.get("process"),
                period_ns=period, sample_origin_ns=origin, rule_version=RULE_VERSION,
                compatible_source_rules=compatible, timeline=rows, segments=segments, upper_runs=upper_runs,
                boundaries=boundaries, transitions=transitions, cues=cues, candidate_events=candidates,
                hypotheses=hypotheses,
                manual_capture_intent=dict(evidence_level="user_declaration", value=report.get("manual_label"),
                                           observed_action_timestamps=False), manual_associations=list(associations),
                timer_diagnostics=dict(accepted_value_counts=dict(timers), rejected_value_counts=dict(rejected_timers),
                                       constant_in_accepted_samples=len(timers) == 1 and bool(accepted),
                                       elapsed_animation_time_verified=False),
                counts=dict(samples=len(rows), accepted=len(accepted), rejected=len(rows) - len(accepted),
                            blocks=block, segments=len(segments), upper_runs=len(upper_runs),
                            candidate_kinds=dict(Counter(c["kind"] for c in candidates))),
                limitations=["10 Hz historical captures may miss short transitions; use recorded cadence",
                             "No atomic snapshot or same-context ABA guarantee", "Source family is not an attack",
                             "Unlabelled intervals cannot establish combo completion or hits"],
                authenticated_actions=[], authentic_attacks_detected=False, phase2_verified=False,
                impact_events=[])


def compare_captures(captures):
    """Exact raw motifs, never merges clocks, actors, generations or builds."""
    if len({c["session"] for c in captures}) != len(captures):
        raise CaptureError("Duplicate capture session in comparison")
    signatures = defaultdict(list)
    stable_signatures = defaultdict(list)
    motifs = defaultdict(list)
    for capture in captures:
        for segment in capture["segments"]:
            key = capture["build_sha256"], _motion(segment), segment["state"]
            stable_signatures[key].append(dict(capture=capture["name"], block=segment["block"],
                                                start_seconds=segment["start_seconds"],
                                                span_seconds=segment["observed_span_seconds"], samples=segment["samples"]))
        for run in capture["upper_runs"]:
            token = _motion(run)[1]
            signatures[(capture["build_sha256"], token)].append(dict(
                capture=capture["name"], block=run["block"], start_seconds=run["start_seconds"],
                span_seconds=run["observed_span_seconds"], samples=run["samples"]))
        for width in (2, 3):
            runs = capture["upper_runs"]
            for start in range(len(runs) - width + 1):
                window = runs[start:start + width]
                if len({v["block"] for v in window}) != 1:
                    continue
                token = tuple(_motion(v)[1] for v in window)
                motifs[(capture["build_sha256"], token)].append(dict(
                    capture=capture["name"], block=window[0]["block"],
                    start_seconds=window[0]["start_seconds"], end_seconds=window[-1]["end_seconds"]))
    return dict(segment_signatures=[dict(build_sha256=key[0], motion_group_index=key[1], state=key[2], occurrences=value)
                                    for key, value in sorted(stable_signatures.items(), key=lambda x: repr(x[0]))],
                signatures=[dict(build_sha256=key[0], upper_motion_group_index=key[1], occurrences=value)
                            for key, value in sorted(signatures.items(), key=lambda x: repr(x[0]))],
                repeated_motifs=[dict(build_sha256=key[0], upper_motion_sequence=key[1], occurrences=value,
                                     evidence_level="raw_pattern_hypothesis", action_name=None,
                                     uncertainty="Same raw IDs do not establish same action or combo")
                                 for key, value in sorted(motifs.items(), key=lambda x: repr(x[0])) if len(value) >= 2],
                authentic_attacks_detected=False, phase2_verified=False)
