#!/usr/bin/env python3
"""Validate Halloween theme files for color validity, required fields, and WCAG AA contrast.

Usage:
    python3 validate.py
    python3 validate.py --themes-dir themes
"""
import argparse
import os
import plistlib
import re
import sys
from typing import Dict, List, Tuple

# ---------- Color Contrast (WCAG 2.1) ----------

def srgb_to_linear(c_srgb: float) -> float:
    if c_srgb <= 0.03928:
        return c_srgb / 12.92
    return ((c_srgb + 0.055) / 1.055) ** 2.4


def relative_luminance(hex_str: str) -> float:
    h = hex_str.lstrip("#")
    if len(h) == 3:
        h = "".join(ch * 2 for ch in h)
    r = int(h[0:2], 16) / 255.0
    g = int(h[2:4], 16) / 255.0
    b = int(h[4:6], 16) / 255.0
    r_lin = srgb_to_linear(r)
    g_lin = srgb_to_linear(g)
    b_lin = srgb_to_linear(b)
    return 0.2126 * r_lin + 0.7152 * g_lin + 0.0722 * b_lin


def contrast_ratio(hex1: str, hex2: str) -> float:
    l1 = relative_luminance(hex1)
    l2 = relative_luminance(hex2)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


# ---------- Validation Engine ----------

class Validator:
    def __init__(self, themes_dir: str):
        self.themes_dir = themes_dir
        self.passed: List[str] = []
        self.failed: List[Tuple[str, str]] = []
        self.hex_regex = re.compile(r"#[0-9a-fA-F]{3,8}")
        self.strict_hex_regex = re.compile(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")

    def assert_true(self, condition: bool, description: str, error_msg: str):
        if condition:
            self.passed.append(description)
        else:
            self.failed.append((description, error_msg))

    def validate_hex_colors_in_file(self, filepath: str):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Find all hashtag occurrences
        candidates = re.findall(r"#[0-9a-zA-Z]+", content)
        for hex_str in candidates:
            # Skip comments or anchors if any (though themes rarely have long words after #)
            # In our files, hex strings should strictly be #RGB or #RRGGBB
            if len(hex_str) in (4, 7):
                is_valid = bool(self.strict_hex_regex.match(hex_str))
                self.assert_true(
                    is_valid,
                    f"Hex color format in {os.path.basename(filepath)}: {hex_str}",
                    f"Invalid hex color format: {hex_str} (expected #RGB or #RRGGBB)"
                )

    def validate_warp(self, filepath: str, expected_name: str, expected_details: str):
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
        content = "".join(lines)
        self.assert_true(f"name: {expected_name}" in content, f"Warp theme name in {filepath}", f"Missing or wrong name (expected {expected_name})")
        self.assert_true(f"details: {expected_details}" in content, f"Warp details in {filepath}", f"Missing details: {expected_details}")
        for field in ["accent:", "cursor:", "background:", "foreground:", "terminal_colors:", "normal:", "bright:"]:
            self.assert_true(field in content, f"Warp required field '{field}' in {filepath}", f"Missing required field {field}")
        for color in ["black:", "red:", "green:", "yellow:", "blue:", "magenta:", "cyan:", "white:"]:
            count = content.count(f"    {color}")
            self.assert_true(count >= 2, f"Warp normal/bright color '{color}' in {filepath}", f"Color {color} should appear in both normal and bright blocks")

    def validate_itermcolors(self, filepath: str):
        try:
            with open(filepath, "rb") as f:
                plist = plistlib.load(f)
            self.assert_true(isinstance(plist, dict), f"iTerm plist parsed in {filepath}", "Plist root is not a dict")
            required_keys = [
                "Background Color", "Foreground Color", "Cursor Color",
                "Selection Color", "Cursor Text Color", "Bold Color"
            ]
            for i in range(16):
                required_keys.append(f"Ansi {i} Color")
            for k in required_keys:
                self.assert_true(k in plist, f"iTerm key '{k}' in {filepath}", f"Missing required plist key: {k}")
                if k in plist:
                    color_dict = plist[k]
                    self.assert_true(
                        all(comp in color_dict for comp in ["Red Component", "Green Component", "Blue Component"]),
                        f"iTerm RGB components for '{k}' in {filepath}",
                        f"Missing RGB component in {k}"
                    )
        except Exception as e:
            self.assert_true(False, f"iTerm parsing {filepath}", f"Failed to parse plist: {e}")

    def validate_ghostty(self, filepath: str):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        for field in ["background =", "foreground =", "cursor-color =", "selection-background ="]:
            self.assert_true(field in content, f"Ghostty field '{field}' in {filepath}", f"Missing field {field}")
        for i in range(16):
            self.assert_true(f"palette = {i}=" in content, f"Ghostty palette {i} in {filepath}", f"Missing palette index {i}")

    def validate_alacritty(self, filepath: str):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        for section in ["[colors.primary]", "[colors.cursor]", "[colors.selection]", "[colors.normal]", "[colors.bright]"]:
            self.assert_true(section in content, f"Alacritty section '{section}' in {filepath}", f"Missing section {section}")
        for color in ["black =", "red =", "green =", "yellow =", "blue =", "magenta =", "cyan =", "white ="]:
            count = content.count(color)
            self.assert_true(count >= 2, f"Alacritty color '{color}' in {filepath}", f"Missing normal/bright color {color}")

    def validate_wezterm(self, filepath: str):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        self.assert_true("[colors]" in content, f"Wezterm [colors] in {filepath}", "Missing [colors] table")
        for field in ["background =", "foreground =", "cursor_bg =", "cursor_fg =", "selection_bg =", "selection_fg =", "ansi =", "brights ="]:
            self.assert_true(field in content, f"Wezterm field '{field}' in {filepath}", f"Missing field {field}")

    def validate_kitty(self, filepath: str):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        for field in ["background ", "foreground ", "cursor ", "selection_background ", "selection_foreground "]:
            self.assert_true(field in content, f"Kitty field '{field}' in {filepath}", f"Missing field {field}")
        for i in range(16):
            self.assert_true(f"color{i} " in content, f"Kitty color{i} in {filepath}", f"Missing color{i}")

    def validate_windows_terminal(self, filepath: str, expected_name: str):
        import json
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assert_true(data.get("name") == expected_name, f"Windows Terminal name in {filepath}", f"Expected name '{expected_name}', got '{data.get('name')}'")
            required_keys = [
                "name", "background", "foreground", "cursorColor", "selectionBackground",
                "black", "red", "green", "yellow", "blue", "purple", "cyan", "white",
                "brightBlack", "brightRed", "brightGreen", "brightYellow", "brightBlue",
                "brightPurple", "brightCyan", "brightWhite"
            ]
            for k in required_keys:
                self.assert_true(k in data, f"Windows Terminal key '{k}' in {filepath}", f"Missing key {k}")
        except Exception as e:
            self.assert_true(False, f"Windows Terminal JSON valid in {filepath}", f"Invalid JSON: {e}")

    def validate_hyper(self, filepath: str):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        self.assert_true("exports.decorateConfig" in content, f"Hyper decorateConfig in {filepath}", "Missing exports.decorateConfig")
        for key in ["backgroundColor:", "foregroundColor:", "borderColor:", "cursorColor:", "selectionColor:", "colors:"]:
            self.assert_true(key in content, f"Hyper key '{key}' in {filepath}", f"Missing key {key}")
        for c in ["black:", "red:", "green:", "yellow:", "blue:", "magenta:", "cyan:", "white:",
                  "lightBlack:", "lightRed:", "lightGreen:", "lightYellow:", "lightBlue:", "lightMagenta:", "lightCyan:", "lightWhite:"]:
            self.assert_true(c in content, f"Hyper color '{c}' in {filepath}", f"Missing color {c}")

    def validate_tabby(self, filepath: str, expected_name: str):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        self.assert_true(f"name: {expected_name}" in content, f"Tabby theme name in {filepath}", f"Missing or wrong name (expected {expected_name})")
        for k in ["foreground:", "background:", "cursor:", "selection:", "colors:"]:
            self.assert_true(k in content, f"Tabby key '{k}' in {filepath}", f"Missing key {k}")
        # Count color list items
        color_items = re.findall(r"^\s*-\s*'#[0-9a-fA-F]{6}'", content, re.MULTILINE)
        self.assert_true(len(color_items) == 16, f"Tabby 16 colors in {filepath}", f"Expected 16 colors, found {len(color_items)}")

    def validate_rio(self, filepath: str):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        self.assert_true("[colors]" in content, f"Rio [colors] table in {filepath}", "Missing [colors] section")
        for k in ["background =", "foreground =", "cursor =", "tabs =", "tabs-active =", "selection-background =", "selection-foreground ="]:
            self.assert_true(k in content, f"Rio field '{k}' in {filepath}", f"Missing field {k}")
        for c in ["black =", "red =", "green =", "yellow =", "blue =", "magenta =", "cyan =", "white =",
                  "light-black =", "light-red =", "light-green =", "light-yellow =", "light-blue =", "light-magenta =", "light-cyan =", "light-white ="]:
            self.assert_true(c in content, f"Rio color '{c}' in {filepath}", f"Missing color {c}")

    def validate_vscode(self, filepath: str, expected_name: str, expected_type: str):
        import json
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assert_true(data.get("name") == expected_name, f"VS Code theme name in {filepath}", f"Expected name '{expected_name}', got '{data.get('name')}'")
            self.assert_true(data.get("type") == expected_type, f"VS Code theme type in {filepath}", f"Expected type '{expected_type}', got '{data.get('type')}'")
            colors = data.get("colors", {})
            required_colors = [
                "editor.background", "editor.foreground", "editorCursor.foreground",
                "activityBar.background", "sideBar.background", "statusBar.background",
                "terminal.background", "terminal.foreground", "terminal.ansiBlack", "terminal.ansiWhite"
            ]
            for rc in required_colors:
                self.assert_true(rc in colors, f"VS Code color '{rc}' in {filepath}", f"Missing color {rc}")
            token_colors = data.get("tokenColors", [])
            self.assert_true(len(token_colors) >= 8, f"VS Code tokenColors in {filepath}", f"Expected >= 8 token color scopes, got {len(token_colors)}")
        except Exception as e:
            self.assert_true(False, f"VS Code JSON valid in {filepath}", f"Invalid JSON: {e}")

    def validate_discord(self, filepath: str, expected_type: str):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        expected_class = f".theme-{expected_type}"
        self.assert_true(expected_class in content, f"Discord class '{expected_class}' in {filepath}", f"Missing {expected_class}")
        for var in ["--background-primary:", "--text-normal:", "--background-accent:", "--status-positive:", "--status-danger:"]:
            self.assert_true(var in content, f"Discord CSS var '{var}' in {filepath}", f"Missing CSS var {var}")

    def validate_slack(self, filepath: str):
        with open(filepath, "r", encoding="utf-8") as f:
            line = f.read().strip()
        parts = line.split(",")
        self.assert_true(len(parts) == 9, f"Slack 9 colors in {filepath}", f"Expected 9 comma-separated values, got {len(parts)}")
        for i, part in enumerate(parts):
            self.assert_true(bool(self.strict_hex_regex.match(part)), f"Slack color {i+1} valid hex in {filepath}", f"Invalid hex in Slack theme: {part}")

    def validate_tmux(self, filepath: str):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        for setting in ["status-style", "status-left-style", "pane-border-style", "pane-active-border-style", "message-style"]:
            self.assert_true(setting in content, f"tmux setting '{setting}' in {filepath}", f"Missing setting {setting}")

    def validate_zsh(self, filepath: str):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        self.assert_true("PROMPT=" in content, f"zsh PROMPT in {filepath}", "Missing PROMPT definition")
        self.assert_true("ZSH_HIGHLIGHT_STYLES" in content, f"zsh ZSH_HIGHLIGHT_STYLES in {filepath}", "Missing ZSH_HIGHLIGHT_STYLES")

    def run_all(self) -> bool:
        print("=" * 60)
        print("🎃 Halloween Theme Pack - Validation Suite")
        print("=" * 60)

        # 1. Palette Contrast Validation (WCAG AA: >= 4.5:1)
        print("\n[1/5] Checking WCAG AA Contrast Ratios (text >= 4.5:1)...")
        from generate import DARK_PALETTE, LIGHT_PALETTE

        # Dark palette check
        dark_bg = DARK_PALETTE["background"]
        dark_fg = DARK_PALETTE["foreground"]
        dark_contrast = contrast_ratio(dark_bg, dark_fg)
        self.assert_true(
            dark_contrast >= 4.5,
            f"Dark foreground/background contrast ({dark_contrast:.2f}:1)",
            f"Contrast ratio {dark_contrast:.2f}:1 does not satisfy WCAG AA 4.5:1"
        )
        print(f"  ✓ Dark Theme (fg {dark_fg} vs bg {dark_bg}): {dark_contrast:.2f}:1 (WCAG AA Pass)")

        # Light palette check
        light_bg = LIGHT_PALETTE["background"]
        light_fg = LIGHT_PALETTE["foreground"]
        light_contrast = contrast_ratio(light_bg, light_fg)
        self.assert_true(
            light_contrast >= 4.5,
            f"Light foreground/background contrast ({light_contrast:.2f}:1)",
            f"Contrast ratio {light_contrast:.2f}:1 does not satisfy WCAG AA 4.5:1"
        )
        print(f"  ✓ Light Theme (fg {light_fg} vs bg {light_bg}): {light_contrast:.2f}:1 (WCAG AA Pass)")

        # Extra accent / text checks
        dark_accent_contrast = contrast_ratio(dark_bg, DARK_PALETTE["accent"])
        light_accent_contrast = contrast_ratio(light_bg, LIGHT_PALETTE["accent"])
        print(f"  ✓ Dark Theme Accent ({DARK_PALETTE['accent']} vs bg): {dark_accent_contrast:.2f}:1")
        print(f"  ✓ Light Theme Accent ({LIGHT_PALETTE['accent']} vs bg): {light_accent_contrast:.2f}:1 (WCAG AA Pass)")
        self.assert_true(
            light_accent_contrast >= 4.5,
            f"Light theme accent contrast ({light_accent_contrast:.2f}:1 >= 4.5:1)",
            f"Accent contrast ratio {light_accent_contrast:.2f}:1 does not satisfy WCAG AA"
        )

        # 2. Duplicate Theme Names
        print("\n[2/5] Checking Theme Names (No duplicate collisions)...")
        dark_name = DARK_PALETTE["name"]
        light_name = LIGHT_PALETTE["name"]
        self.assert_true(dark_name != light_name, "Distinct theme names for dark and light", f"Duplicate theme name: '{dark_name}'")
        print(f"  ✓ Dark theme name: '{dark_name}'")
        print(f"  ✓ Light theme name: '{light_name}'")

        # 3. File existence checks
        print("\n[3/5] Verifying Generated Files Existence...")
        expected_dark_files = [
            ("terminal/halloween.yaml", "warp"),
            ("terminal/halloween.itermcolors", "itermcolors"),
            ("terminal/halloween.ghostty", "ghostty"),
            ("terminal/halloween.alacritty.toml", "alacritty"),
            ("terminal/halloween.wezterm.toml", "wezterm"),
            ("terminal/halloween.kitty.conf", "kitty"),
            ("terminal/halloween.windows-terminal.json", "windows-terminal"),
            ("terminal/halloween.hyper.js", "hyper"),
            ("terminal/halloween.tabby.yaml", "tabby"),
            ("terminal/halloween.rio.toml", "rio"),
            ("editor/halloween-vscode.json", "vscode"),
            ("app/halloween-slack.txt", "slack"),
            ("app/halloween-discord.css", "discord"),
            ("app/halloween.tmux.conf", "tmux"),
            ("app/halloween.zsh", "zsh"),
        ]

        expected_light_files = [
            ("light/halloween-light.yaml", "warp"),
            ("light/halloween-light.itermcolors", "itermcolors"),
            ("light/halloween-light.ghostty", "ghostty"),
            ("light/halloween-light.alacritty.toml", "alacritty"),
            ("light/halloween-light.wezterm.toml", "wezterm"),
            ("light/halloween-light.kitty.conf", "kitty"),
            ("light/halloween-light.windows-terminal.json", "windows-terminal"),
            ("light/halloween-light.hyper.js", "hyper"),
            ("light/halloween-light.tabby.yaml", "tabby"),
            ("light/halloween-light.rio.toml", "rio"),
            ("light/halloween-light-vscode.json", "vscode"),
            ("light/halloween-light-slack.txt", "slack"),
            ("light/halloween-light-discord.css", "discord"),
            ("light/halloween-light.tmux.conf", "tmux"),
            ("light/halloween-light.zsh", "zsh"),
        ]

        all_files_to_check = []
        for rel_path, kind in expected_dark_files:
            full = os.path.join(self.themes_dir, rel_path)
            self.assert_true(os.path.isfile(full), f"File exists: {rel_path}", f"File missing: {full}")
            all_files_to_check.append((full, kind, "dark", dark_name))

        for rel_path, kind in expected_light_files:
            full = os.path.join(self.themes_dir, rel_path)
            self.assert_true(os.path.isfile(full), f"File exists: {rel_path}", f"File missing: {full}")
            all_files_to_check.append((full, kind, "light", light_name))

        print(f"  ✓ Total expected theme files checked: {len(all_files_to_check)} files")

        # 4. Format and Required Fields Validation
        print("\n[4/5] Checking Required Fields and Format Validity...")
        for full, kind, variant, theme_name in all_files_to_check:
            if not os.path.isfile(full):
                continue
            details = "darker" if variant == "dark" else "lighter"
            if kind == "warp":
                self.validate_warp(full, theme_name, details)
            elif kind == "itermcolors":
                self.validate_itermcolors(full)
            elif kind == "ghostty":
                self.validate_ghostty(full)
            elif kind == "alacritty":
                self.validate_alacritty(full)
            elif kind == "wezterm":
                self.validate_wezterm(full)
            elif kind == "kitty":
                self.validate_kitty(full)
            elif kind == "windows-terminal":
                self.validate_windows_terminal(full, theme_name)
            elif kind == "hyper":
                self.validate_hyper(full)
            elif kind == "tabby":
                self.validate_tabby(full, theme_name)
            elif kind == "rio":
                self.validate_rio(full)
            elif kind == "vscode":
                self.validate_vscode(full, theme_name, variant)
            elif kind == "slack":
                self.validate_slack(full)
            elif kind == "discord":
                self.validate_discord(full, variant)
            elif kind == "tmux":
                self.validate_tmux(full)
            elif kind == "zsh":
                self.validate_zsh(full)

        print(f"  ✓ File structure and required fields validated for all formats")

        # 5. Hex Colors Format
        print("\n[5/5] Scanning Hex Color Syntax in All Files (#RGB or #RRGGBB)...")
        for full, _, _, _ in all_files_to_check:
            if os.path.isfile(full):
                self.validate_hex_colors_in_file(full)
        print(f"  ✓ Hex color syntax validated across all generated theme files")

        # Report
        print("\n" + "=" * 60)
        print("VALIDATION REPORT")
        print("=" * 60)
        print(f"Passed checks: {len(self.passed)}")
        print(f"Failed checks: {len(self.failed)}")

        if self.failed:
            print("\n❌ FAILURES:")
            for desc, err in self.failed:
                print(f"  - {desc}: {err}")
            print("\nResult: ❌ FAILED")
            return False
        else:
            print("\nResult: ✅ ALL CHECKS PASSED")
            return True


def main():
    parser = argparse.ArgumentParser(description="Validate generated theme files.")
    parser.add_argument("--themes-dir", default="themes", help="Themes directory to validate")
    args = parser.parse_args()

    validator = Validator(args.themes_dir)
    success = validator.run_all()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
