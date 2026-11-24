#!/usr/bin/env python3
import glob
import json
import subprocess
import time
from pathlib import Path

BACKUP_FILE = Path.home() / ".local/share/ding-hide-labels/backup.json"
OWN_LAUNCHER_NAME = "ocultar-nomes.desktop"

SYSTEM_APP_DIRS = [
    Path("/usr/share/applications"),
    Path("/usr/local/share/applications"),
    Path("/var/lib/flatpak/exports/share/applications"),
    Path.home() / ".local/share/applications",
    Path.home() / ".local/share/flatpak/exports/share/applications",
]


def get_desktop_dir() -> Path:
    try:
        out = subprocess.check_output(["xdg-user-dir", "DESKTOP"], text=True).strip()
        if out and Path(out).exists():
            return Path(out)
    except Exception:
        pass
    for candidate in (Path.home() / "Desktop", Path.home() / "Área de Trabalho"):
        if candidate.exists():
            return candidate
    return Path.home() / "Desktop"


def extract_entry_name_lines(lines: list[str]) -> list[str]:
    in_entry = False
    found = []
    for line in lines:
        s = line.strip()
        if s.startswith("["):
            in_entry = (s == "[Desktop Entry]")
        elif in_entry and (line.startswith("Name=") or line.startswith("Name[")):
            found.append(line if line.endswith("\n") else line + "\n")
    return found


def find_system_name_lines(filename: str) -> list[str]:
    for app_dir in SYSTEM_APP_DIRS:
        candidate = app_dir / filename
        if candidate.is_file():
            try:
                lines = candidate.read_text(encoding="utf-8").splitlines(keepends=True)
                found = extract_entry_name_lines(lines)
                if found:
                    return found
            except Exception:
                continue
    return []


def load_backup() -> dict[str, list[str]]:
    if BACKUP_FILE.exists():
        try:
            return json.loads(BACKUP_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def reload_ding() -> None:
    subprocess.run(["gnome-extensions", "disable", "ding@rastersoft.com"], check=False)
    time.sleep(0.3)
    subprocess.run(["gnome-extensions", "enable", "ding@rastersoft.com"], check=False)


def main() -> None:
    desktop_dir = get_desktop_dir()
    files = sorted(glob.glob(str(desktop_dir / "*.desktop")))
    backup = load_backup()

    restored_count = 0
    for f in files:
        path = Path(f)
        if path.name == OWN_LAUNCHER_NAME:
            continue

        original_lines = backup.get(path.name)
        source = "backup"
        if not original_lines:
            original_lines = find_system_name_lines(path.name)
            source = "sistema"

        if not original_lines:
            print(f"[ignorado] {path.name} (sem backup nem original no sistema)")
            continue

        lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
        in_entry = False
        replaced = False
        new_lines = []

        for line in lines:
            s = line.strip()
            if s.startswith("["):
                in_entry = (s == "[Desktop Entry]")
                new_lines.append(line)
            elif in_entry and (line.startswith("Name=") or line.startswith("Name[")):
                if not replaced:
                    new_lines.extend(
                        l if l.endswith("\n") else l + "\n" for l in original_lines
                    )
                    replaced = True
            else:
                new_lines.append(line)

        if replaced:
            path.write_text("".join(new_lines), encoding="utf-8")
            restored_count += 1
            print(f"[restaurado via {source}] {path.name}")

    reload_ding()
    print(f"Concluído: {restored_count} app(s) restaurada(s).")


if __name__ == "__main__":
    main()
