#!/usr/bin/env python3
"""Read a God of War II TOC; resolve available PAK extents from an ISO-root CSV."""

import argparse
import csv
import hashlib
import json
from pathlib import Path
import struct
import sys


SECTOR_SIZE = 2048
PACK_SPLIT = 10_000_000
MAX_TOC = 16 * 1024 * 1024
SAMPLES = ("R_HERO00.WAD", "R_HERO01.WAD", "R_PERMA.WAD")


class TocError(ValueError):
    pass


def parse_toc(data):
    if len(data) < 4 or len(data) > MAX_TOC:
        raise TocError("Invalid TOC length.")
    count = struct.unpack_from("<I", data)[0]
    table_end = 4 + count * 36
    if not 0 < count <= 100_000 or table_end > len(data) or (len(data) - table_end) % 4:
        raise TocError("Invalid file count or truncated TOC tables.")
    offsets = struct.unpack_from(f"<{(len(data) - table_end) // 4}I", data, table_end)
    entries = []
    seen = set()
    used_slots = set()
    for index in range(count):
        raw_name, size, encounters, start = struct.unpack_from("<24sIII", data, 4 + index * 36)
        try:
            name = raw_name.split(b"\0", 1)[0].decode("ascii")
        except UnicodeError as error:
            raise TocError("Non-ASCII TOC filename.") from error
        if (not name or name.upper() in seen or any(ord(c) < 32 for c in name)
                or "/" in name or "\\" in name or name in (".", "..")):
            raise TocError("Unsafe or duplicate TOC filename.")
        if size == 0 or encounters == 0 or start + encounters > len(offsets):
            raise TocError("Invalid file length or encounter range.")
        seen.add(name.upper())
        used_slots.update(range(start, start + encounters))
        entries.append({"name": name, "bytes": size, "raw_sectors": list(offsets[start:start + encounters])})
    # Same split used by god_of_war_browser's GOW2 driver. Missing PAKs remain unresolved.
    indexed = any(sector >= PACK_SPLIT for entry in entries for sector in entry["raw_sectors"])
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(),
            "file_count": count, "encounter_count": sum(len(e["raw_sectors"]) for e in entries),
            "offset_table_slots": len(offsets), "unused_offset_slots": len(offsets) - len(used_slots),
            "addressing": "indexed" if indexed else "absolute", "entries": entries}


def root_paks(rows):
    paks = {}
    for row in rows:
        name = row.get("Name", "").upper()
        if not (name.startswith("PART") and name.endswith(".PAK") and name[4:-4].isdigit()):
            continue
        index = int(name[4:-4])
        sector, size = int(row["Sector"]), int(row["Bytes"])
        if index < 1 or index in paks or sector < 0 or size <= 0 or row.get("Directory", "").lower() != "false":
            raise TocError("Invalid PAK metadata in root CSV.")
        paks[index] = {"sector": sector, "bytes": size}
    return paks


def resolve(report, paks):
    for entry in report["entries"]:
        locations = []
        for raw in entry["raw_sectors"]:
            if report["addressing"] == "indexed":
                pak_id, relative = raw // PACK_SPLIT + 1, (raw % PACK_SPLIT) * SECTOR_SIZE
            else:
                pak_id, relative = 1, raw * SECTOR_SIZE
                while pak_id in paks and relative >= paks[pak_id]["bytes"]:
                    relative -= paks[pak_id]["bytes"]
                    pak_id += 1
            pak = paks.get(pak_id)
            available = pak is not None and relative + entry["bytes"] <= pak["bytes"]
            locations.append({"raw_sector": raw, "pak": f"PART{pak_id}.PAK", "pak_offset": relative,
                              "iso_offset": pak["sector"] * SECTOR_SIZE + relative if available else None})
        entry["locations"] = locations
    report["sample_candidates"] = [entry for entry in report["entries"] if entry["name"] in SAMPLES]
    report["scope"] = "File names do not prove asset contents. Missing/hidden-layer PAK extents are not guessed."
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("toc", type=Path)
    parser.add_argument("--root-csv", type=Path)
    parser.add_argument("--manifest", type=Path)
    args = parser.parse_args(argv)
    try:
        with args.toc.open("rb") as stream:
            data = stream.read(MAX_TOC + 1)
        report = parse_toc(data)
        if args.manifest:
            manifest = json.loads(args.manifest.read_text(encoding="utf-8-sig"))
            if (not isinstance(manifest, dict) or manifest.get("IndexBytes") != len(data)
                    or str(manifest.get("IndexSHA256", "")).lower() != report["sha256"]):
                raise TocError("TOC does not match the supplied report.")
        paks = {}
        if args.root_csv:
            with args.root_csv.open(encoding="utf-8-sig", newline="") as stream:
                paks = root_paks(csv.DictReader(stream))
        resolve(report, paks)
    except (OSError, ValueError, struct.error, KeyError) as error:
        parser.exit(1, f"Error: {error}\n")
    json.dump(report, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
