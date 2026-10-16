"""Validate observer logs and summarize candidates; never classify attacks."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path


def analyze(run):
    run = Path(run)
    report_bytes = (run / "report.json").read_bytes()
    event_file = run / "events.jsonl"
    if event_file.stat().st_size > 16 * 1024 * 1024:
        raise ValueError("Event file exceeds the finite observer budget")
    event_bytes = event_file.read_bytes()
    report = json.loads(report_bytes)
    events = [json.loads(line) for line in event_bytes.decode("utf-8").splitlines()]
    if report.get("protocol") != "dmc3-read-only-observer" or report.get("schema_version") != 1:
        raise ValueError("Unknown report protocol/schema")
    if not events or events[-1]["stage"] != "session.result":
        raise ValueError("Capture has no final session.result")
    if [e["sequence"] for e in events] != list(range(1, len(events) + 1)):
        raise ValueError("Missing, duplicate or reordered sequence")
    if any(e["session"] != report["session"] or e.get("schema_version") != 1
           or e.get("protocol") != report["protocol"] for e in events):
        raise ValueError("Mixed session/schema/protocol")
    if any(b["monotonic_ns"] < a["monotonic_ns"] for a, b in zip(events, events[1:])):
        raise ValueError("Monotonic clock moved backwards")
    samples = [e for e in events if e["stage"] == "candidate.sample"]
    valid = [e for e in samples if e["data"]["valid"]]
    if (len(valid) != report["candidate_samples"] or len(samples) - len(valid) != report["invalid_samples"]):
        raise ValueError("Report/sample counters differ")
    start = samples[0]["monotonic_ns"] if samples else report["started_monotonic_ns"]
    changes = []
    last = None
    for event in samples:
        data = event["data"]
        motion = tuple((m["group"], m["index"]) for m in data.get("motion", []))
        key = data["status"], motion, data.get("state"), data.get("error", {}).get("stage")
        if key != last:
            changes.append(dict(t_seconds=(event["monotonic_ns"] - start) / 1e9,
                                status=data["status"], motion_group_index=motion,
                                state=data.get("state"), timer=data.get("motion_timer"), error=data.get("error")))
            last = key
    annotations = []
    annotation_file = run / "annotations.jsonl"
    if annotation_file.exists():
        if annotation_file.stat().st_size > 1024 * 1024:
            raise ValueError("Annotation budget exceeded")
        for line in annotation_file.read_text(encoding="utf-8").splitlines():
            item = json.loads(line)
            if (item.get("session") != report["session"] or item.get("provenance") != "manual_report_unverified"
                    or item["monotonic_ns"] < report["started_monotonic_ns"]
                    or item["monotonic_ns"] > events[-1]["monotonic_ns"]):
                raise ValueError("Annotation outside capture or mixed session")
            annotations.append(item)
    return dict(protocol="dmc3-candidate-summary", schema_version=1,
                report_sha256=hashlib.sha256(report_bytes).hexdigest(),
                events_sha256=hashlib.sha256(event_bytes).hexdigest(),
                integrity="parsed_session_sequence_clock_counters_consistent; hashes are not a signature",
                samples=len(samples), coherent_candidates=len(valid), invalid=len(samples) - len(valid),
                read_calls=report.get("read_calls"), read_bytes=report.get("read_bytes"),
                motions=dict(Counter(str([(m["group"], m["index"]) for m in e["data"]["motion"]]) for e in valid)),
                states=dict(Counter(str(e["data"]["state"]) for e in valid)),
                invalid_reasons=dict(Counter(e["data"].get("error", {}).get("stage", e["data"]["status"])
                                             for e in samples if not e["data"]["valid"])),
                rejected_timer_values=dict(Counter(e["data"].get("error", {}).get("value", "not_recorded")
                                                   for e in samples if e["data"].get("error", {}).get("stage") == "motion_timer")),
                manual_capture_intent=report.get("manual_label"),
                manual_annotations=annotations,
                manual_labels_are_not_observed_action_timestamps=True,
                transitions=changes, phase2_verified=False, attack_detector=False)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", type=Path)
    args = parser.parse_args(argv)
    summary = analyze(args.run)
    with (args.run / "candidate-summary.json").open("x", encoding="utf-8") as out:
        json.dump(summary, out, indent=2, ensure_ascii=False, allow_nan=False)
    print(json.dumps({k: v for k, v in summary.items() if k != "transitions"}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
