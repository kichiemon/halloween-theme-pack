#!/usr/bin/env python3
"""Validate Halloween theme files for color validity, required fields, and WCAG AA contrast.

Usage:
    python3 validate.py
    python3 validate.py --themes-dir themes
"""
import argparse
import json
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
        self.strict_hex_regex = re.compile(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")

    def assert_true(self, condition: bool, description: str, error_msg: str):
        if condition:
            self.passed.append(description)
        else:
            self.failed.append((description, error_msg))

    def validate_hex_colors_in_file(self, filepath: str):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        candidates = re.findall(r"#[0-9a-zA-Z]+", content)
        for hex_str in candidates:
            if len(hex_str) in (4, 7):
                is_valid = bool(self.strict_hex_regex.match(hex_str))
                self.assert_true(
                    is_valid,
                    f"Hex color format in {os.path.basename(filepath)}: {hex_str}",
                    f"Invalid hex color format: {hex_str} (expected #RGB or #RRGGBB)"
                )

    def validate_warp(self, filepath: str, expected_name: str, expected_details: str):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
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

    # ---------- New Formats Validators ----------

    def validate_k9s(self, filepath: str):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        for field in ["k9s:", "body:", "prompt:", "dialog:", "frame:", "views:", "table:", "yaml:"]:
            self.assert_true(field in content, f"K9s field '{field}' in {filepath}", f"Missing field {field}")

    def validate_raycast(self, filepath: str, expected_name: str, expected_type: str):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assert_true(data.get("name") == expected_name, f"Raycast name in {filepath}", f"Expected name {expected_name}")
            self.assert_true(data.get("appearance") == expected_type, f"Raycast appearance in {filepath}", f"Expected appearance {expected_type}")
            colors = data.get("colors", {})
            for c in ["background", "text", "accent", "red", "green", "blue", "yellow", "cyan", "magenta"]:
                self.assert_true(c in colors, f"Raycast color '{c}' in {filepath}", f"Missing color {c}")
            share_url = data.get("shareUrl", "")
            self.assert_true(share_url.startswith("raycast://theme?data="), f"Raycast shareUrl in {filepath}", "Missing or invalid shareUrl")
        except Exception as e:
            self.assert_true(False, f"Raycast JSON valid in {filepath}", f"Invalid JSON: {e}")

    def validate_base16(self, filepath: str, expected_name: str):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        self.assert_true(f'scheme: "{expected_name}"' in content, f"Base16 scheme name in {filepath}", f"Missing scheme: {expected_name}")
        self.assert_true('system: "base16"' in content, f"Base16 system spec in {filepath}", "Missing system: base16")
        for i in range(16):
            base_key = f"base0{hex(i)[2:].upper()}" if i < 16 else ""
            self.assert_true(f"{base_key}:" in content, f"Base16 key '{base_key}' in {filepath}", f"Missing key {base_key}")

    def validate_obsidian_css(self, filepath: str, expected_type: str):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        expected_class = f".theme-{expected_type}"
        self.assert_true(expected_class in content, f"Obsidian class '{expected_class}' in {filepath}", f"Missing {expected_class}")
        for var in ["--background-primary:", "--text-normal:", "--interactive-accent:", "--text-accent:"]:
            self.assert_true(var in content, f"Obsidian CSS var '{var}' in {filepath}", f"Missing var {var}")

    def validate_obsidian_manifest(self, filepath: str, expected_name: str):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assert_true(data.get("name") == expected_name, f"Obsidian manifest name in {filepath}", f"Expected name {expected_name}")
            self.assert_true("version" in data and "author" in data, f"Obsidian manifest fields in {filepath}", "Missing version or author")
        except Exception as e:
            self.assert_true(False, f"Obsidian manifest JSON valid in {filepath}", f"Invalid JSON: {e}")

    def validate_yazi(self, filepath: str):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        for sec in ["[mgr]", "[status]", "[select]", "[input]", "[completion]"]:
            self.assert_true(sec in content, f"Yazi section '{sec}' in {filepath}", f"Missing section {sec}")
        for k in ["cwd =", "hovered =", "find_keyword =", "marker_copied ="]:
            self.assert_true(k in content, f"Yazi key '{k}' in {filepath}", f"Missing key {k}")

    def validate_lazydocker(self, filepath: str):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        for field in ["gui:", "theme:", "activeBorderColor:", "inactiveBorderColor:", "selectedLineBgColor:"]:
            self.assert_true(field in content, f"Lazydocker field '{field}' in {filepath}", f"Missing field {field}")

    def validate_xcode(self, filepath: str):
        try:
            with open(filepath, "rb") as f:
                plist = plistlib.load(f)
            self.assert_true(isinstance(plist, dict), f"Xcode plist parsed in {filepath}", "Xcode root is not a dict")
            for k in ["DVTSourceTextBackground", "DVTSourceTextForeground", "DVTSourceTextInsertionPointColor", "DVTSourceTextSyntaxColors"]:
                self.assert_true(k in plist, f"Xcode key '{k}' in {filepath}", f"Missing key {k}")
            syntax_dict = plist.get("DVTSourceTextSyntaxColors", {})
            for sk in ["xcode.syntax.keyword", "xcode.syntax.string", "xcode.syntax.comment", "xcode.syntax.number"]:
                self.assert_true(sk in syntax_dict, f"Xcode syntax key '{sk}' in {filepath}", f"Missing syntax key {sk}")
        except Exception as e:
            self.assert_true(False, f"Xcode parsing {filepath}", f"Failed to parse plist: {e}")

    def validate_glamour(self, filepath: str):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            for k in ["document", "heading", "link", "code", "strong"]:
                self.assert_true(k in data, f"Glamour element '{k}' in {filepath}", f"Missing element {k}")
        except Exception as e:
            self.assert_true(False, f"Glamour JSON valid in {filepath}", f"Invalid JSON: {e}")

    def validate_pywal(self, filepath: str):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assert_true("special" in data and "colors" in data, f"Pywal structure in {filepath}", "Missing special or colors")
            for i in range(16):
                self.assert_true(f"color{i}" in data.get("colors", {}), f"Pywal color{i} in {filepath}", f"Missing color{i}")
        except Exception as e:
            self.assert_true(False, f"Pywal JSON valid in {filepath}", f"Invalid JSON: {e}")

    def validate_tokens(self, filepath: str):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            color_group = data.get("color", {})
            for k in ["background", "foreground", "accent", "success", "destructive"]:
                self.assert_true(k in color_group and "$value" in color_group[k], f"Token '{k}' in {filepath}", f"Missing token {k}")
        except Exception as e:
            self.assert_true(False, f"Tokens JSON valid in {filepath}", f"Invalid JSON: {e}")

    def validate_fish(self, filepath: str):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        for cmd in ["set -g fish_color_normal", "set -g fish_color_command", "set -g fish_color_quote", "set -g fish_color_error"]:
            self.assert_true(cmd in content, f"fish command '{cmd}' in {filepath}", f"Missing command {cmd}")

    def validate_starship(self, filepath: str, expected_id: str):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        self.assert_true(f'palette = "{expected_id}"' in content, f"Starship palette assignment in {filepath}", f"Missing palette = '{expected_id}'")
        self.assert_true(f"[palettes.{expected_id}]" in content, f"Starship palette table in {filepath}", f"Missing table [palettes.{expected_id}]")
        for k in ["background =", "foreground =", "accent =", "success =", "destructive ="]:
            self.assert_true(k in content, f"Starship key '{k}' in {filepath}", f"Missing key {k}")

    def validate_oh_my_posh(self, filepath: str):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assert_true("palette" in data and "blocks" in data, f"oh-my-posh structure in {filepath}", "Missing palette or blocks")
            pal = data.get("palette", {})
            for k in ["background", "foreground", "accent", "success", "destructive"]:
                self.assert_true(k in pal, f"oh-my-posh palette key '{k}' in {filepath}", f"Missing palette key {k}")
        except Exception as e:
            self.assert_true(False, f"oh-my-posh JSON valid in {filepath}", f"Invalid JSON: {e}")

    def validate_btop(self, filepath: str):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        for k in ["theme[main_bg]=", "theme[main_fg]=", "theme[title]=", "theme[cpu_start]=", "theme[temp_start]="]:
            self.assert_true(k in content, f"btop setting '{k}' in {filepath}", f"Missing setting {k}")

    def validate_tig(self, filepath: str):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        for k in ["color default", "color cursor", "color diff-header", "color diff-add", "color diff-del"]:
            self.assert_true(k in content, f"tig setting '{k}' in {filepath}", f"Missing setting {k}")

    def validate_gitui(self, filepath: str):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        for k in ["selected_tab =", "command_fg =", "selection_bg =", "diff_line_add =", "diff_line_delete ="]:
            self.assert_true(k in content, f"gitui key '{k}' in {filepath}", f"Missing key {k}")

    def validate_zed(self, filepath: str, expected_name: str, expected_appearance: str):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assert_true(data.get("name") == expected_name, f"Zed theme root name in {filepath}", f"Expected name {expected_name}")
            themes_list = data.get("themes", [])
            self.assert_true(len(themes_list) > 0, f"Zed themes array in {filepath}", "Empty themes list")
            theme = themes_list[0]
            self.assert_true(theme.get("appearance") == expected_appearance, f"Zed appearance in {filepath}", f"Expected {expected_appearance}")
            style = theme.get("style", {})
            for k in ["background", "editor.foreground", "editor.background", "terminal.background", "syntax"]:
                self.assert_true(k in style, f"Zed style key '{k}' in {filepath}", f"Missing style key {k}")
            syntax = style.get("syntax", {})
            for sk in ["comment", "keyword", "string", "function", "number"]:
                self.assert_true(sk in syntax, f"Zed syntax key '{sk}' in {filepath}", f"Missing syntax key {sk}")
        except Exception as e:
            self.assert_true(False, f"Zed JSON valid in {filepath}", f"Invalid JSON: {e}")

    def validate_spicetify_ini(self, filepath: str, expected_section: str):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        self.assert_true(f"[{expected_section}]" in content, f"Spicetify INI section [{expected_section}] in {filepath}", f"Missing section [{expected_section}]")
        for k in ["text", "subtext", "main", "sidebar", "player", "card", "button", "notification"]:
            self.assert_true(f"{k} " in content or f"{k}=" in content, f"Spicetify INI key '{k}' in {filepath}", f"Missing key {k}")

    def validate_spicetify_css(self, filepath: str):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        self.assert_true(":root {" in content, f"Spicetify CSS :root in {filepath}", "Missing :root block")
        for var in ["--spice-text:", "--spice-main:", "--spice-sidebar:", "--spice-button:", "--spice-card:"]:
            self.assert_true(var in content, f"Spicetify CSS var '{var}' in {filepath}", f"Missing var {var}")

    def validate_wallpaper_svg(self, filepath: str):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        self.assert_true("<svg" in content and "</svg>" in content, f"SVG tag structure in {filepath}", "Missing svg tags")
        self.assert_true('viewBox="0 0 3840 2160"' in content, f"SVG 4K viewBox in {filepath}", "Missing 4K viewBox")
        self.assert_true("halloweenBgGradient" in content, f"SVG background gradient in {filepath}", "Missing halloweenBgGradient")

    def validate_chrome(self, filepath: str):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assert_true(data.get("manifest_version") in (2, 3), f"Chrome manifest_version in {filepath}", "Invalid manifest_version")
            theme = data.get("theme", {})
            self.assert_true("colors" in theme, f"Chrome theme colors in {filepath}", "Missing colors")
        except Exception as e:
            self.assert_true(False, f"Chrome JSON valid in {filepath}", f"Invalid JSON: {e}")

    def validate_nvim(self, filepath: str):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        self.assert_true("vim.cmd" in content or "vim.api" in content or "highlight" in content, f"Neovim Lua structure in {filepath}", "Missing nvim lua syntax")

    def validate_helix(self, filepath: str):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        for k in ["background =", "foreground =", "accent ="]:
            self.assert_true(k in content, f"Helix key '{k}' in {filepath}", f"Missing key {k}")

    def validate_sublime(self, filepath: str, expected_name: str):
        try:
            with open(filepath, "rb") as f:
                plist = plistlib.load(f)
            self.assert_true(plist.get("name") == expected_name, f"Sublime theme name in {filepath}", f"Expected name {expected_name}")
            self.assert_true("settings" in plist, f"Sublime settings array in {filepath}", "Missing settings")
        except Exception as e:
            self.assert_true(False, f"Sublime plist valid in {filepath}", f"Invalid plist: {e}")

    def run_all(self) -> bool:
        print("=" * 60)
        print("🎃 Halloween Theme Pack - Validation Suite")
        print("=" * 60)

        # 1. Palette Contrast Validation (WCAG AA: >= 4.5:1)
        print("\n[1/5] Checking WCAG AA Contrast Ratios (text >= 4.5:1)...")
        from generate import DARK_PALETTE, LIGHT_PALETTE, OLED_PALETTE, PASTEL_PALETTE, CYBERPUNK_PALETTE, VAMPIRE_PALETTE, PHANTOM_PALETTE

        palettes_to_check = [
            ("Dark (Halloween)", DARK_PALETTE),
            ("Light (Halloween Day)", LIGHT_PALETTE),
            ("OLED (Pure Void)", OLED_PALETTE),
            ("Pastel (Spooky Kawaii)", PASTEL_PALETTE),
            ("Cyberpunk (Neon Pumpkin)", CYBERPUNK_PALETTE),
            ("Vampire Velvet", VAMPIRE_PALETTE),
            ("Phantom Mint", PHANTOM_PALETTE),
        ]

        for pal_label, pal in palettes_to_check:
            bg = pal["background"]
            fg = pal["foreground"]
            c_text = contrast_ratio(bg, fg)
            self.assert_true(
                c_text >= 4.5,
                f"{pal_label} fg/bg contrast ({c_text:.2f}:1)",
                f"Contrast ratio {c_text:.2f}:1 does not satisfy WCAG AA 4.5:1"
            )
            c_accent = contrast_ratio(bg, pal["accent"])
            self.assert_true(
                c_accent >= 4.5,
                f"{pal_label} accent/bg contrast ({c_accent:.2f}:1)",
                f"Accent contrast ratio {c_accent:.2f}:1 does not satisfy WCAG AA 4.5:1"
            )
            print(f"  ✓ {pal_label}: text {c_text:.2f}:1, accent {c_accent:.2f}:1 (WCAG AA Pass)")

        # 2. Duplicate Theme Names
        print("\n[2/5] Checking Theme Names (No duplicate collisions)...")
        all_pals = [DARK_PALETTE, LIGHT_PALETTE, OLED_PALETTE, PASTEL_PALETTE, CYBERPUNK_PALETTE, VAMPIRE_PALETTE, PHANTOM_PALETTE]
        names = [p["name"] for p in all_pals]
        self.assert_true(len(names) == len(set(names)), "Distinct theme names for all variants", f"Duplicate theme names detected: {names}")
        for p in all_pals:
            print(f"  ✓ Theme variant: '{p['name']}' (id: '{p['id']}')")

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
            ("terminal/halloween.k9s.yaml", "k9s"),
            ("terminal/halloween.base16.yaml", "base16"),
            ("terminal/halloween.yazi.toml", "yazi"),
            ("terminal/halloween.glamour.json", "glamour"),
            ("terminal/halloween.colors-wal.json", "pywal"),
            ("terminal/halloween.btop.theme", "btop"),
            ("editor/halloween-vscode.json", "vscode"),
            ("editor/halloween.obsidian.css", "obsidian_css"),
            ("editor/halloween-obsidian-manifest.json", "obsidian_manifest"),
            ("editor/halloween.xccolortheme", "xcode"),
            ("editor/halloween.nvim.lua", "nvim"),
            ("editor/halloween.helix.toml", "helix"),
            ("editor/halloween.sublime-tmTheme", "sublime"),
            ("editor/halloween-zed.json", "zed"),
            ("app/halloween-slack.txt", "slack"),
            ("app/halloween-discord.css", "discord"),
            ("app/halloween.tmux.conf", "tmux"),
            ("app/halloween.zsh", "zsh"),
            ("app/halloween.raycast.json", "raycast"),
            ("app/halloween.lazydocker.yaml", "lazydocker"),
            ("app/halloween.tokens.json", "tokens"),
            ("app/halloween.fish", "fish"),
            ("app/halloween.starship.toml", "starship"),
            ("app/halloween.omp.json", "omp"),
            ("app/halloween.tigrc", "tig"),
            ("app/halloween.gitui.toml", "gitui"),
            ("app/halloween-chrome.json", "chrome"),
            ("app/halloween.spicetify.ini", "spicetify_ini"),
            ("app/halloween.spicetify.css", "spicetify_css"),
            ("app/halloween-wallpaper.svg", "wallpaper_svg"),
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
            ("light/halloween-light.k9s.yaml", "k9s"),
            ("light/halloween-light.base16.yaml", "base16"),
            ("light/halloween-light.yazi.toml", "yazi"),
            ("light/halloween-light.glamour.json", "glamour"),
            ("light/halloween-light.colors-wal.json", "pywal"),
            ("light/halloween-light.btop.theme", "btop"),
            ("light/halloween-light-vscode.json", "vscode"),
            ("light/halloween-light.obsidian.css", "obsidian_css"),
            ("light/halloween-light-obsidian-manifest.json", "obsidian_manifest"),
            ("light/halloween-light.xccolortheme", "xcode"),
            ("light/halloween-light.nvim.lua", "nvim"),
            ("light/halloween-light.helix.toml", "helix"),
            ("light/halloween-light.sublime-tmTheme", "sublime"),
            ("light/halloween-light-zed.json", "zed"),
            ("light/halloween-light-slack.txt", "slack"),
            ("light/halloween-light-discord.css", "discord"),
            ("light/halloween-light.tmux.conf", "tmux"),
            ("light/halloween-light.zsh", "zsh"),
            ("light/halloween-light.raycast.json", "raycast"),
            ("light/halloween-light.lazydocker.yaml", "lazydocker"),
            ("light/halloween-light.tokens.json", "tokens"),
            ("light/halloween-light.fish", "fish"),
            ("light/halloween-light.starship.toml", "starship"),
            ("light/halloween-light.omp.json", "omp"),
            ("light/halloween-light.tigrc", "tig"),
            ("light/halloween-light.gitui.toml", "gitui"),
            ("light/halloween-light-chrome.json", "chrome"),
            ("light/halloween-light.spicetify.ini", "spicetify_ini"),
            ("light/halloween-light.spicetify.css", "spicetify_css"),
            ("light/halloween-light-wallpaper.svg", "wallpaper_svg"),
        ]

        all_files_to_check = []
        for rel_path, kind in expected_dark_files:
            full = os.path.join(self.themes_dir, rel_path)
            self.assert_true(os.path.isfile(full), f"File exists: {rel_path}", f"File missing: {full}")
            all_files_to_check.append((full, kind, "dark", DARK_PALETTE["name"], DARK_PALETTE["id"]))

        for rel_path, kind in expected_light_files:
            full = os.path.join(self.themes_dir, rel_path)
            self.assert_true(os.path.isfile(full), f"File exists: {rel_path}", f"File missing: {full}")
            all_files_to_check.append((full, kind, "light", LIGHT_PALETTE["name"], LIGHT_PALETTE["id"]))

        # Also verify extra variants under variants/
        variant_specs = [
            ("oled", OLED_PALETTE),
            ("pastel", PASTEL_PALETTE),
            ("cyberpunk", CYBERPUNK_PALETTE),
            ("vampire", VAMPIRE_PALETTE),
            ("phantom", PHANTOM_PALETTE),
        ]
        for var_id, pal in variant_specs:
            pfx = pal["id"]
            var_dir = f"variants/{var_id}"
            var_files = [
                (f"{var_dir}/{pfx}.yaml", "warp"),
                (f"{var_dir}/{pfx}.itermcolors", "itermcolors"),
                (f"{var_dir}/{pfx}.ghostty", "ghostty"),
                (f"{var_dir}/{pfx}.alacritty.toml", "alacritty"),
                (f"{var_dir}/{pfx}.wezterm.toml", "wezterm"),
                (f"{var_dir}/{pfx}.kitty.conf", "kitty"),
                (f"{var_dir}/{pfx}.windows-terminal.json", "windows-terminal"),
                (f"{var_dir}/{pfx}.hyper.js", "hyper"),
                (f"{var_dir}/{pfx}.tabby.yaml", "tabby"),
                (f"{var_dir}/{pfx}.rio.toml", "rio"),
                (f"{var_dir}/{pfx}.k9s.yaml", "k9s"),
                (f"{var_dir}/{pfx}.base16.yaml", "base16"),
                (f"{var_dir}/{pfx}.yazi.toml", "yazi"),
                (f"{var_dir}/{pfx}.glamour.json", "glamour"),
                (f"{var_dir}/{pfx}.colors-wal.json", "pywal"),
                (f"{var_dir}/{pfx}.btop.theme", "btop"),
                (f"{var_dir}/{pfx}-vscode.json", "vscode"),
                (f"{var_dir}/{pfx}.obsidian.css", "obsidian_css"),
                (f"{var_dir}/{pfx}-obsidian-manifest.json", "obsidian_manifest"),
                (f"{var_dir}/{pfx}.xccolortheme", "xcode"),
                (f"{var_dir}/{pfx}.nvim.lua", "nvim"),
                (f"{var_dir}/{pfx}.helix.toml", "helix"),
                (f"{var_dir}/{pfx}.sublime-tmTheme", "sublime"),
                (f"{var_dir}/{pfx}-zed.json", "zed"),
                (f"{var_dir}/{pfx}-slack.txt", "slack"),
                (f"{var_dir}/{pfx}-discord.css", "discord"),
                (f"{var_dir}/{pfx}.tmux.conf", "tmux"),
                (f"{var_dir}/{pfx}.zsh", "zsh"),
                (f"{var_dir}/{pfx}.raycast.json", "raycast"),
                (f"{var_dir}/{pfx}.lazydocker.yaml", "lazydocker"),
                (f"{var_dir}/{pfx}.tokens.json", "tokens"),
                (f"{var_dir}/{pfx}.fish", "fish"),
                (f"{var_dir}/{pfx}.starship.toml", "starship"),
                (f"{var_dir}/{pfx}.omp.json", "omp"),
                (f"{var_dir}/{pfx}.tigrc", "tig"),
                (f"{var_dir}/{pfx}.gitui.toml", "gitui"),
                (f"{var_dir}/{pfx}-chrome.json", "chrome"),
                (f"{var_dir}/{pfx}.spicetify.ini", "spicetify_ini"),
                (f"{var_dir}/{pfx}.spicetify.css", "spicetify_css"),
                (f"{var_dir}/{pfx}-wallpaper.svg", "wallpaper_svg"),
            ]
            for rel_path, kind in var_files:
                full = os.path.join(self.themes_dir, rel_path)
                self.assert_true(os.path.isfile(full), f"File exists: {rel_path}", f"File missing: {full}")
                all_files_to_check.append((full, kind, pal["type"], pal["name"], pal["id"]))

        print(f"  ✓ Total theme files checked across all variants: {len(all_files_to_check)} files")

        # 4. Format and Required Fields Validation
        print("\n[4/5] Checking Required Fields and Format Validity...")
        for full, kind, variant, theme_name, theme_id in all_files_to_check:
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
            elif kind == "k9s":
                self.validate_k9s(full)
            elif kind == "raycast":
                self.validate_raycast(full, theme_name, variant)
            elif kind == "base16":
                self.validate_base16(full, theme_name)
            elif kind == "obsidian_css":
                self.validate_obsidian_css(full, variant)
            elif kind == "obsidian_manifest":
                self.validate_obsidian_manifest(full, theme_name)
            elif kind == "yazi":
                self.validate_yazi(full)
            elif kind == "lazydocker":
                self.validate_lazydocker(full)
            elif kind == "xcode":
                self.validate_xcode(full)
            elif kind == "glamour":
                self.validate_glamour(full)
            elif kind == "pywal":
                self.validate_pywal(full)
            elif kind == "tokens":
                self.validate_tokens(full)
            elif kind == "fish":
                self.validate_fish(full)
            elif kind == "starship":
                self.validate_starship(full, theme_id)
            elif kind == "omp":
                self.validate_oh_my_posh(full)
            elif kind == "btop":
                self.validate_btop(full)
            elif kind == "tig":
                self.validate_tig(full)
            elif kind == "gitui":
                self.validate_gitui(full)
            elif kind == "zed":
                self.validate_zed(full, theme_name, variant)
            elif kind == "spicetify_ini":
                expected_sec = theme_name.replace(" ", "_")
                self.validate_spicetify_ini(full, expected_sec)
            elif kind == "spicetify_css":
                self.validate_spicetify_css(full)
            elif kind == "wallpaper_svg":
                self.validate_wallpaper_svg(full)
            elif kind == "chrome":
                self.validate_chrome(full)
            elif kind == "nvim":
                self.validate_nvim(full)
            elif kind == "helix":
                self.validate_helix(full)
            elif kind == "sublime":
                self.validate_sublime(full, theme_name)

        print(f"  ✓ File structure and required fields validated for all {len(all_files_to_check)} formats")

        # 5. Hex Colors Format
        print("\n[5/5] Scanning Hex Color Syntax in All Files (#RGB or #RRGGBB)...")
        for full, _, _, _, _ in all_files_to_check:
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
