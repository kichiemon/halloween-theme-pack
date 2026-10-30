#!/usr/bin/env bash
# Halloween Theme Pack - OS Ambient Auto-Switcher Daemon Wrapper
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
exec python3 "$DIR/scripts/ambient_switcher.py" "$@"
