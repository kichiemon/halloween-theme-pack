#!/usr/bin/env python3
"""Generate Halloween theme files for multiple apps from one palette.

Usage:
    python3 generate.py            # writes to ./out/
    python3 generate.py --out DIR  # custom output dir
"""
import argparse
import json
import os
import struct

# ---------- Palette (single source of truth) ----------
P = {
    "name": "Halloween",
    "background": "#1a0d2e",
    "foreground": "#f4e7d3",
    "card": "#241340",
    "secondary": "#2d1b4e",
    "muted": "#b8a9d9",
    "border": "#3d2a5e",
    "sidebar": "#150a24",
    "accent": "#ff6b35",      # pumpkin
    "success": "#39ff14",     # slime green
    "destructive": "#ff4d6d", # blood red
    "cursor": "#ff6b35",
    "selection": "#3d2a5e",
}
ANSI = {
    "black": "#2d1b4e", "red": "#ff4d6d", "green": "#39ff14",
    "yellow": "#ffb347", "blue": "#6b8cff", "magenta": "#c77dff",
    "cyan": "#5ffbf1", "white": "#f4e7d3",
}
BRIGHT = {
    "black": "#4a3570", "red": "#ff7a95", "green": "#7fff6b",
    "yellow": "#ffd28a", "blue": "#9db3ff", "magenta": "#ddb3ff",
    "cyan": "#9dfff7", "white": "#fff5e6",
}
ORDER = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]


def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) / 255.0 for i in (0, 2, 4))


def hex2tuple(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def ensure(d):
    os.makedirs(d, exist_ok=True)


# ---------- Terminal formats ----------

def gen_warp(out):
    lines = [
        f"name: {P['name']}",
        f"accent: '{P['accent']}'",
        f"cursor: '{P['cursor']}'",
        f"background: '{P['background']}'",
        "details: darker",
        f"foreground: '{P['foreground']}'",
        "",
        "terminal_colors:",
        "  normal:",
    ]
    for k in ORDER:
        lines.append(f"    {k}: '{ANSI[k]}'")
    lines.append("  bright:")
    for k in ORDER:
        lines.append(f"    {k}: '{BRIGHT[k]}'")
    lines.append("")
    with open(os.path.join(out, "halloween.yaml"), "w") as f:
        f.write("\n".join(lines))


def gen_itermcolors(out):
    def color_block(hexv):
        r, g, b = hex2rgb(hexv)
        return (
            "<dict>\n"
            "  <key>Color Space</key>\n  <string>sRGB</string>\n"
            f"  <key>Red Component</key>\n  <real>{r:.6f}</real>\n"
            f"  <key>Green Component</key>\n  <real>{g:.6f}</real>\n"
            f"  <key>Blue Component</key>\n  <real>{b:.6f}</real>\n"
            "  <key>Alpha Component</key>\n  <real>1.000000</real>\n"
            "</dict>"
        )
    mapping = {}
    for i, k in enumerate(ORDER):
        mapping[f"Ansi {i} Color"] = ANSI[k]
    for i, k in enumerate(ORDER):
        mapping[f"Ansi {i + 8} Color"] = BRIGHT[k]
    mapping["Background Color"] = P["background"]
    mapping["Foreground Color"] = P["foreground"]
    mapping["Cursor Color"] = P["cursor"]
    mapping["Selection Color"] = P["selection"]
    mapping["Cursor Text Color"] = P["background"]
    mapping["Bold Color"] = P["foreground"]
    body = []
    for key, val in mapping.items():
        body.append(f"  <key>{key}</key>\n  {color_block(val)}")
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" '
        '"http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n'
        '<plist version="1.0">\n<dict>\n' + "\n".join(body) + "\n</dict>\n</plist>\n"
    )
    with open(os.path.join(out, "halloween.itermcolors"), "w") as f:
        f.write(xml)


def gen_ghostty(out):
    lines = [
        f"# {P['name']} theme for Ghostty",
        f"background = {P['background'].lstrip('#')}",
        f"foreground = {P['foreground'].lstrip('#')}",
        f"cursor-color = {P['cursor'].lstrip('#')}",
        f"selection-background = {P['selection'].lstrip('#')}",
    ]
    for i, k in enumerate(ORDER):
        lines.append(f"palette = {i}={ANSI[k]}")
    for i, k in enumerate(ORDER):
        lines.append(f"palette = {i + 8}={BRIGHT[k]}")
    lines.append("")
    with open(os.path.join(out, "halloween.ghostty"), "w") as f:
        f.write("\n".join(lines))


def gen_alacritty(out):
    ansi_list = [ANSI[k] for k in ORDER]
    bright_list = [BRIGHT[k] for k in ORDER]
    toml = f'''# {P['name']} theme for Alacritty
[colors.primary]
background = "{P['background']}"
foreground = "{P['foreground']}"

[colors.cursor]
text = "{P['background']}"
cursor = "{P['cursor']}"

[colors.selection]
text = "{P['foreground']}"
background = "{P['selection']}"

[colors.normal]
black = "{ansi_list[0]}"
red = "{ansi_list[1]}"
green = "{ansi_list[2]}"
yellow = "{ansi_list[3]}"
blue = "{ansi_list[4]}"
magenta = "{ansi_list[5]}"
cyan = "{ansi_list[6]}"
white = "{ansi_list[7]}"

[colors.bright]
black = "{bright_list[0]}"
red = "{bright_list[1]}"
green = "{bright_list[2]}"
yellow = "{bright_list[3]}"
blue = "{bright_list[4]}"
magenta = "{bright_list[5]}"
cyan = "{bright_list[6]}"
white = "{bright_list[7]}"
'''
    with open(os.path.join(out, "halloween.alacritty.toml"), "w") as f:
        f.write(toml)


def gen_wezterm(out):
    ansi_list = [ANSI[k] for k in ORDER]
    bright_list = [BRIGHT[k] for k in ORDER]
    toml = f'''# {P['name']} theme for WezTerm
[colors]
background = "{P['background']}"
foreground = "{P['foreground']}"
cursor_bg = "{P['cursor']}"
cursor_fg = "{P['background']}"
selection_bg = "{P['selection']}"
selection_fg = "{P['foreground']}"

ansi = {json.dumps(ansi_list)}
brights = {json.dumps(bright_list)}
'''
    with open(os.path.join(out, "halloween.wezterm.toml"), "w") as f:
        f.write(toml)


def gen_kitty(out):
    lines = [f"# {P['name']} theme for kitty", f"background {P['background']}",
             f"foreground {P['foreground']}", f"cursor {P['cursor']}",
             f"selection_background {P['selection']}",
             f"selection_foreground {P['foreground']}", ""]
    for i, k in enumerate(ORDER):
        lines.append(f"color{i} {ANSI[k]}")
    for i, k in enumerate(ORDER):
        lines.append(f"color{i + 8} {BRIGHT[k]}")
    lines.append("")
    with open(os.path.join(out, "halloween.kitty.conf"), "w") as f:
        f.write("\n".join(lines))


# ---------- Editor formats ----------

def gen_vscode(out):
    ansi = [ANSI[k] for k in ORDER]
    theme = {
        "name": P["name"],
        "type": "dark",
        "colors": {
            "editor.background": P["background"],
            "editor.foreground": P["foreground"],
            "editorCursor.foreground": P["cursor"],
            "editor.selectionBackground": P["selection"],
            "editorLineNumber.foreground": P["muted"],
            "editorLineNumber.activeForeground": P["accent"],
            "activityBar.background": P["sidebar"],
            "activityBar.foreground": P["foreground"],
            "activityBar.activeBorder": P["accent"],
            "sideBar.background": P["sidebar"],
            "sideBar.foreground": P["foreground"],
            "sideBarTitle.foreground": P["accent"],
            "statusBar.background": P["secondary"],
            "statusBar.foreground": P["foreground"],
            "titleBar.activeBackground": P["background"],
            "titleBar.activeForeground": P["foreground"],
            "panel.background": P["background"],
            "terminal.background": P["background"],
            "terminal.foreground": P["foreground"],
            "terminal.ansiBlack": ansi[0],
            "terminal.ansiRed": ansi[1],
            "terminal.ansiGreen": ansi[2],
            "terminal.ansiYellow": ansi[3],
            "terminal.ansiBlue": ansi[4],
            "terminal.ansiMagenta": ansi[5],
            "terminal.ansiCyan": ansi[6],
            "terminal.ansiWhite": ansi[7],
            "button.background": P["accent"],
            "button.foreground": P["background"],
            "input.background": P["secondary"],
            "input.border": P["border"],
            "focusBorder": P["accent"],
            "list.activeSelectionBackground": P["secondary"],
            "list.hoverBackground": P["card"],
            "badge.background": P["accent"],
            "badge.foreground": P["background"],
        },
        "tokenColors": [
            {"scope": ["comment", "punctuation.definition.comment"], "settings": {"foreground": P["muted"], "fontStyle": "italic"}},
            {"scope": ["keyword", "storage.type", "storage.modifier"], "settings": {"foreground": P["accent"]}},
            {"scope": ["string", "string.quoted"], "settings": {"foreground": P["success"]}},
            {"scope": ["constant.numeric"], "settings": {"foreground": P["destructive"]}},
            {"scope": ["entity.name.function", "support.function"], "settings": {"foreground": P["blue"] if False else "#6b8cff"}},
            {"scope": ["variable", "variable.other"], "settings": {"foreground": P["foreground"]}},
            {"scope": ["entity.name.type", "support.type", "support.class"], "settings": {"foreground": P["magenta"] if False else "#c77dff"}},
            {"scope": ["keyword.operator"], "settings": {"foreground": P["cyan"] if False else "#5ffbf1"}},
        ],
    }
    # fix color refs
    theme["tokenColors"][4]["settings"]["foreground"] = "#6b8cff"
    theme["tokenColors"][6]["settings"]["foreground"] = "#c77dff"
    theme["tokenColors"][7]["settings"]["foreground"] = "#5ffbf1"
    with open(os.path.join(out, "halloween-vscode.json"), "w") as f:
        json.dump(theme, f, indent=2)
        f.write("\n")


# ---------- App formats ----------

def gen_slack(out):
    # Slack theme string: column_bg,menu_bg,active_item,active_item_text,hover_item,mention_badge,text_color,active_presence,mention_badge_text
    s = ",".join([
        P["background"], P["secondary"], P["accent"], P["background"],
        P["card"], P["foreground"], P["foreground"], P["success"], P["destructive"],
    ])
    with open(os.path.join(out, "halloween-slack.txt"), "w") as f:
        f.write(s + "\n")


def gen_discord(out):
    css = f"""/* {P['name']} theme for Discord (BetterDiscord) */
.theme-dark {{
  --background-primary: {P['background']};
  --background-secondary: {P['secondary']};
  --background-secondary-alt: {P['card']};
  --background-tertiary: {P['sidebar']};
  --background-accent: {P['accent']};
  --text-normal: {P['foreground']};
  --text-muted: {P['muted']};
  --interactive-normal: {P['muted']};
  --interactive-hover: {P['foreground']};
  --interactive-active: {P['accent']};
  --brand-experiment: {P['accent']};
  --status-positive: {P['success']};
  --status-danger: {P['destructive']};
}}
"""
    with open(os.path.join(out, "halloween-discord.css"), "w") as f:
        f.write(css)


def gen_tmux(out):
    conf = f"""# {P['name']} theme for tmux
set -g status-style "bg={P['secondary']},fg={P['foreground']}"
set -g status-left-style "bg={P['accent']},fg={P['background']},bold"
set -g status-right-style "bg={P['secondary']},fg={P['muted']}"
set -g pane-border-style "fg={P['border']}"
set -g pane-active-border-style "fg={P['accent']}"
set -g message-style "bg={P['accent']},fg={P['background']}"
set -g mode-style "bg={P['accent']},fg={P['background']}"
setw -g window-status-style "fg={P['muted']}"
setw -g window-status-current-style "fg={P['accent']},bold"
"""
    with open(os.path.join(out, "halloween.tmux.conf"), "w") as f:
        f.write(conf)


def gen_zsh(out):
    conf = f"""# {P['name']} theme for zsh prompt
PROMPT='%F{{{P['accent']}}}%n%f@%F{{{P['magenta'] if False else '#c77dff'}}}%m%f %F{{{P['muted']}}}%~%f %F{{{P['accent']}}}❯%f '
# success/fail indicator colors
ZSH_HIGHLIGHT_STYLES[command]='fg={P['success']}'
ZSH_HIGHLIGHT_STYLES[unknown-token]='fg={P['destructive']}'
"""
    conf = conf.replace("P['magenta'] if False else '#c77dff'", "#c77dff")
    with open(os.path.join(out, "halloween.zsh"), "w") as f:
        f.write(conf)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="themes")
    args = ap.parse_args()
    base = args.out
    term = os.path.join(base, "terminal")
    edit = os.path.join(base, "editor")
    app = os.path.join(base, "app")
    for d in (base, term, edit, app):
        ensure(d)

    gen_warp(term)
    gen_itermcolors(term)
    gen_ghostty(term)
    gen_alacritty(term)
    gen_wezterm(term)
    gen_kitty(term)
    gen_vscode(edit)
    gen_slack(app)
    gen_discord(app)
    gen_tmux(app)
    gen_zsh(app)

    # copy the canonical warp yaml to repo root location name
    print("Generated theme files under", base)
    for root, _, files in os.walk(base):
        for fn in sorted(files):
            print(" ", os.path.relpath(os.path.join(root, fn), base))


if __name__ == "__main__":
    main()
