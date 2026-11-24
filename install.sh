#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN_DIR="$HOME/.local/bin"
HIDE_SCRIPT="$BIN_DIR/ocultar-nomes.py"
RESTORE_SCRIPT="$BIN_DIR/restaurar-nomes.py"

DESKTOP_DIR="$(xdg-user-dir DESKTOP 2>/dev/null || echo "$HOME/Desktop")"
if [ ! -d "$DESKTOP_DIR" ] && [ -d "$HOME/Área de Trabalho" ]; then
  DESKTOP_DIR="$HOME/Área de Trabalho"
fi

mkdir -p "$BIN_DIR" "$DESKTOP_DIR"
cp "$SCRIPT_DIR/ocultar_nomes.py" "$HIDE_SCRIPT"
cp "$SCRIPT_DIR/restaurar_nomes.py" "$RESTORE_SCRIPT"
chmod 755 "$HIDE_SCRIPT" "$RESTORE_SCRIPT"

LAUNCHER_PATH="$DESKTOP_DIR/ocultar-nomes.desktop"
python3 -c '
import sys
launcher_path, exec_path = sys.argv[1], sys.argv[2]
content = f"""[Desktop Entry]
Type=Application
Name=\u200b
Exec={exec_path}
Icon=view-refresh
Terminal=false
"""
with open(launcher_path, "w", encoding="utf-8") as f:
    f.write(content)
' "$LAUNCHER_PATH" "$HIDE_SCRIPT"

chmod 755 "$LAUNCHER_PATH"
gio set "$LAUNCHER_PATH" metadata::trusted true 2>/dev/null || true

"$HIDE_SCRIPT"
echo "Instalação concluída. Atalho criado em: $LAUNCHER_PATH"
