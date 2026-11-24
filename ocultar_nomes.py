#!/usr/bin/env python3
import glob
import json
import subprocess
import time
from pathlib import Path

BACKUP_DIR = Path.home() / ".local/share/ding-hide-labels"
BACKUP_FILE = BACKUP_DIR / "backup.json"
OWN_LAUNCHER_NAME = "ocultar-nomes.desktop"


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


def is_hidden(value: str) -> bool:
    clean = value.strip("\r\n ")
    return len(clean) > 0 and all(c in ("\u200b", "\u2800") for c in clean)


def extract_entry_name_lines(lines: list[str]) -> list[str]:
    in_entry = False
    found = []
    for line in lines:
        s = line.strip()
        if s.startswith("["):
            in_entry = (s == "[Desktop Entry]")
        elif in_entry and (line.startswith("Name=") or line.startswith("Name[")):
            found.append(line)
    return found


def load_backup() -> dict[str, list[str]]:
    if BACKUP_FILE.exists():
        try:
            return json.loads(BACKUP_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def save_backup(data: dict[str, list[str]]) -> None:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    BACKUP_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def reload_ding() -> None:
    subprocess.run(["gnome-extensions", "disable", "ding@rastersoft.com"], check=False)
    time.sleep(0.3)
    subprocess.run(["gnome-extensions", "enable", "ding@rastersoft.com"], check=False)


def main() -> None:
    desktop_dir = get_desktop_dir()
    files = sorted(glob.glob(str(desktop_dir / "*.desktop")))
    target_files = [Path(f) for f in files if Path(f).name != OWN_LAUNCHER_NAME]

    backup = load_backup()

    for idx, path in enumerate(target_files, start=2):
        lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
        name_lines = extract_entry_name_lines(lines)

        has_real_name = any(
            not is_hidden(l.split("=", 1)[1]) for l in name_lines if "=" in l
        )
        if has_real_name:
            backup[path.name] = name_lines

        hidden_name = "\u200b" * idx
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
                    new_lines.append(f"Name={hidden_name}\n")
                    replaced = True
            else:
                new_lines.append(line)

        if replaced:
            path.write_text("".join(new_lines), encoding="utf-8")

    save_backup(backup)
    reload_ding()


if __name__ == "__main__":
    main()
