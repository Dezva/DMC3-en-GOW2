"""Build-specific static gates and candidate actor sampling; never writes memory."""
import hashlib
import math
from pathlib import Path
import struct

from dmc3_memory import ObservationError, read_exact, unpack, valid_pointer


BUILD_SHA256 = "4ae4bb5c83c19a649fc60edc5ca40e7f3ceee6337e4e4275025bfa9caa40c0a0"
DDMK_COMMIT = "0319ae7132a6a822fd4dede2fb7cad484900169f"
ROOTS = {"actor_pool": 0xC90E28, "event_pool": 0xC90E10, "session": 0xC8F250}
SOURCE_ANCHORS = [(0x23918A, bytes.fromhex("75188b431c")),
                  (0x238CCA, bytes.fromhex("0f85920100008b431c"))]


def anchor_manifest():
    return [dict(rva=rva, size=len(code), sha256=hashlib.sha256(code).hexdigest())
            for rva, code in SOURCE_ANCHORS]


def inspect_pe(path):
    path = Path(path)
    before = path.stat()
    if not 256 <= before.st_size <= 64 * 1024 * 1024:
        raise ObservationError("disk_pe", "Executable size outside bounded inspection")
    data = path.read_bytes()
    after = path.stat()
    if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
        raise ObservationError("disk_changed", "Executable changed while being read")
    try:
        if data[:2] != b"MZ":
            raise ValueError("Missing MZ")
        pe = struct.unpack_from("<I", data, 60)[0]
        if data[pe:pe + 4] != b"PE\0\0":
            raise ValueError("Missing PE signature")
        machine, count, timestamp = struct.unpack_from("<HHI", data, pe + 4)
        optional_size = struct.unpack_from("<H", data, pe + 20)[0]
        if machine != 0x8664 or not 1 <= count <= 96 or optional_size < 112:
            raise ValueError("Expected bounded x64 PE32+")
        if struct.unpack_from("<H", data, pe + 24)[0] != 0x20B:
            raise ValueError("Expected PE32+")
        image_size = struct.unpack_from("<I", data, pe + 24 + 56)[0]
        sections = []
        for index in range(count):
            pos = pe + 24 + optional_size + index * 40
            name, vsize, rva, size, offset = struct.unpack_from("<8sIIII", data, pos)
            flags = struct.unpack_from("<I", data, pos + 36)[0]
            if offset + size > len(data) or rva + max(vsize, size) > image_size:
                raise ValueError("Section extent outside file/image")
            sections.append(dict(name=name.rstrip(b"\0").decode("ascii", "replace"), rva=rva,
                                 virtual_size=vsize, raw_size=size, raw_offset=offset, flags=flags))
    except (struct.error, ValueError) as error:
        raise ObservationError("disk_pe", str(error)) from error
    return dict(sha256=hashlib.sha256(data).hexdigest(), bytes=len(data), machine=machine,
                timestamp=timestamp, image_size=image_size, pe_offset=pe, sections=sections), data


def derive_profile(path, inspected=None):
    metadata, data = inspected if inspected is not None else inspect_pe(path)
    if metadata["sha256"] != BUILD_SHA256:
        raise ObservationError("profile_incompatible", "Different executable build; no prior RVA applied",
                               expected=BUILD_SHA256, actual=metadata["sha256"], actual_build=metadata)
    for rva, expected in SOURCE_ANCHORS:
        section = next((s for s in metadata["sections"] if s["rva"] <= rva
                        and rva + len(expected) <= s["rva"] + s["raw_size"]
                        and s["flags"] & 0x20000000), None)
        if section is None:
            raise ObservationError("static_profile", "Source anchor outside executable section")
        offset = section["raw_offset"] + rva - section["rva"]
        if data[offset:offset + len(expected)] != expected:
            raise ObservationError("static_profile", "DDMK source instruction anchor differs", rva=rva)
    signatures = []
    # One finite scan of file-backed executable sections on DISK, never live RAM.
    # These are candidate RIP-relative MOV encodings, not a general disassembler.
    for section in metadata["sections"]:
        if not section["flags"] & 0x20000000:
            continue
        code = data[section["raw_offset"]:section["raw_offset"] + section["raw_size"]]
        for pos in range(len(code) - 6):
            if code[pos] not in (0x48, 0x4C) or code[pos + 1] != 0x8B or code[pos + 2] & 0xC7 != 0x05:
                continue
            rva = section["rva"] + pos
            target = rva + 7 + struct.unpack_from("<i", code, pos + 3)[0]
            for name in ("actor_pool", "event_pool"):
                if target == ROOTS[name] and not any(s["root"] == name for s in signatures):
                    signatures.append(dict(root=name, rva=rva, size=7, target_rva=target,
                                           sha256=hashlib.sha256(code[pos:pos + 7]).hexdigest()))
    if not any(s["root"] == "actor_pool" for s in signatures):
        raise ObservationError("static_profile", "Actor root needs a file-backed code reference")
    for rva in ROOTS.values():
        if not any(s["rva"] <= rva and rva + 8 <= s["rva"] + s["virtual_size"]
                   and s["flags"] & 0x80000000 for s in metadata["sections"]):
            raise ObservationError("static_profile", "Source-derived root outside writable PE section", rva=rva)
    return dict(schema_version=1, profile_id="dmc3-hdc-4ae4bb5c-candidate-v1",
                status="candidate_static_only", ddmk_commit=DDMK_COMMIT, build=metadata,
                roots=dict(ROOTS), signatures=signatures, source_anchors=anchor_manifest(),
                root_evidence={name: ("source_and_disk_rip_mov" if any(s["root"] == name for s in signatures)
                                      else "ddmk_source_and_writable_pe_section_only") for name in ROOTS},
                actor_fields={"character_u32": 0x78, "id_u8": 0x118, "clone_u32": 0x11C,
                              "motion_index_group_u8x4": 0x39B0, "motion_timer_f32": 0x3E34,
                              "state_u32": 0x3E64},
                actor_semantics_verified=False, attack_detector=False)


def verify_loaded_image(memory, image, metadata):
    if image["size"] != metadata["image_size"] or not valid_pointer(image["base"], image["size"], 4096):
        raise ObservationError("loaded_image", "Main image base/size mismatch")
    base = image["base"]
    dos = read_exact(memory, base, 64)
    if dos[:2] != b"MZ" or struct.unpack_from("<I", dos, 60)[0] != metadata["pe_offset"]:
        raise ObservationError("loaded_image", "Loaded DOS header differs")
    header = read_exact(memory, base + metadata["pe_offset"], 88)
    if (header[:4] != b"PE\0\0" or struct.unpack_from("<H", header, 4)[0] != metadata["machine"]
            or struct.unpack_from("<H", header, 24)[0] != 0x20B
            or struct.unpack_from("<I", header, 8)[0] != metadata["timestamp"]
            or struct.unpack_from("<I", header, 80)[0] != metadata["image_size"]):
        raise ObservationError("loaded_image", "Loaded PE identity differs")


def verify_profile(memory, image, metadata, profile, *, headers_verified=False):
    # Reject edited or stale profile fields before touching any candidate address.
    if (profile.get("schema_version") != 1 or metadata["sha256"] != BUILD_SHA256
            or profile.get("build") != metadata or profile.get("roots") != ROOTS
            or profile.get("source_anchors") != anchor_manifest()
            or profile.get("actor_fields") != {
                "character_u32": 0x78, "id_u8": 0x118, "clone_u32": 0x11C,
                "motion_index_group_u8x4": 0x39B0, "motion_timer_f32": 0x3E34, "state_u32": 0x3E64}):
        raise ObservationError("profile_incompatible", "Profile/build/layout mismatch; candidate reads refused")
    if not headers_verified:
        verify_loaded_image(memory, image, metadata)
    base = image["base"]
    signatures = profile.get("signatures", [])
    if not 1 <= len(signatures) <= 2 or "actor_pool" not in {s["root"] for s in signatures}:
        raise ObservationError("static_profile", "Missing actor root signature")
    for signature in signatures:
        rva = signature["rva"]
        if (signature["root"] not in ("actor_pool", "event_pool") or signature["size"] != 7 or not any(s["rva"] <= rva and rva + 7 <= s["rva"] + s["raw_size"]
                                               and s["flags"] & 0x20000000 for s in metadata["sections"])):
            raise ObservationError("static_profile", "Signature outside executable file-backed section")
        code = read_exact(memory, base + rva, 7)
        target = rva + 7 + struct.unpack_from("<i", code, 3)[0]
        if (hashlib.sha256(code).hexdigest() != signature["sha256"]
                or target != ROOTS[signature["root"]]):
            raise ObservationError("static_profile", "Loaded code/reference differs; no actor read")
    for anchor in anchor_manifest():
        code = read_exact(memory, base + anchor["rva"], anchor["size"])
        if hashlib.sha256(code).hexdigest() != anchor["sha256"]:
            raise ObservationError("static_profile", "Loaded source anchor differs; no actor read")


class CandidateSampler:
    """Conservative, generation-based candidate data; no action classification."""
    def __init__(self, memory, base):
        self.memory, self.base = memory, base
        self.previous = None
        self.stable = 0
        self.generation = 0
        self.last_timer = None
        self.last_motion = None

    def invalidate(self):
        self.previous = None
        self.stable = 0
        self.last_timer = None
        self.last_motion = None
        self.generation += 1

    def ptr(self, address):
        pointer, = unpack(self.memory, address, "<Q")
        if not valid_pointer(pointer, 8, 8):
            raise ObservationError("actor_unavailable", "Null, misaligned or non-user pointer", at=address)
        return pointer

    def context(self):
        actor_pool = self.ptr(self.base + ROOTS["actor_pool"])
        event_pool = self.ptr(self.base + ROOTS["event_pool"])
        actor = self.ptr(actor_pool + 3 * 8)
        event = self.ptr(event_pool + 8 * 8)
        session = read_exact(self.memory, self.base + ROOTS["session"], 32)
        mission, = struct.unpack_from("<I", session)
        character = session[0x14]
        room, position, mode, subevent, screen, next_screen = unpack(self.memory, event + 0x18, "<6I")
        if not (0 <= mission <= 20 and character == 0 and room <= 4096 and position <= 4096
                and mode == 1 and subevent <= 4096 and screen <= 4096 and next_screen <= 4096):
            raise ObservationError("context_unknown", "Not a conservative Dante MAIN candidate context",
                                   mission=mission, character=character, room=room, event=mode)
        return (actor_pool, event_pool, actor, event, mission, character,
                room, position, mode, subevent, screen, next_screen)

    def sample(self):
        try:
            if not self.memory.alive():
                raise ObservationError("process_lost", "Original process exited or identity changed")
            if not self.memory.foreground():
                raise ObservationError("foreground_lost", "DMC3 is not foreground; no gameplay read")
            before = self.context()
            actor = before[2]
            character, = unpack(self.memory, actor + 0x78, "<I")
            identity = read_exact(self.memory, actor + 0x118, 8)
            actor_id, clone = identity[0], struct.unpack_from("<I", identity, 4)[0]
            motion = tuple(read_exact(self.memory, actor + 0x39B0, 4))
            timer, = unpack(self.memory, actor + 0x3E34, "<f")
            state, = unpack(self.memory, actor + 0x3E64, "<I")
            if character != 0 or actor_id > 3 or clone != 0 or any(g >= 34 for g in motion[1::2]):
                raise ObservationError("actor_identity", "Candidate actor identity/motion range rejected")
            if not math.isfinite(timer) or not 0 <= timer <= 1_000_000:
                raise ObservationError("motion_timer", "Nonfinite or out-of-policy timer; value remains unknown",
                                       value=repr(timer), motion=list(motion), state=state)
            after = self.context()
            if before != after or not self.memory.alive() or not self.memory.foreground():
                raise ObservationError("context_changed", "Process/actor/scene changed during sample")
            if self.previous != before:
                self.invalidate()
                self.previous = before
            self.stable += 1
            # A reset on the same motion may be a loop: record, never call it an attack.
            reset = self.last_motion == motion and self.last_timer is not None and timer < self.last_timer
            self.last_timer, self.last_motion = timer, motion
            return dict(valid=self.stable >= 3, status="candidate_coherent" if self.stable >= 3 else "warming_up",
                        generation=self.generation, actor=actor, character=character, actor_id=actor_id,
                        motion=[dict(index=motion[0], group=motion[1]), dict(index=motion[2], group=motion[3])],
                        motion_timer=timer, state=state, context=list(before[4:]),
                        timer_reset_same_motion=reset, actor_semantics_verified=False, attack_detected=False)
        except ObservationError as error:
            self.invalidate()
            return dict(valid=False, status="invalid", generation=self.generation,
                        error=error.data, actor_semantics_verified=False, attack_detected=False)
