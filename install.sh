#!/usr/bin/env bash
# Install agent skills into Claude Code and/or OpenCode.
# Usage: ./install.sh [all|claude|opencode]

set -euo pipefail

TARGET="${1:-all}"
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/skills"

install_collection() {
  local name="$1" from="$2" to="$3"
  if [ ! -d "$from" ]; then
    echo "skip: $from not found"
    return
  fi
  mkdir -p "$to"
  cp -R "$from"/. "$to"/
  local count
  count=$(find "$to" -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')
  echo "installed $name -> $to ($count skills)"
}

case "$TARGET" in
  claude)
    install_collection "Claude Code" "$SRC/claude" "$HOME/.claude/skills"
    ;;
  opencode)
    install_collection "OpenCode" "$SRC/opencode" "$HOME/.config/opencode/skills"
    ;;
  all)
    install_collection "Claude Code" "$SRC/claude" "$HOME/.claude/skills"
    install_collection "OpenCode" "$SRC/opencode" "$HOME/.config/opencode/skills"
    ;;
  *)
    echo "usage: $0 [all|claude|opencode]" >&2
    exit 1
    ;;
esac

echo
echo "Done. Restart the agent (or start a new session) to pick up the skills."
