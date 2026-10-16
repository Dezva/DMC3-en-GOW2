#!/usr/bin/env python3
"""Inspect a DMC3 PAC and copy its blocks and supported DDS textures read-only."""

import argparse
import hashlib
import json
from pathlib import Path
import struct
import sys


MAX_INPUT = 64 * 1024 * 1024
MAX_ENTRIES = 4096


class PacError(ValueError):
    """Malformed or unsupported PAC/DDS structure."""


def slots(data, base=0, end=None):
    """Offsets are relative to each PAC, not the outer file; spans include padding."""
    end = len(data) if end is None else end
    if base < 0 or end > len(data) or end - base < 8:
        raise PacError("Truncated PAC header.")
    if data[base:base + 4] not in (b"PAC\0", b"PNST"):
        raise PacError("Expected a PAC or PNST header.")
    count = struct.unpack_from("<I", data, base + 4)[0]
    if count > MAX_ENTRIES or 8 + count * 4 > end - base:
        raise PacError("Invalid PAC entry count or truncated offset table.")
    offsets = struct.unpack_from(f"<{count}I", data, base + 8)
    present = [offset for offset in offsets if offset]
    if present != sorted(set(present)):
        raise PacError("Aliased or unordered PAC offsets are unsupported.")
    if any(offset < 8 + count * 4 or offset >= end - base for offset in present):
        raise PacError("PAC entry points outside its payload.")
    boundaries = dict(zip(present, present[1:] + [end - base]))
    return [None if offset == 0 else (base + offset, base + boundaries[offset])
            for offset in offsets]


def dds_info(data, offset, end):
    if offset < 0 or offset + 128 > end or end > len(data):
        raise PacError("Truncated DDS header.")
    if data[offset:offset + 4] != b"DDS ":
        raise PacError("Expected DDS signature.")
    size, flags, height, width, pitch, depth, mip_count = struct.unpack_from("<7I", data, offset + 4)
    pf_size, pf_flags = struct.unpack_from("<II", data, offset + 76)
    fourcc = data[offset + 84:offset + 88]
    caps2 = struct.unpack_from("<I", data, offset + 112)[0]
    if size != 124 or pf_size != 32 or not pf_flags & 4:
        raise PacError("Unsupported DDS header or pixel format.")
    if not 1 <= width <= 4096 or not 1 <= height <= 4096:
        raise PacError("Unsupported DDS dimensions.")
    if depth > 1 or caps2 & (0x200 | 0x200000):
        raise PacError("Cubemap and volume DDS files are unsupported.")
    if fourcc not in (b"DXT1", b"DXT3", b"DXT5"):
        raise PacError("Only DXT1, DXT3 and DXT5 DDS textures are supported.")
    levels = mip_count or 1
    if levels > max(width, height).bit_length():
        raise PacError("Invalid DDS mip count.")
    block_size = 8 if fourcc == b"DXT1" else 16
    payload_size = sum(max(1, (max(1, width >> level) + 3) // 4)
                       * max(1, (max(1, height >> level) + 3) // 4) * block_size
                       for level in range(levels))
    byte_size = 128 + payload_size
    if offset + byte_size > end:
        raise PacError("DDS mip data exceeds its PAC block.")
    return {"offset": offset, "width": width, "height": height,
            "format": fourcc.decode("ascii"), "mip_levels": levels,
            "byte_size": byte_size, "declared_pitch_or_linear_size": pitch}


def analyze(data):
    if len(data) > MAX_INPUT:
        raise PacError("PAC exceeds the 64 MiB inspection limit.")
    root_slots = slots(data)
    blocks = []
    textures = []
    files = {}
    for index, span in enumerate(root_slots):
        if span is None:
            blocks.append({"index": index, "absent": True})
            continue
        start, end = span
        signature = data[start:start + 4]
        extension = {b"MOD ": "mod", b"SHW ": "shw", b"PAC\0": "pac",
                     b"PNST": "pac"}.get(signature, "bin")
        filename = f"slot_{index:03d}.{extension}"
        payload = data[start:end]
        files[filename] = payload
        block = {"index": index, "offset": start, "span_bytes": end - start,
                 "signature_hex": signature.hex(), "file": filename,
                 "sha256": hashlib.sha256(payload).hexdigest()}
        if signature in (b"PAC\0", b"PNST"):
            inner = slots(data, start, end)
            block["nested_slot_count"] = len(inner)
            block["nested_present_count"] = sum(span is not None for span in inner)
        blocks.append(block)
        cursor = start
        while True:
            offset = data.find(b"DDS ", cursor, end)
            if offset == -1:
                break
            # A magic string alone does not identify a DDS embedded in arbitrary data.
            if offset + 128 > end or data[offset + 4:offset + 8] != b"\x7c\0\0\0":
                cursor = offset + 4
                continue
            info = dds_info(data, offset, end)
            info["slot_index"] = index
            filename = f"texture_{len(textures):03d}.dds"
            texture = data[offset:offset + info["byte_size"]]
            info.update(file=filename, sha256=hashlib.sha256(texture).hexdigest())
            files[filename] = texture
            textures.append(info)
            cursor = offset + info["byte_size"]
    return {"source_bytes": len(data), "source_sha256": hashlib.sha256(data).hexdigest(),
            "slot_count": len(root_slots), "blocks": blocks, "textures": textures,
            "limitations": "Block spans may include alignment padding. MOD geometry, "
                           "bones and skin weights are not decoded. This is not a game patch."}, files


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pac", type=Path)
    parser.add_argument("--manifest", type=Path, help="Optional Export-DanteSample informe.json")
    parser.add_argument("--output", type=Path, help="New output directory; existing directories are rejected")
    args = parser.parse_args(argv)
    try:
        with args.pac.open("rb") as stream:
            data = stream.read(MAX_INPUT + 1)
        if len(data) > MAX_INPUT:
            raise PacError("PAC exceeds the 64 MiB inspection limit.")
        if args.manifest:
            manifest = json.loads(args.manifest.read_text(encoding="utf-8-sig"))
            if not isinstance(manifest, dict):
                raise PacError("Manifest must be a JSON object.")
            if (manifest.get("Bytes") != len(data)
                    or str(manifest.get("SHA256", "")).lower() != hashlib.sha256(data).hexdigest()):
                raise PacError("PAC does not match manifest length/SHA256.")
        report, files = analyze(data)
        if args.output:
            args.output.mkdir(parents=True, exist_ok=False)
            for filename, payload in files.items():
                with (args.output / filename).open("xb") as stream:
                    stream.write(payload)
            with (args.output / "pac-report.json").open("x", encoding="utf-8") as stream:
                json.dump(report, stream, ensure_ascii=False, indent=2)
                stream.write("\n")
    except (OSError, ValueError, struct.error) as error:
        parser.exit(1, f"Error: {error}\n")
    json.dump(report, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
