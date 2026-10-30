#!/usr/bin/env bash
# Halloween Theme Pack — One-command installer
# Usage: curl -fsSL https://raw.githubusercontent.com/kichiemon/halloween-theme-pack/main/install.sh | bash

set -euo pipefail

REPO="kichiemon/halloween-theme-pack"
BRANCH="main"
BASE_URL="https://raw.githubusercontent.com/${REPO}/${BRANCH}"

echo "🎃 Halloween Theme Pack Installer"
echo "================================"
echo ""

# Detect OS
OS="$(uname -s)"
ARCH="$(uname -m)"
echo "Detected: ${OS} (${ARCH})"
echo ""

# Choose variant
echo "Which variant do you want?"
echo "  1) Halloween (Dark) — deep purple night"
echo "  2) Halloween Day (Light) — warm cream"
echo "  3) Halloween OLED (Pure Void)"
echo "  4) Halloween Pastel (Spooky Kawaii)"
echo "  5) Halloween Cyberpunk (Neon Plasma)"
read -rp "Choice [1]: " VARIANT_CHOICE
VARIANT_CHOICE="${VARIANT_CHOICE:-1}"

case "$VARIANT_CHOICE" in
  1) VARIANT="dark"; VDIR="" ;;
  2) VARIANT="light"; VDIR="light/" ;;
  3) VARIANT="oled"; VDIR="variants/oled/" ;;
  4) VARIANT="pastel"; VDIR="variants/pastel/" ;;
  5) VARIANT="cyberpunk"; VDIR="variants/cyberpunk/" ;;
  *) echo "Invalid choice"; exit 1 ;;
esac

echo ""
echo "Installing ${VARIANT} variant..."
echo ""

# Create temp dir
TMPDIR="$(mktemp -d)"
trap 'rm -rf "$TMPDIR"' EXIT

# Download binary
echo "Downloading halloween-gen binary..."
if [ "$OS" = "Darwin" ]; then
  if [ "$ARCH" = "arm64" ]; then
    BINARY="halloween-gen-macos-arm64"
  else
    BINARY="halloween-gen-macos-x86_64"
  fi
else
  BINARY="halloween-gen-linux-x86_64"
fi

curl -fsSL "https://github.com/${REPO}/releases/latest/download/${BINARY}" -o "${TMPDIR}/halloween-gen" 2>/dev/null || {
  echo "Binary not found in releases. Falling back to generating from source..."
  echo "Please install Python 3.9+ and run: python3 generate.py"
  exit 1
}
chmod +x "${TMPDIR}/halloween-gen"

# Generate themes
echo "Generating theme files..."
"${TMPDIR}/halloween-gen" --out "${TMPDIR}/themes" 2>/dev/null || {
  echo "Generation failed. Please check the binary."
  exit 1
}

echo ""
echo "✅ Theme files generated in: ${TMPDIR}/themes"
echo ""
echo "Next steps:"
echo "  1. Browse themes in: ${TMPDIR}/themes/"
echo "  2. Copy the relevant file to your app's config directory"
echo "  3. See README.md for per-app install instructions:"
echo "     https://github.com/${REPO}#-installation-guide"
echo ""
echo "🎃 Happy Halloween!"
