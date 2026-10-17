"""Finite DISK-only x64 references to candidate +0x3E34; no process access.

Capstone is an optional isolated research dependency, never needed by the observer.
Linear decoding and local direct-flow reachability do not establish actor provenance.
"""
import argparse
import bisect
from collections import Counter
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
import math
from pathlib import Path
import struct
import sys
import uuid

from dmc3_profile import BUILD_SHA256, inspect_pe
from dmc3_memory import ObservationError

MAX_FUNCTION = 65536
MAX_TOTAL = 2 * 1024 * 1024
ANCHORS = [(0x20932C, 13, "ecbcdfe1b67c21cb406351b5646398513c4fc2f0be3a3c9cf4fcc259fe13b16f"),
           (0x21F69E, 16, "4abfb7c8c4a44c0e649fd5cdfc35505252185827d5f6f98bab99f1567680e6ad")]


def rva_bytes(meta, data, rva, size, *, executable=False):
    if not isinstance(rva, int) or not isinstance(size, int) or rva < 0 or not 0 < size <= 64 * 1024 * 1024:
        raise ValueError("RVA/size outside bounded inspection")
    candidates = [s for s in meta["sections"]
                  if s["rva"] <= rva and rva + size <= s["rva"] + min(s["raw_size"], s["virtual_size"])
                  and (not executable or s["flags"] & 0x20000000)]
    if len(candidates) != 1:
        raise ValueError("RVA must map uniquely to requested file-backed section")
    section = candidates[0]
    offset = section["raw_offset"] + rva - section["rva"]
    result = data[offset:offset + size]
    if len(result) != size:
        raise ValueError("Partial disk range")
    return result


def require_build_and_anchors(meta, data):
    if meta["sha256"] != BUILD_SHA256:
        raise ValueError("Different build; prior RVA refused")
    for rva, size, expected in ANCHORS:
        if hashlib.sha256(rva_bytes(meta, data, rva, size, executable=True)).hexdigest() != expected:
            raise ValueError("Pinned source anchor differs")


def runtime_ranges(meta, data):
    # PE32+ exception directory, index 3. RUNTIME_FUNCTION contains three u32 RVAs.
    offset = meta["pe_offset"] + 24 + 112 + 3 * 8
    if offset + 8 > len(data):
        raise ValueError("Missing exception directory")
    rva, size = struct.unpack_from("<II", data, offset)
    if not size or size % 12 or size > 1024 * 1024:
        raise ValueError("Invalid bounded exception directory")
    ranges = list(struct.iter_unpack("<III", rva_bytes(meta, data, rva, size)))
    previous_end = 0
    for start, end, unwind in ranges:
        if not start < end or start < previous_end:
            raise ValueError("Unsorted/overlapping runtime ranges")
        rva_bytes(meta, data, start, end - start, executable=True)
        rva_bytes(meta, data, unwind, 4)
        previous_end = end
    return ranges


def local_reachable(instructions, start, cs):
    """Only direct flow inside this range. Indirect/outside edges stay unknown."""
    indexed = {x.address: x for x in instructions}
    pending, visited = [start], set()
    while pending:
        address = pending.pop()
        if address in visited or address not in indexed:
            continue
        visited.add(address)
        insn = indexed[address]
        if insn.group(cs.CS_GRP_RET) or insn.group(cs.CS_GRP_IRET) or insn.mnemonic in ("int3", "ud2", "hlt"):
            continue
        if insn.group(cs.CS_GRP_JUMP):
            if insn.operands and insn.operands[0].type == cs.x86.X86_OP_IMM:
                pending.append(insn.operands[0].imm)
            if insn.mnemonic in ("jmp", "ljmp"):
                continue
        pending.append(address + insn.size)
    return visited


def decode_range(code, start, cs):
    decoder = cs.Cs(cs.CS_ARCH_X86, cs.CS_MODE_64)
    decoder.detail = True
    instructions = list(decoder.disasm(code, start))
    complete = bool(instructions) and instructions[-1].address + instructions[-1].size == start + len(code)
    reachable = local_reachable(instructions, start, cs)
    references = []
    for i, insn in enumerate(instructions):
        operands = [o for o in insn.operands if o.type == cs.x86.X86_OP_MEM and o.mem.disp == 0x3E34]
        if not operands:
            continue
        row = dict(rva=insn.address, mnemonic=insn.mnemonic, operands=insn.op_str,
                   instruction_sha256=hashlib.sha256(insn.bytes).hexdigest(),
                   locally_reachable=insn.address in reachable, linear_range_complete=complete,
                   memory_operands=[dict(base=insn.reg_name(o.mem.base), index=insn.reg_name(o.mem.index),
                                         scale=o.mem.scale, displacement=o.mem.disp, size=o.size,
                                         access=o.access) for o in operands],
                   actor_provenance_verified=False,
                   context=[dict(rva=x.address, assembly=x.mnemonic + " " + x.op_str)
                            for x in instructions[max(0, i - 3):i + 4]])
        if (insn.mnemonic == "mov" and insn.operands[0].type == cs.x86.X86_OP_MEM
                and len(insn.operands) == 2 and insn.operands[1].type == cs.x86.X86_OP_IMM):
            bits = insn.operands[1].imm & 0xFFFFFFFF
            value = struct.unpack("<f", struct.pack("<I", bits))[0]
            row["immediate_low32"] = bits
            row["immediate_low32_float"] = value if math.isfinite(value) else None
        references.append(row)
    return references, complete


def inspect_native(path, cs):
    meta, data = inspect_pe(path)
    require_build_and_anchors(meta, data)
    ranges = runtime_ranges(meta, data)
    starts = [r[0] for r in ranges]
    hits, selected, unresolved = [], set(), []
    for section in meta["sections"]:
        if not section["flags"] & 0x20000000:
            continue
        code = rva_bytes(meta, data, section["rva"], min(section["raw_size"], section["virtual_size"]), executable=True)
        position = -1
        while (position := code.find(b"\x34\x3e\x00\x00", position + 1)) >= 0:
            rva = section["rva"] + position
            hits.append(rva)
            if len(hits) > 1024:
                raise ValueError("Raw candidate budget exceeded")
            index = bisect.bisect_right(starts, rva) - 1
            if index < 0 or rva >= ranges[index][1]:
                unresolved.append(rva)
            else:
                selected.add(ranges[index])
    if len(selected) > 512 or sum(end - start for start, end, _ in selected) > MAX_TOTAL:
        raise ValueError("Selected function budget exceeded")
    refs, skipped = [], []
    for start, end, unwind in sorted(selected):
        if end - start > MAX_FUNCTION:
            skipped.append(dict(start=start, end=end, reason="range_budget"))
            continue
        code = rva_bytes(meta, data, start, end - start, executable=True)
        rows, complete = decode_range(code, start, cs)
        if not complete:
            skipped.append(dict(start=start, end=end, reason="linear_decode_incomplete"))
        for row in rows:
            row.update(runtime_range=[start, end], unwind_rva=unwind,
                       runtime_range_sha256=hashlib.sha256(code).hexdigest())
        refs.extend(rows)
    try:
        distribution = importlib.metadata.version("capstone")
    except importlib.metadata.PackageNotFoundError:
        distribution = None
    return dict(protocol="dmc3-disk-native-timer", schema_version=1, disk_build=meta,
                decoder=dict(distribution_version=distribution, binding_version=cs.__version__,
                             core_api=list(cs.cs_version())),
                raw_displacement_hits=len(hits), selected_runtime_ranges=len(selected),
                unresolved_raw_rvas=unresolved, skipped_ranges=skipped, references=refs,
                mnemonic_counts=dict(Counter(r["mnemonic"] for r in refs)),
                local_reachable_references=sum(r["locally_reachable"] for r in refs),
                limitations=["Finite disk displacement scan; indirect/base-adjusted references can be missed",
                             "Pdata ranges may be fragments; leaf functions without entries are not searched",
                             "Linear decode can encounter data; local direct reachability is limited, not full CFG",
                             "Same displacement does not prove actor identity or live execution",
                             "No units, negative-value semantics or combo detector verified"],
                no_game_process_access=True, pine_repeated=False, phase2_verified=False,
                authentic_attacks_detected=False)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--exe", type=Path, required=True)
    parser.add_argument("--decoder-path", type=Path, help="Already verified isolated Capstone directory; no downloads")
    parser.add_argument("--output-root", type=Path, default=Path(r"D:\logs"))
    args = parser.parse_args(argv)
    try:
        if args.decoder_path:
            sys.path.insert(0, str(args.decoder_path.resolve()))
        import capstone
        report = inspect_native(args.exe, capstone)
        report["created_utc"] = datetime.now(timezone.utc).isoformat()
        run = args.output_root / ("dmc3-native-timer-" + datetime.now().strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex)
        run.mkdir(parents=True, exist_ok=False)
        with (run / "report.json").open("x", encoding="utf-8") as stream:
            json.dump(report, stream, ensure_ascii=False, indent=2, allow_nan=False)
        print(json.dumps(dict(output=str(run), references=len(report["references"]), phase2_verified=False)))
        return 0
    except (OSError, ImportError, ValueError, KeyError, struct.error, ObservationError) as error:
        print(json.dumps(dict(error=str(error), no_game_process_access=True, phase2_verified=False)))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
