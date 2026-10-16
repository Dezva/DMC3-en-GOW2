#!/usr/bin/env python3
"""Read PS2 disc identity from an uncompressed ISO without modifying it."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import struct
import sys


SECTOR = 2048
MAX_METADATA = 8 * 1024 * 1024


class DiscError(ValueError):
    """Unsupported or malformed disc input."""


class Disc:
    def __init__(self, stream):
        self.stream = stream
        stream.seek(0, 2)
        self.size = stream.tell()
        self.volume_sectors = None
        for sector in range(16, min(self.size // SECTOR, 256)):
            descriptor = self.read(sector * SECTOR, SECTOR)
            if descriptor[1:6] != b"CD001" or descriptor[6] != 1:
                raise DiscError("No es una ISO ISO9660 de sectores de 2048 bytes.")
            if descriptor[0] == 255:
                break
            if descriptor[0] == 1:
                if self.both16(descriptor, 128) != SECTOR:
                    raise DiscError("El tamaño de sector de esta ISO no es compatible.")
                self.volume_sectors = self.both32(descriptor, 80)
                if self.volume_sectors * SECTOR > self.size:
                    raise DiscError("La imagen está truncada respecto al volumen declarado.")
                self.volume = descriptor[40:72].decode("ascii", "replace").strip()
                self.root = self.record(descriptor[156:190])
                if not self.root[2] & 2:
                    raise DiscError("El registro raíz no es un directorio.")
                return
        raise DiscError("No se encontró un descriptor primario ISO9660.")

    @staticmethod
    def both16(data, offset):
        little = struct.unpack_from("<H", data, offset)[0]
        big = struct.unpack_from(">H", data, offset + 2)[0]
        if little != big:
            raise DiscError("Campo ISO9660 de 16 bits inconsistente.")
        return little

    @staticmethod
    def both32(data, offset):
        little = struct.unpack_from("<I", data, offset)[0]
        big = struct.unpack_from(">I", data, offset + 4)[0]
        if little != big:
            raise DiscError("Campo ISO9660 de 32 bits inconsistente.")
        return little

    def read(self, offset, length):
        if offset < 0 or length < 0 or offset + length > self.size:
            raise DiscError("La imagen está truncada o contiene una extensión inválida.")
        self.stream.seek(offset)
        data = self.stream.read(length)
        if len(data) != length:
            raise DiscError("No se pudo leer la extensión completa.")
        return data

    def record(self, data):
        if len(data) < 34 or data[0] != len(data) or 33 + data[32] > len(data):
            raise DiscError("Registro de directorio ISO9660 inválido.")
        if data[1] or data[26] or data[27] or data[25] & 128:
            raise DiscError("No se admiten archivos extendidos, intercalados o multiextensión.")
        extent = self.both32(data, 2)
        length = self.both32(data, 10)
        if extent * SECTOR + length > self.volume_sectors * SECTOR:
            raise DiscError("Una extensión excede el volumen declarado.")
        return extent * SECTOR, length, data[25], data[33:33 + data[32]]

    def entries(self, directory):
        offset, length, flags, _ = directory
        if not flags & 2:
            raise DiscError("La ruta esperada no es un directorio.")
        if length > MAX_METADATA:
            raise DiscError("El directorio supera el límite de lectura de metadatos.")
        data = self.read(offset, length)
        position = 0
        while position < len(data):
            size = data[position]
            if size == 0:
                position = (position // SECTOR + 1) * SECTOR
                continue
            if position % SECTOR + size > SECTOR or position + size > len(data):
                raise DiscError("Un registro cruza el límite del directorio o sector.")
            entry = self.record(data[position:position + size])
            if entry[3] not in (b"\0", b"\1"):
                yield entry
            position += size

    def find(self, path):
        current = self.root
        for part in path.replace("\\", "/").split("/"):
            if not part or part in (".", ".."):
                raise DiscError("Ruta de disco no admitida.")
            matches = [e for e in self.entries(current)
                       if e[3].decode("ascii", "replace").split(";")[0].upper()
                       == part.split(";")[0].upper()]
            if len(matches) != 1:
                raise DiscError(f"Archivo ausente o ambiguo en la ISO: {part}")
            current = matches[0]
        return current

    def report(self):
        cnf = self.find("SYSTEM.CNF")
        if cnf[2] & 2 or cnf[1] > MAX_METADATA:
            raise DiscError("SYSTEM.CNF no es un archivo de configuración válido.")
        text = self.read(cnf[0], cnf[1]).decode("ascii", "replace")
        match = re.search(r"^\s*BOOT2\s*=\s*cdrom0?:[\\/]*(\S+)\s*$", text,
                          re.IGNORECASE | re.MULTILINE)
        if not match:
            raise DiscError("SYSTEM.CNF no contiene una ruta BOOT2 de PS2 compatible.")
        boot = match[1]
        elf = self.find(boot)
        if elf[2] & 2 or elf[1] < 52:
            raise DiscError("El ejecutable BOOT2 no es un ELF32 válido.")
        header = self.read(elf[0], 52)
        if header[:7] != b"\x7fELF\x01\x01\x01":
            raise DiscError("Se esperaba un ELF de 32 bits little-endian.")
        kind, machine, version, entry = struct.unpack_from("<HHII", header, 16)
        if machine != 8 or kind != 2 or version != 1:
            raise DiscError("El archivo BOOT2 no es un ejecutable ELF MIPS compatible.")
        digest = hashlib.sha256()
        for position in range(0, elf[1], 1024 * 1024):
            digest.update(self.read(elf[0] + position, min(1024 * 1024, elf[1] - position)))
        filename = boot.replace("\\", "/").rsplit("/", 1)[-1].split(";")[0]
        serial = re.fullmatch(r"([A-Z]{4})_(\d{3})\.(\d{2})", filename.upper())
        return {
            "volume_label": self.volume,
            "disc_serial": f"{serial[1]}-{serial[2]}{serial[3]}" if serial else None,
            "boot_path": boot,
            "elf_size_bytes": elf[1],
            "elf_entry_address": f"0x{entry:08X}",
            "elf_sha256": digest.hexdigest(),
            "note": "SHA-256 identifica este ejecutable; no es el CRC de PCSX2. "
                    "La identidad del juego debe confirmarse por separado.",
        }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("iso", type=Path, help="ISO PS2 sin comprimir; lectura solamente")
    args = parser.parse_args(argv)
    if args.iso.suffix.lower() in (".chd", ".cso", ".gz", ".zip"):
        parser.exit(2, "Error: utiliza una ISO sin comprimir, no CHD/CSO/ZIP/GZ.\n")
    try:
        with args.iso.open("rb") as stream:
            result = Disc(stream).report()
    except (OSError, DiscError) as error:
        parser.exit(1, f"Error: {error}\n")
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
