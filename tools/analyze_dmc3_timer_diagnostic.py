"""Offline qualified timer observations. Never promotes rejected gameplay samples."""
import argparse
from collections import Counter
import csv
from datetime import datetime
import hashlib
import json
import math
from pathlib import Path
import uuid

from dmc3_temporal import CaptureError, load_capture, parse_json
from dmc3_timer_diagnostic import diagnostic_manifest
from dmc3_profile import BUILD_SHA256


def integer(value, low=0, high=0xFFFFFFFF):
    return type(value) is int and low <= value <= high


def finite(value):
    return type(value) in (int, float) and math.isfinite(value)


def qualified_row(row, start_ns):
    result = dict(sequence=row["sequence"], t_seconds=row["t_seconds"], generation=row["generation"],
                  sample_valid=row["accepted"], status=row["status"],
                  error_stage=row["raw"].get("error", {}).get("stage"), diagnostic_present=False)
    d = row["raw"].get("timer_diagnostic")
    if d is None:
        if row["accepted"]:
            raise CaptureError("Accepted diagnostic-mode sample is missing its diagnostic")
        return result
    if (not isinstance(d, dict) or type(d.get("schema_version")) is not int or d.get("schema_version") != 1
            or d.get("actor_context_rechecked") is not True or d.get("atomic_snapshot") is not False
            or d.get("semantics_verified") is not False or d.get("attack_detected") is not False
            or not integer(d.get("read_begin_ns"), start_ns, row["monotonic_ns"])
            or not integer(d.get("read_end_ns"), d["read_begin_ns"], row["monotonic_ns"])
            or not integer(d.get("actor"), 0x10000, 0x7FFFFFFFFFFF) or d["actor"] % 8
            or not integer(d.get("actor_id"), 0, 3) or not integer(d.get("character"), 0, 0)
            or not all(integer(d.get(k)) for k in ("event_before", "event_after"))
            or not all(integer(d.get(k), 0, 255) for k in ("phase_before", "phase_after"))):
        raise CaptureError("Malformed timer diagnostic identity/quality/window")
    context = d.get("context")
    motion = d.get("motion")
    if (not isinstance(context, list) or len(context) != 8 or not integer(context[0], 0, 20)
            or context[1] != 0 or context[4] != 1 or not all(integer(x, 0, 4096) for x in context)
            or not isinstance(motion, list) or len(motion) != 2
            or not all(isinstance(m, dict) and integer(m.get("index"), 0, 255)
                       and integer(m.get("group"), 0, 33) for m in motion)
            or not integer(d.get("state"))):
        raise CaptureError("Malformed timer diagnostic context/motion/state")
    stable = (d["event_before"], d["phase_before"]) == (d["event_after"], d["phase_after"])
    if (d.get("event_phase_stable") is not stable or d.get("motion_state_quality") !=
            ("read_complete_context_rechecked_not_atomic" if stable else "transition_observation_only")):
        raise CaptureError("Inconsistent timer diagnostic phase quality")
    timer, speed = d.get("timer_raw_f32"), d.get("speed_f32")
    for value, raw in ((timer, d.get("timer_raw_repr")), (speed, d.get("speed_raw_repr"))):
        if not ((finite(value) and raw == repr(value)) or (value is None and raw in ("nan", "inf", "-inf"))):
            raise CaptureError("Inconsistent finite/unknown diagnostic scalar")
    timer_ok = finite(timer) and 0 <= timer <= 1_000_000
    if (d.get("timer_quality") != ("within_existing_policy" if timer_ok else "rejected_unknown")
            or d.get("speed_quality") != ("finite_units_unknown" if finite(speed) else "nonfinite_unknown")
            or (row["accepted"] and (not stable or not timer_ok))):
        raise CaptureError("Diagnostic must not accept unknown timer/phase")
    if (not stable and result["error_stage"] != "diagnostic_transition") or (
            stable and not timer_ok and result["error_stage"] != "motion_timer"):
        raise CaptureError("Diagnostic rejection reason disagrees")
    if row["accepted"] and any(d[key] != row[key] for key in ("actor", "actor_id", "context", "motion", "state")):
        raise CaptureError("Diagnostic and accepted sample disagree")
    if row["accepted"] and timer != row["motion_timer"]:
        raise CaptureError("Diagnostic and accepted timer disagree")
    result.update(diagnostic_present=True, actor=d["actor"], context=context,
                  read_begin_ns=d["read_begin_ns"], read_end_ns=d["read_end_ns"],
                  event_before=d["event_before"], event_after=d["event_after"],
                  phase_before=d["phase_before"], phase_after=d["phase_after"],
                  event_phase_stable=stable, speed=speed, speed_quality=d["speed_quality"],
                  timer_raw=timer, timer_quality=d["timer_quality"], motion=motion, state=d["state"],
                  atomic_snapshot=False, semantics_verified=False)
    return result


def analyze(run):
    run = Path(run)
    capture = load_capture(run)
    if capture["build_sha256"] != BUILD_SHA256:
        raise CaptureError("Different diagnostic build; prior interpretation refused")
    sidecars = {}
    for name in ("report.json", "candidate-profile.json"):
        if (run / name).stat().st_size > 16 * 1024 * 1024:
            raise CaptureError("Diagnostic sidecar exceeds budget")
        raw = (run / name).read_bytes()
        if len(raw) > 16 * 1024 * 1024 or hashlib.sha256(raw).hexdigest() != capture["source_hashes"].get(name):
            raise CaptureError("Missing or changed diagnostic sidecar")
        sidecars[name] = parse_json(raw.decode("utf-8-sig"))
    report = sidecars["report.json"]
    if (report.get("timer_diagnostic") is not True or report.get("loaded_profile_gates_verified") is not True
            or sidecars["candidate-profile.json"].get("timer_diagnostic") != diagnostic_manifest()):
        raise CaptureError("Not a verified timer diagnostic profile")
    if not capture["timeline"]:
        raise CaptureError("No actor samples; profile-only is not gameplay evidence")
    rows = [qualified_row(r, report["started_monotonic_ns"]) for r in capture["timeline"]]
    return dict(protocol="dmc3-qualified-timer-review", capture=capture["name"],
                source_hashes=capture["source_hashes"], rows=rows,
                samples=len(rows), accepted_gameplay_samples=capture["counts"]["accepted"],
                rejected_gameplay_samples=capture["counts"]["rejected"],
                diagnostic_missing=sum(not r["diagnostic_present"] for r in rows),
                timer_rejections_with_context=sum(r["diagnostic_present"] and r["timer_quality"] == "rejected_unknown" for r in rows),
                transitions_during_read=sum(r["diagnostic_present"] and not r["event_phase_stable"] for r in rows),
                event_phase_counts=dict(Counter(str((r["event_before"], r["phase_before"])) for r in rows
                                               if r["diagnostic_present"] and r["event_phase_stable"])),
                no_game_access=True, timer_policy_changed=False, negative_cause_verified=False,
                timer_units_verified=False, phase2_verified=False, authentic_attacks_detected=False,
                limitations=["Qualified diagnostic attempts are not accepted gameplay samples",
                             "Rows remain separate; no bridging invalidation/gaps or inferring native input times",
                             "Context and event brackets are not an atomic snapshot; same-value ABA can be missed",
                             "Finite speed and raw event/phase values do not validate their semantics"])


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("capture", type=Path)
    parser.add_argument("--output-root", type=Path, default=Path(r"D:\logs"))
    args = parser.parse_args(argv)
    try:
        if args.output_root.resolve() == args.capture.resolve() or args.capture.resolve() in args.output_root.resolve().parents:
            raise CaptureError("Output must be outside the original capture")
        result = analyze(args.capture)
        run = args.output_root / ("dmc3-timer-review-" + datetime.now().strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex)
        run.mkdir(parents=True, exist_ok=False)
        with (run / "analysis.json").open("x", encoding="utf-8") as stream:
            json.dump(result, stream, ensure_ascii=False, indent=2, allow_nan=False)
        columns = list(dict.fromkeys(key for row in result["rows"] for key in row))
        with (run / "observations.csv").open("x", encoding="utf-8-sig", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=columns)
            writer.writeheader()
            for row in result["rows"]:
                values = {k: json.dumps(v) if isinstance(v, (dict, list)) else v for k, v in row.items()}
                values = {k: "'" + v if isinstance(v, str) and v.lstrip().startswith(("=", "+", "-", "@")) else v for k, v in values.items()}
                writer.writerow(values)
        print(json.dumps(dict(output=str(run), samples=result["samples"], phase2_verified=False)))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(json.dumps(dict(error=str(error), phase2_verified=False)))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
