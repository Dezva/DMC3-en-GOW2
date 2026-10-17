"""Offline DMC3 chronology and candidate hypotheses; never opens games or PINE."""
import argparse
import csv
from datetime import datetime
import json
from pathlib import Path
import uuid

from dmc3_temporal import CaptureError, compare_captures, load_capture, parse_json


def _csv_cell(value):
    if isinstance(value, (dict, list, tuple)):
        value = json.dumps(value, ensure_ascii=False, allow_nan=False)
    if isinstance(value, str) and value.lstrip().startswith(("=", "+", "-", "@")):
        return "'" + value
    return value


def _write_csv(path, rows, fields):
    with path.open("x", newline="", encoding="utf-8-sig") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: _csv_cell(v) for k, v in row.items() if k in fields})


def export_analysis(captures, output_root):
    """Create one new directory after input validation. Never writes into captures."""
    comparison = compare_captures(captures)
    output_root = Path(output_root)
    run = output_root / ("dmc3-timeline-" + datetime.now().strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex)
    run.mkdir(parents=True, exist_ok=False)
    bundle = dict(protocol="dmc3-offline-analysis-bundle", schema_version=1, captures=captures,
                  comparison=comparison, authentic_attacks_detected=False, phase2_verified=False,
                  no_game_access=True, pine_repeated=False)
    with (run / "analysis.json").open("x", encoding="utf-8") as stream:
        json.dump(bundle, stream, ensure_ascii=False, indent=2, allow_nan=False)
    fields = {
        "timeline": ["capture", "sequence", "monotonic_ns", "t_seconds", "status", "generation", "block",
                     "accepted", "rejected_reason", "actor_id", "context", "motion", "motion_timer", "state", "state_bits"],
        "segments": ["capture", "segment_id", "block", "generation", "actor_id", "context", "motion", "state",
                     "start_ns", "end_ns", "start_seconds", "end_seconds", "samples", "observed_span_seconds",
                     "left_censored", "right_censored", "onset_bracket_ns", "end_bracket_ns", "timer_min", "timer_max"],
        "transitions": ["capture", "kind", "block", "previous_sequence", "sequence", "time_bracket_ns", "fields",
                        "before_motion", "after_motion", "before_state", "after_state", "before", "after", "evidence_level"],
        "candidate_events": ["capture", "id", "kind", "block", "generation", "context", "start_ns", "end_ns",
                             "start_seconds", "end_seconds", "upper_motion_group_index", "source_sequences", "member_ids",
                             "left_censored", "right_censored", "evidence_level", "uncertainty", "alternatives",
                             "authentic_attack", "impact_generated"],
        "boundaries": ["capture", "sequence", "monotonic_ns", "reasons", "generation", "block", "context", "error"],
    }
    for kind, columns in fields.items():
        rows = [dict(row, capture=capture["name"]) for capture in captures for row in capture[kind]]
        _write_csv(run / (kind + ".csv"), rows, columns)
    lines = ["# DMC3 · análisis offline", "", "Hipótesis sin ataques autenticados; phase2_verified=false.",
             "No hubo acceso a juegos ni repetición PINE. Los CSV vacíos significan sin datos, no estado cero.", ""]
    for capture in captures:
        count = capture["counts"]
        lines.extend([f"## {capture['name']}", "",
                      f"Muestras aceptadas {count['accepted']}/{count['samples']}; bloques {count['blocks']}; "
                      f"segmentos {count['segments']}. Hipótesis: {json.dumps(count['candidate_kinds'])}.",
                      "Timer: " + json.dumps(capture["timer_diagnostics"], ensure_ascii=False), "",
                      "Cambios observados (tiempos acotados entre dos muestras; no tiempos de golpes):", ""])
        for transition in capture["transitions"]:
            low, high = transition["time_bracket_ns"]
            origin = capture["sample_origin_ns"]
            lines.append(f"- {(low-origin)/1e9:.3f}–{(high-origin)/1e9:.3f} s: {transition['kind']}, "
                         f"secuencia {transition['previous_sequence']} → {transition['sequence']}.")
        lines.append("")
    with (run / "transitions.md").open("x", encoding="utf-8") as stream:
        stream.write("\n".join(lines))
    return run


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("captures", nargs="+", type=Path)
    parser.add_argument("--output-root", type=Path, default=Path(r"D:\logs"))
    parser.add_argument("--integrity-manifest", type=Path,
                        help="JSON: captures -> directory name -> filename -> expected SHA-256")
    parser.add_argument("--review", type=Path, action="append", default=[], help="Retrospective context, never automatic labels")
    args = parser.parse_args(argv)
    try:
        if len(args.captures) > 32 or len(args.review) > 8:
            raise CaptureError("Comparison/review budget exceeded")
        output = args.output_root.resolve()
        for capture in args.captures:
            source = capture.resolve()
            if output == source or source in output.parents:
                raise CaptureError("Output root must be outside every historical capture")
        manifest = None
        if args.integrity_manifest:
            if args.integrity_manifest.stat().st_size > 1024 * 1024:
                raise CaptureError("Integrity manifest budget exceeded")
            manifest = parse_json(args.integrity_manifest.read_text(encoding="utf-8-sig"))["captures"]
        captures = []
        for path in args.captures:
            if manifest is not None and path.name not in manifest:
                raise CaptureError(f"Missing expected hashes for {path.name}")
            captures.append(load_capture(path, expected_hashes=None if manifest is None else manifest[path.name], reviews=args.review))
        run = export_analysis(captures, output)
        print(json.dumps(dict(output=str(run), captures=len(captures), phase2_verified=False,
                              authentic_attacks_detected=False), ensure_ascii=False))
        return 0
    except (OSError, ValueError, KeyError, TypeError, UnicodeError) as error:
        print(json.dumps(dict(error=str(error), phase2_verified=False, authentic_attacks_detected=False), ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
