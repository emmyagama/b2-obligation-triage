#!/usr/bin/env python3
"""Pack, verify and unpack the LLM response cache as a versioned ZIP artifact."""
import argparse
import hashlib
import os
import shutil
import sys
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CACHE = ROOT / "cache/llm"
DEFAULT_ARCHIVE = ROOT / "dist/b2-llm-cache-v1.zip"
PREFIX = PurePosixPath("cache/llm")


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def cache_files(cache_dir):
    cache_dir = Path(cache_dir)
    if not cache_dir.is_dir():
        raise ValueError(f"cache directory not found: {cache_dir}")
    files = sorted(path for path in cache_dir.rglob("*.json") if path.is_file())
    if not files:
        raise ValueError(f"cache directory has no JSON response files: {cache_dir}")
    return files


def pack(cache_dir, archive):
    cache_dir = Path(cache_dir)
    archive = Path(archive)
    archive.parent.mkdir(parents=True, exist_ok=True)
    files = cache_files(cache_dir)
    tmp = archive.with_name(archive.name + ".tmp")
    with zipfile.ZipFile(tmp, "w") as bundle:
        for path in files:
            name = (PREFIX / path.relative_to(cache_dir).as_posix()).as_posix()
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            bundle.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    os.replace(tmp, archive)
    digest = sha256(archive)
    checksum = archive.with_name(archive.name + ".sha256")
    checksum.write_text(f"{digest}  {archive.name}\n", encoding="ascii")
    print(f"packed {len(files)} files -> {archive} ({archive.stat().st_size} bytes)")
    print(f"sha256 {digest}")
    return archive, checksum


def read_checksum(checksum, archive):
    checksum = Path(checksum)
    if not checksum.is_file():
        raise ValueError(f"checksum file not found: {checksum}")
    parts = checksum.read_text(encoding="ascii").split()
    if not parts or len(parts[0]) != 64 or any(c not in "0123456789abcdefABCDEF" for c in parts[0]):
        raise ValueError(f"invalid SHA-256 checksum file: {checksum}")
    if len(parts) > 1 and Path(parts[1]).name != Path(archive).name:
        raise ValueError(f"checksum names {parts[1]}, not {Path(archive).name}")
    return parts[0].lower()


def verify(archive, checksum):
    archive = Path(archive)
    if not archive.is_file():
        raise ValueError(f"archive not found: {archive}")
    expected = read_checksum(checksum, archive)
    actual = sha256(archive)
    if actual != expected:
        raise ValueError(f"SHA-256 mismatch: expected {expected}, got {actual}")
    try:
        with zipfile.ZipFile(archive) as bundle:
            infos = bundle.infolist()
            if not infos:
                raise ValueError("archive is empty")
            names = set()
            for info in infos:
                name = PurePosixPath(info.filename)
                if name.is_absolute() or ".." in name.parts or not name.as_posix().startswith(PREFIX.as_posix() + "/"):
                    raise ValueError(f"unsafe or unexpected archive path: {info.filename}")
                if name.suffix != ".json":
                    raise ValueError(f"unexpected non-JSON archive entry: {info.filename}")
                if info.filename in names:
                    raise ValueError(f"duplicate archive entry: {info.filename}")
                names.add(info.filename)
            total = sum(info.file_size for info in infos)
    except zipfile.BadZipFile as exc:
        raise ValueError(f"invalid ZIP archive: {archive}") from exc
    print(f"verified {len(names)} files, {total} uncompressed bytes")
    print(f"sha256 {actual}")
    return len(names), total, actual


def unpack(archive, checksum, dest):
    verify(archive, checksum)
    dest = Path(dest).resolve()
    with zipfile.ZipFile(archive) as bundle:
        for info in bundle.infolist():
            target = (dest / info.filename).resolve()
            if dest not in target.parents:
                raise ValueError(f"refusing to extract outside destination: {info.filename}")
            target.parent.mkdir(parents=True, exist_ok=True)
            with bundle.open(info) as source, target.open("wb") as output:
                shutil.copyfileobj(source, output)
    print(f"unpacked into {dest}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)

    pack_parser = commands.add_parser("pack", help="create a deterministic ZIP and checksum")
    pack_parser.add_argument("--cache-dir", type=Path, default=DEFAULT_CACHE)
    pack_parser.add_argument("--out", type=Path, default=DEFAULT_ARCHIVE)

    verify_parser = commands.add_parser("verify", help="verify the archive checksum and paths")
    verify_parser.add_argument("--archive", type=Path, required=True)
    verify_parser.add_argument("--checksum", type=Path, required=True)

    unpack_parser = commands.add_parser("unpack", help="verify and extract into a repository root")
    unpack_parser.add_argument("--archive", type=Path, required=True)
    unpack_parser.add_argument("--checksum", type=Path, required=True)
    unpack_parser.add_argument("--dest", type=Path, default=ROOT)

    args = parser.parse_args()
    try:
        if args.command == "pack":
            pack(args.cache_dir, args.out)
        elif args.command == "verify":
            verify(args.archive, args.checksum)
        else:
            unpack(args.archive, args.checksum, args.dest)
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
