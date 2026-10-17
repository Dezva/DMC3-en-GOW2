"""Finite external DMC3 observer, Windows x64, standard library, read only.

All gameplay fields remain candidates; no action/attack detector is implemented.
"""
import argparse
import ctypes
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import time
import uuid

from dmc3_memory import ObservationError, WindowsMemory, QUERY_LIMITED, QUERY_READ, read_exact
from dmc3_profile import (BUILD_SHA256, CandidateSampler, derive_profile, inspect_pe,
                          verify_loaded_image, verify_profile)
from dmc3_timer_diagnostic import (TimerDiagnosticSampler, derive_timer_profile,
                                   verify_timer_profile)


DEFAULT_EXE = r"D:\HayJueguitosEnLaCompu\Devil May Cry HD Collection\dmc3.exe"


def utc():
    return datetime.now(timezone.utc).isoformat()


def write_new(path, data):
    with path.open("x", encoding="utf-8") as stream:
        json.dump(data, stream, ensure_ascii=False, indent=2)


def maybe_action_cue(event, planned_seconds, elapsed_seconds, emitted=False, beep=None):
    """One optional instruction cue; never an observed action or game input.

    Bounded synchronous 60 ms tone. Its actual emission is logged, and the
    existing sampler still discards late ticks rather than catching up.
    """
    if emitted or planned_seconds is None or elapsed_seconds < planned_seconds:
        return emitted
    detail = dict(planned_seconds=planned_seconds, actual_elapsed_seconds=elapsed_seconds,
                  frequency_hz=1200, duration_ms=60, cue_only=True, actual_action_unknown=True)
    event("sampling.action_cue.begin", detail)
    if beep is None:
        import winsound
        beep = winsound.Beep
    try:
        beep(1200, 60)
    except OSError:
        event("sampling.action_cue.end", dict(cue_only=True, sound_call_succeeded=False))
        raise
    event("sampling.action_cue.end", dict(cue_only=True, sound_call_succeeded=True,
                                         actual_action_unknown=True))
    return True


def annotate(args):
    run = Path(args.annotate)
    session = json.loads((run / "session.json").read_text(encoding="utf-8"))
    if session.get("protocol") != "dmc3-read-only-observer" or len(args.action or "") not in range(1, 121):
        raise ValueError("A valid observer session and manual action label are required")
    # perf_counter_ns uses the same system clock across processes on Windows.
    stamp = time.perf_counter_ns()
    entry = dict(session=session["session"], utc=utc(), monotonic_ns=stamp,
                 elapsed_ns=stamp - session["started_monotonic_ns"],
                 action=args.action, provenance="manual_report_unverified", attack_detected=False)
    if entry["elapsed_ns"] < 0 or entry["elapsed_ns"] > 600 * 1_000_000_000:
        raise ValueError("Session is stale or belongs to another monotonic clock")
    if (run / "report.json").exists():
        raise ValueError("Capture already completed; historical labels cannot be inserted")
    with (run / "annotations.jsonl").open("a", encoding="utf-8") as out:
        out.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print("Manual annotation saved; no attack inferred.")
    return 0


def capture(args):
    timer_diagnostic = getattr(args, "timer_diagnostic", False)
    profile_only = getattr(args, "profile_only", False)
    run = Path(args.log_root) / ("dmc3-observe-" + datetime.now().strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex)
    run.mkdir(parents=True, exist_ok=False)
    start = time.perf_counter_ns()
    session = dict(protocol="dmc3-read-only-observer", schema_version=1, session=uuid.uuid4().hex,
                   started_utc=utc(), started_monotonic_ns=start, read_only=True)
    write_new(run / "session.json", session)
    report = dict(session, observer_bits=ctypes.sizeof(ctypes.c_void_p) * 8,
                  requested_access=QUERY_READ, access_verified=False, loaded_profile_gates_verified=False,
                  actor_semantics_verified=False, authentic_attacks_detected=False,
                  game_to_game_communication=False, candidate_samples=0, invalid_samples=0,
                  manual_label=args.label, manual_label_provenance="manual_capture_intent_unverified",
                  requires_game_foreground=True,
                  lead_in_seconds=args.lead_in_seconds, audible_cues=args.beep,
                  action_cue_seconds=getattr(args, "action_cue_seconds", None),
                  timer_diagnostic=timer_diagnostic, profile_only=profile_only,
                  scene_detection="observed roots/mission/room/event only; same-context ABA may be missed",
                  errors=[])
    memory = None
    sequence = 0

    def event(stage, data):
        nonlocal sequence
        sequence += 1
        entry = dict(protocol=session["protocol"], schema_version=1, session=session["session"],
                     sequence=sequence, utc=utc(), monotonic_ns=time.perf_counter_ns(), stage=stage, data=data)
        entry["elapsed_ns"] = entry["monotonic_ns"] - start
        with (run / "events.jsonl").open("a", encoding="utf-8") as out:
            out.write(json.dumps(entry, ensure_ascii=False, allow_nan=False) + "\n")

    print("Capture:", run, flush=True)
    success = False
    try:
        event("session.start", dict(mode="access_only" if args.access_only else "profile_only" if profile_only else "candidate_sampling",
                                    hz=args.hz, samples=args.samples))
        inspected = inspect_pe(args.exe)
        metadata = inspected[0]
        report["disk_build"] = metadata
        report["build_matches_known_profile"] = metadata["sha256"] == BUILD_SHA256
        event("disk.identity", dict(sha256=metadata["sha256"], known_build=report["build_matches_known_profile"]))
        if not args.access_only and not report["build_matches_known_profile"]:
            raise ObservationError("profile_incompatible", "Different build; prior RVA not applied",
                                   expected=BUILD_SHA256, actual=metadata["sha256"])
        memory = WindowsMemory()
        report["process"] = memory.discover(args.exe)
        stamp = report["process"]["creation_filetime"]
        report["process"]["started_utc"] = datetime.fromtimestamp((stamp - 116444736000000000) / 1e7, timezone.utc).isoformat()
        limited = memory.open(QUERY_LIMITED, False, report["process"]["pid"])
        if limited:
            try:
                report["tokens"] = dict(observer=memory.token_context(-1), target=memory.token_context(limited))
            except ObservationError as error:
                report["token_query_error"] = error.data
            finally:
                memory.close_handle(limited)
        event("process.identity", dict(process=report["process"], tokens=report.get("tokens")))
        memory.attach(report["process"])
        report["image"] = memory.image()
        verify_loaded_image(memory, report["image"], metadata)
        report["access_verified"] = True
        event("memory.access", dict(verified=True, image=report["image"], candidate_reads=False))
        if not args.access_only:
            # One finite disk scan of this exact build; never a historical PID/base.
            derive = derive_timer_profile if timer_diagnostic else derive_profile
            verify = verify_timer_profile if timer_diagnostic else verify_profile
            profile = derive(args.exe, inspected=inspected)
            write_new(run / "candidate-profile.json", profile)
            event("disk.profile", dict(profile_id=profile["profile_id"], sha256=metadata["sha256"],
                                       status=profile["status"], root_evidence=profile["root_evidence"]))
            verify(memory, report["image"], metadata, profile, headers_verified=True)
            report["loaded_profile_gates_verified"] = True
            event("loaded.profile_gates", dict(verified=True, semantic_validation=False))
            if not profile_only:
                sampler_class = TimerDiagnosticSampler if timer_diagnostic else CandidateSampler
                sampler = sampler_class(memory, report["image"]["base"])
                event("sampling.lead_in", dict(seconds=args.lead_in_seconds,
                                           provenance="operator preparation; not an observed action"))
                if args.lead_in_seconds:
                    time.sleep(args.lead_in_seconds)
                if args.beep:
                    import winsound
                    winsound.Beep(880, 200)
                event("sampling.begin", dict(cue_only=True, actual_action_unknown=True))
                start_capture = time.perf_counter()
                action_cue_emitted = False
                for index in range(args.samples):
                    deadline = start_capture + index / args.hz
                    if time.perf_counter() - deadline > 1 / args.hz:
                        event("sampling.skipped", dict(index=index, reason="late tick discarded; no catch-up burst"))
                        continue
                    delay = deadline - time.perf_counter()
                    if delay > 0:
                        time.sleep(delay)
                    action_cue_emitted = maybe_action_cue(
                        event, getattr(args, "action_cue_seconds", None),
                        time.perf_counter() - start_capture, action_cue_emitted)
                    sample = sampler.sample()
                    report["candidate_samples" if sample["valid"] else "invalid_samples"] += 1
                    event("candidate.sample", sample)
                    if sample.get("error", {}).get("stage") == "process_lost":
                        break
                event("sampling.end", dict(cue_only=True))
                if args.beep:
                    import winsound
                    winsound.Beep(660, 200)
        if not memory.alive():
            raise ObservationError("process_lost", "Process ended before capture completion")
        # Streaming fingerprint again: no file replacement silently accepted.
        with Path(args.exe).open("rb") as source:
            digest = hashlib.file_digest(source, "sha256").hexdigest() if hasattr(hashlib, "file_digest") else _hash(source)
        if digest != metadata["sha256"]:
            raise ObservationError("disk_changed", "Executable fingerprint changed during capture")
        success = args.access_only or profile_only or report["candidate_samples"] > 0
    except ObservationError as error:
        report["errors"].append(error.data)
        event("error", error.data)
    except (OSError, ValueError, KeyError, TypeError) as error:
        detail = dict(stage="observer", message=str(error), winerror=getattr(error, "winerror", None))
        report["errors"].append(detail)
        event("error", detail)
    except KeyboardInterrupt:
        report["errors"].append(dict(stage="interrupted", message="Capture stopped by operator"))
    finally:
        if memory:
            report["read_calls"], report["read_bytes"] = memory.read_calls, memory.read_bytes
            memory.close()
        report["completed_utc"] = utc()
        report["elapsed_ns"] = time.perf_counter_ns() - start
        report["capture_has_coherent_candidates"] = report["candidate_samples"] > 0
        report["phase2_verified"] = False
        report["exit_success"] = success and not report["errors"]
        event("session.result", dict(exit_success=report["exit_success"], phase2_verified=False))
        write_new(run / "report.json", report)
    print(json.dumps({key: report[key] for key in ("access_verified", "candidate_samples", "invalid_samples",
                                                   "phase2_verified", "errors")}, ensure_ascii=False))
    return 0 if report["exit_success"] else 1


def _hash(stream):
    result = hashlib.sha256()
    for block in iter(lambda: stream.read(1024 * 1024), b""):
        result.update(block)
    return result.hexdigest()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--exe", default=DEFAULT_EXE)
    parser.add_argument("--log-root", default=r"D:\logs")
    parser.add_argument("--access-only", action="store_true")
    parser.add_argument("--profile-only", action="store_true", help="Verify disk/loaded profile only; no actor sampling or cues")
    parser.add_argument("--timer-diagnostic", action="store_true", help="Guarded event/phase/speed and rejected-timer observations")
    parser.add_argument("--samples", type=int, default=100)
    parser.add_argument("--hz", type=float, default=10)
    parser.add_argument("--label", default="unlabelled")
    parser.add_argument("--annotate", metavar="RUN_DIRECTORY")
    parser.add_argument("--action")
    parser.add_argument("--lead-in-seconds", type=float, default=0)
    parser.add_argument("--beep", action="store_true", help="Windows audible start/end cues for manual captures")
    parser.add_argument("--action-cue-seconds", type=float, metavar="SECONDS",
                        help="One optional short instruction tone during sampling; requires --beep")
    args = parser.parse_args(argv)
    if args.timer_diagnostic and (args.access_only or args.annotate):
        parser.error("Timer diagnostic requires sampling or --profile-only")
    if args.profile_only and (args.access_only or args.annotate or args.beep or args.lead_in_seconds or args.action_cue_seconds is not None):
        parser.error("Profile-only cannot sample, annotate, prepare or emit cues")
    if not 1 <= args.samples <= 6000 or not 1 <= args.hz <= 20 or args.samples / args.hz > 300:
        parser.error("Use 1–20 Hz, 1–6000 samples and at most 300 seconds")
    if not 0 <= args.lead_in_seconds <= 30:
        parser.error("Preparation delay must be between 0 and 30 seconds")
    if args.action_cue_seconds is not None and (not args.beep or args.access_only or args.annotate
            or not 1 <= args.action_cue_seconds <= args.samples / args.hz - 1):
        parser.error("Action cue requires sampling with --beep, at least 1 s after start and 1 s before end")
    return annotate(args) if args.annotate else capture(args)


if __name__ == "__main__":
    raise SystemExit(main())
