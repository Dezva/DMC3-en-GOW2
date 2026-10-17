"""Optional guarded timer observations. Negative timers remain rejected.

Standard library only. Native anchor provenance: docs/dmc3-timer-native.md.
No unit/action meaning is established by this diagnostic.
"""
import hashlib
import math
import struct
import time

from dmc3_memory import ObservationError, read_exact, unpack
from dmc3_profile import (BUILD_SHA256, CandidateSampler, derive_profile, inspect_pe,
                          verify_profile)


FIELDS = {"actor_event_u32": 0x3E08, "phase_u8": 0x3E10, "speed_f32": 0x14}
NATIVE_ANCHORS = [
    (0x1F6F96, 8, "4f86986d6e3189f9766658706b522ffa8054f6ff6e978f7cc17811bde7798596"),
    (0x1F4440, 7, "cce4a02dde017c1badcbddb6cf60c0a72a50e66108f42bad5c4a97e38676703b"),
    (0x1F448E, 24, "cb9ca6259d4ce40decb3c8f0592a29d6eb8e09050c8bb6b78ce2cb03baa18a12"),
]


def diagnostic_manifest():
    return dict(profile_id="dmc3-hdc-4ae4bb5c-timer-diagnostic-v1", schema_version=1,
                fields=dict(FIELDS), native_anchors=[dict(rva=r, size=n, sha256=h) for r, n, h in NATIVE_ANCHORS],
                semantics_verified=False, negative_timer_accepted=False)


def _executable_section(metadata, rva, size):
    if not any(s["flags"] & 0x20000000 and s["rva"] <= rva
               and rva + size <= s["rva"] + min(s["raw_size"], s["virtual_size"])
               for s in metadata["sections"]):
        raise ObservationError("timer_profile", "Native diagnostic anchor outside executable bytes", rva=rva)


def derive_timer_profile(path, inspected=None):
    metadata, data = inspected if inspected is not None else inspect_pe(path)
    profile = derive_profile(path, inspected=(metadata, data))
    for rva, size, expected in NATIVE_ANCHORS:
        _executable_section(metadata, rva, size)
        section = next(s for s in metadata["sections"] if s["rva"] <= rva
                       and rva + size <= s["rva"] + min(s["raw_size"], s["virtual_size"])
                       and s["flags"] & 0x20000000)
        offset = section["raw_offset"] + rva - section["rva"]
        if hashlib.sha256(data[offset:offset + size]).hexdigest() != expected:
            raise ObservationError("timer_profile", "Native diagnostic disk anchor differs", rva=rva)
    profile["timer_diagnostic"] = diagnostic_manifest()
    return profile


def verify_timer_profile(memory, image, metadata, profile, *, headers_verified=False):
    # Reject edited/stale extension before even base-profile memory reads.
    if metadata.get("sha256") != BUILD_SHA256 or profile.get("timer_diagnostic") != diagnostic_manifest():
        raise ObservationError("profile_incompatible", "Timer diagnostic profile/build mismatch")
    verify_profile(memory, image, metadata, profile, headers_verified=headers_verified)
    for rva, size, expected in NATIVE_ANCHORS:
        _executable_section(metadata, rva, size)
        if hashlib.sha256(read_exact(memory, image["base"] + rva, size)).hexdigest() != expected:
            raise ObservationError("timer_profile", "Loaded native diagnostic anchor differs", rva=rva)


class TimerDiagnosticSampler(CandidateSampler):
    """Separate observation quality from legacy acceptance; never accepts -1."""

    def event_phase(self, actor):
        # Includes the four intervening lastEvent bytes, ignored here; no full structure read.
        return struct.unpack("<I4xB", read_exact(self.memory, actor + FIELDS["actor_event_u32"], 9))

    def identity(self, actor):
        character, = unpack(self.memory, actor + 0x78, "<I")
        raw = read_exact(self.memory, actor + 0x118, 8)
        return character, raw[0], struct.unpack_from("<I", raw, 4)[0]

    def sample(self):
        diagnostic = None
        try:
            if not self.memory.alive():
                raise ObservationError("process_lost", "Original process exited or identity changed")
            if not self.memory.foreground():
                raise ObservationError("foreground_lost", "DMC3 is not foreground; no gameplay read")
            began = time.perf_counter_ns()
            before = self.context()
            actor = before[2]
            identity = self.identity(actor)
            first = self.event_phase(actor)
            motion = tuple(read_exact(self.memory, actor + 0x39B0, 4))
            timer, = unpack(self.memory, actor + 0x3E34, "<f")
            state, = unpack(self.memory, actor + 0x3E64, "<I")
            speed, = unpack(self.memory, actor + FIELDS["speed_f32"], "<f")
            character, actor_id, clone = identity
            if character != 0 or actor_id > 3 or clone != 0 or any(g >= 34 for g in motion[1::2]):
                raise ObservationError("actor_identity", "Candidate actor identity/motion range rejected")
            after = self.context()
            if before != after:
                raise ObservationError("context_changed", "Actor/scene changed; no further old-actor reads")
            final_identity = self.identity(actor)
            last = self.event_phase(actor)
            if before != after or identity != final_identity or not self.memory.alive() or not self.memory.foreground():
                raise ObservationError("context_changed", "Process/actor/identity/scene changed during diagnostic")
            ended = time.perf_counter_ns()
            timer_ok = math.isfinite(timer) and 0 <= timer <= 1_000_000
            stable_phase = first == last
            diagnostic = dict(schema_version=1, read_begin_ns=began, read_end_ns=ended,
                              actor_context_rechecked=True, atomic_snapshot=False,
                              actor=actor, actor_id=actor_id, character=character, context=list(before[4:]),
                              event_before=first[0], event_after=last[0], phase_before=first[1], phase_after=last[1],
                              event_phase_stable=stable_phase,
                              speed_f32=speed if math.isfinite(speed) else None, speed_raw_repr=repr(speed),
                              speed_quality="finite_units_unknown" if math.isfinite(speed) else "nonfinite_unknown",
                              timer_raw_f32=timer if math.isfinite(timer) else None, timer_raw_repr=repr(timer),
                              timer_quality="within_existing_policy" if timer_ok else "rejected_unknown",
                              motion=[dict(index=motion[0], group=motion[1]), dict(index=motion[2], group=motion[3])],
                              state=state, motion_state_quality="read_complete_context_rechecked_not_atomic"
                              if stable_phase else "transition_observation_only",
                              semantics_verified=False, attack_detected=False)
            if not stable_phase:
                raise ObservationError("diagnostic_transition", "Actor event/phase changed during reads")
            if not timer_ok:
                raise ObservationError("motion_timer", "Nonfinite or out-of-policy timer; value remains unknown",
                                       value=repr(timer), motion=list(motion), state=state)
            if self.previous != before:
                self.invalidate()
                self.previous = before
            self.stable += 1
            reset = self.last_motion == motion and self.last_timer is not None and timer < self.last_timer
            self.last_timer, self.last_motion = timer, motion
            return dict(valid=self.stable >= 3, status="candidate_coherent" if self.stable >= 3 else "warming_up",
                        generation=self.generation, actor=actor, character=character, actor_id=actor_id,
                        motion=diagnostic["motion"], motion_timer=timer, state=state, context=list(before[4:]),
                        timer_reset_same_motion=reset, timer_diagnostic=diagnostic,
                        actor_semantics_verified=False, attack_detected=False)
        except ObservationError as error:
            self.invalidate()
            result = dict(valid=False, status="invalid", generation=self.generation, error=error.data,
                          actor_semantics_verified=False, attack_detected=False)
            # No fields survive access/identity/context faults. A rejected timer or
            # bracketed transition can retain only this explicitly qualified attempt.
            if diagnostic is not None:
                result["timer_diagnostic"] = diagnostic
            return result
