# DING Selective Hide App Labels

[Português (Portugal)](README.pt-PT.md) | **English**

A lightweight utility and desktop launcher for the **Desktop Icons NG (DING)** GNOME Shell extension that selectively hides the text labels of application shortcuts (`.desktop` files) on your desktop while preserving the visible names of regular folders and files.

---

## How It Works

The DING extension only provides a global toggle to show or hide icon labels across the entire desktop. To achieve selective label hiding without modifying the extension's source code:

1. **Selective Targeting (`*.desktop` only):** When executed, `ocultar_nomes.py` scans the user's desktop directory (`xdg-user-dir DESKTOP`, typically `~/Desktop`) and filters exclusively for `.desktop` launcher files. Regular folders and documents are completely ignored.
2. **Zero-Width Space Substitution (`\u200b`):** Inside the `[Desktop Entry]` section of each `.desktop` file, the script replaces `Name=` (and localized `Name[...]=` entries) with an increasing sequence of Unicode *Zero-Width Space* (`\u200b`) characters (`2x`, `3x`, `4x`, etc.).
   * Unlike standard spaces, `\u200b` is not stripped by DING.
   * Because it has zero visual width, long sequences never trigger text wrapping or ellipsis (`...`) truncation.
   * Giving each file a unique character count prevents DING from detecting duplicate item names.
3. **Automatic Backup:** Before modifying any shortcut that still has a visible name, the original `Name=` and `Name[...]=` lines are saved to `~/.local/share/ding-hide-labels/backup.json`.
4. **Live Extension Reload:** After updating the files, the script toggles `ding@rastersoft.com` via `gnome-extensions` so the desktop refreshes immediately.
5. **Smart Restoration (`restaurar_nomes.py`):** Restores original labels from `backup.json`. If a shortcut was already hidden before the first backup, it automatically searches standard system and Flatpak application directories (`/usr/share/applications`, `/var/lib/flatpak/exports/share/applications`, `~/.local/share/...`) to recover the original name.

---

## Requirements

* Linux desktop running **GNOME Shell** with the **Desktop Icons NG (DING)** extension (`ding@rastersoft.com`) enabled.
* **Python 3** (pre-installed on Fedora, Ubuntu, and most modern distributions).
* `gio` and `gnome-extensions` CLI tools (included with GNOME).

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/manelalmeida/ding-selective-hide-labels.git](https://github.com/manelalmeida/ding-selective-hide-labels.git)
   cd ding-selective-hide-labels
Run the installer:

Bash
chmod +x install.sh
./install.sh
What install.sh does:
Copies ocultar_nomes.py and restaurar_nomes.py to ~/.local/bin/.

Creates a label-free refresh launcher (ocultar-nomes.desktop) on your desktop with 0755 permissions and marks it as trusted via gio set ... metadata::trusted true.

Runs ocultar_nomes.py immediately to hide existing application labels.

Usage
Hide labels on new shortcuts: Whenever you add a new application shortcut to your desktop, click the refresh icon (view-refresh) on your desktop to hide its label and reload DING.

Restore original application names (without uninstalling): Right-click the refresh icon on your desktop and select Restaurar Nomes das Apps, or run:

Bash
~/.local/bin/restaurar-nomes.py
Uninstallation
To remove the scripts, desktop launcher, and local backup:

Bash
cd ding-selective-hide-labels
chmod +x uninstall.sh
./uninstall.sh
The uninstaller will ask if you want to restore the original application labels before removing the files.

Known Limitations
System Trash Icon: The native Trash icon provided by DING is rendered internally rather than from a .desktop file in ~/Desktop, so its label cannot be hidden by this script. As a workaround, you can disable the native Trash icon in DING settings and create a custom .desktop shortcut pointing to Exec=gio open trash:///.
