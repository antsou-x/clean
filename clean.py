"""Audit et nettoyage ciblés du cache local de roues pip."""
import argparse
import ctypes
import json
import os
from pathlib import Path
import re
import stat
import sys
import time
from dataclasses import dataclass

AGE = 30 * 86400
WHEEL = re.compile(r"[A-Za-z0-9_][A-Za-z0-9_.+!-]*(?:-[A-Za-z0-9_.+!]+){4}\.whl", re.ASCII)


class Refusal(Exception):
    pass


def cache_root():
    if sys.platform == "win32":
        buffer = ctypes.create_unicode_buffer(260)
        if ctypes.windll.shell32.SHGetFolderPathW(None, 0x28, None, 0, buffer):
            raise Refusal("Profil Windows indisponible.")
        home = Path(buffer.value)
        relative = "AppData/Local/pip/Cache/wheels"
    elif sys.platform == "darwin":
        import pwd
        home = Path(pwd.getpwuid(os.getuid()).pw_dir)
        relative = "Library/Caches/pip/wheels"
    else:
        raise Refusal("Windows ou macOS requis.")
    if not home.is_absolute() or ".." in home.parts or str(home).startswith(("\\\\", "//")):
        raise Refusal("Profil local requis.")
    return home / relative


def elevated():
    if sys.platform == "win32":
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    return os.geteuid() == 0


def linked(info):
    return stat.S_ISLNK(info.st_mode) or bool(getattr(info, "st_file_attributes", 0)
                                              & stat.FILE_ATTRIBUTE_REPARSE_POINT)


def check_dir(path):
    for directory in (*reversed(path.parents), path):
        info = directory.lstat()
        if linked(info) or not stat.S_ISDIR(info.st_mode):
            raise Refusal("Dossier redirigé ou incompatible.")
        if directory != Path(directory.anchor) and os.path.ismount(directory):
            raise Refusal("Point de montage intermédiaire.")
        try:
            (directory / ".git").lstat()
        except FileNotFoundError:
            continue
        raise Refusal("Dépôt Git protégé.")


@dataclass(frozen=True)
class Entry:
    path: Path
    signature: tuple


def identify(path, cutoff):
    info = path.lstat()
    if (linked(info) or not stat.S_ISREG(info.st_mode) or info.st_nlink != 1
            or not info.st_ino or info.st_mtime_ns > cutoff):
        return None
    return Entry(path, (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns, info.st_ctime_ns))


def scan(root, cutoff):
    entries = []
    issues = 0
    try:
        check_dir(root)
    except FileNotFoundError:
        return entries, issues

    def visit(directory, depth):
        nonlocal issues
        check_dir(directory)
        for path in directory.iterdir():
            try:
                if depth < 4:
                    width = 2 if depth < 3 else 50
                    if re.fullmatch("[a-f0-9]{%d}" % width, path.name):
                        visit(path, depth + 1)
                elif WHEEL.fullmatch(path.name):
                    entry = identify(path, cutoff)
                    if entry:
                        entries.append(entry)
            except (OSError, Refusal):
                issues += 1

    visit(root, 0)
    return sorted(entries, key=lambda entry: entry.path), issues


def run(root, clean, share, detail):
    cutoff = time.time_ns() - AGE * 10**9
    entries, issues = scan(root, cutoff)
    size = sum(entry.signature[2] for entry in entries)
    if share:
        print(json.dumps(dict(candidats=len(entries), octets=size, anomalies=issues)))
        return int(bool(issues))
    print(f"{len(entries)} archive(s) de plus de 30 jours, {size} octets logiques. Anomalies : {issues}.")
    if detail or clean:
        for entry in entries:
            print(entry.path.relative_to(root).as_posix(), entry.signature[2], "octets")
    if not clean or not entries or issues:
        return int(bool(issues))
    if elevated() or not sys.stdin.isatty():
        raise Refusal("Terminal interactif sans élévation requis.")
    print("Suppression définitive de cette liste. Fermez les opérations pip en cours.")
    if input("Tapez OUI pour confirmer : ") != "OUI":
        print("Annulé.")
        return 0
    removed = 0
    for entry in entries:
        try:
            check_dir(entry.path.parent)
            if identify(entry.path, cutoff) != entry:
                raise Refusal("Entrée modifiée.")
            entry.path.unlink()
            removed += 1
        except (OSError, Refusal):
            issues += 1
    print(f"Archives retirées : {removed}. Omises ou en erreur : {issues}.")
    return int(bool(issues))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--clean", action="store_true", help="prévisualiser puis confirmer la suppression")
    mode.add_argument("--share", action="store_true", help="afficher uniquement les compteurs JSON")
    mode.add_argument("--detail", action="store_true", help="afficher les noms locaux")
    args = parser.parse_args(argv)
    try:
        return run(cache_root(), args.clean, args.share, args.detail)
    except (OSError, EOFError, KeyboardInterrupt, Refusal) as error:
        print(f"Arrêt : {error if isinstance(error, Refusal) else type(error).__name__}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

