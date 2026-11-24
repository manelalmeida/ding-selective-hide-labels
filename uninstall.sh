#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN_DIR="$HOME/.local/bin"
HIDE_SCRIPT="$BIN_DIR/ocultar-nomes.py"
RESTORE_SCRIPT="$BIN_DIR/restaurar-nomes.py"
BACKUP_DIR="$HOME/.local/share/ding-hide-labels"

DESKTOP_DIR="$(xdg-user-dir DESKTOP 2>/dev/null || echo "$HOME/Desktop")"
if [ ! -d "$DESKTOP_DIR" ] && [ -d "$HOME/Área de Trabalho" ]; then
  DESKTOP_DIR="$HOME/Área de Trabalho"
fi

read -r -p "Queres restaurar os nomes originais das apps antes de desinstalar? [S/n] " resp
if [[ ! "$resp" =~ ^[nN]$ ]]; then
  if [ -x "$RESTORE_SCRIPT" ]; then
    "$RESTORE_SCRIPT"
  elif [ -f "$SCRIPT_DIR/restaurar_nomes.py" ]; then
    python3 "$SCRIPT_DIR/restaurar_nomes.py"
  fi
fi

rm -f "$HIDE_SCRIPT" "$RESTORE_SCRIPT" "$DESKTOP_DIR/ocultar-nomes.desktop"
rm -rf "$BACKUP_DIR"

gnome-extensions disable ding@rastersoft.com 2>/dev/null || true
sleep 0.3
gnome-extensions enable ding@rastersoft.com 2>/dev/null || true

echo "Desinstalação concluída."
