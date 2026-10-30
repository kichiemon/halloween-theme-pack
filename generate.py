#!/usr/bin/env python3
"""Generate Halloween theme files for multiple apps from one palette.

Usage:
    python3 generate.py            # writes to ./themes/
    python3 generate.py --out DIR  # custom output dir
"""
import argparse
import json
import os

# ---------- Palettes (single source of truth) ----------
DARK_PALETTE = {
    "id": "halloween",
    "name": "Halloween",
    "type": "dark",
    "details": "darker",
    "background": "#1a0d2e",
    "foreground": "#f4e7d3",
    "card": "#241340",
    "secondary": "#2d1b4e",
    "muted": "#b8a9d9",
    "border": "#3d2a5e",
    "sidebar": "#150a24",
    "accent": "#ff6b35",       # pumpkin
    "success": "#39ff14",      # slime green
    "destructive": "#ff4d6d",  # blood red
    "cursor": "#ff6b35",
    "selection": "#3d2a5e",
    "selection_text": "#f4e7d3",
    "blue": "#6b8cff",
    "magenta": "#c77dff",
    "cyan": "#5ffbf1",
    "yellow": "#ffb347",
    "ansi": {
        "black": "#2d1b4e",
        "red": "#ff4d6d",
        "green": "#39ff14",
        "yellow": "#ffb347",
        "blue": "#6b8cff",
        "magenta": "#c77dff",
        "cyan": "#5ffbf1",
        "white": "#f4e7d3",
    },
    "bright": {
        "black": "#4a3570",
        "red": "#ff7a95",
        "green": "#7fff6b",
        "yellow": "#ffd28a",
        "blue": "#9db3ff",
        "magenta": "#ddb3ff",
        "cyan": "#9dfff7",
        "white": "#fff5e6",
    },
}

LIGHT_PALETTE = {
    "id": "halloween-light",
    "name": "Halloween Day",
    "type": "light",
    "details": "lighter",
    "background": "#faf4eb",  # warm cream
    "foreground": "#241432",  # dark purple text
    "card": "#f2e7d8",        # warm bone card
    "secondary": "#e8dcce",   # soft cream-taupe
    "muted": "#756388",       # muted witch purple
    "border": "#d8c8b4",      # parchment border
    "sidebar": "#f4ece1",     # deeper cream
    "accent": "#bf4904",      # rich pumpkin orange (contrast >= 4.5:1)
    "success": "#1b772d",     # herb green (contrast >= 4.5:1)
    "destructive": "#b81438", # blood crimson (contrast >= 4.5:1)
    "cursor": "#bf4904",      # pumpkin cursor
    "selection": "#e5d0b5",   # soft pumpkin parchment
    "selection_text": "#241432",
    "blue": "#2b4acb",
    "magenta": "#7e22ce",
    "cyan": "#0e7490",
    "yellow": "#9e6000",
    "ansi": {
        "black": "#241432",
        "red": "#b81438",
        "green": "#1b772d",
        "yellow": "#9e6000",
        "blue": "#2b4acb",
        "magenta": "#7e22ce",
        "cyan": "#0e7490",
        "white": "#d8ccbc",
    },
    "bright": {
        "black": "#5c4d6b",
        "red": "#cf2248",
        "green": "#228b37",
        "yellow": "#b56f00",
        "blue": "#3b5bdb",
        "magenta": "#9333ea",
        "cyan": "#0284c7",
        "white": "#241432",
    },
}

# Backwards compatibility aliases
P = DARK_PALETTE
ANSI = DARK_PALETTE["ansi"]
BRIGHT = DARK_PALETTE["bright"]
ORDER = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]


def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))


def hex2tuple(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def ensure(d):
    os.makedirs(d, exist_ok=True)


# ---------- Terminal formats ----------

def gen_warp(pal, out_path):
    ansi = pal["ansi"]
    bright = pal["bright"]
    lines = [
        f"name: {pal['name']}",
        f"accent: '{pal['accent']}'",
        f"cursor: '{pal['cursor']}'",
        f"background: '{pal['background']}'",
        f"details: {pal['details']}",
        f"foreground: '{pal['foreground']}'",
        "",
        "terminal_colors:",
        "  normal:",
    ]
    for k in ORDER:
        lines.append(f"    {k}: '{ansi[k]}'")
    lines.append("  bright:")
    for k in ORDER:
        lines.append(f"    {k}: '{bright[k]}'")
    lines.append("")
    with open(out_path, "w") as f:
        f.write("\n".join(lines))


def gen_itermcolors(pal, out_path):
    ansi = pal["ansi"]
    bright = pal["bright"]

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
        mapping[f"Ansi {i} Color"] = ansi[k]
    for i, k in enumerate(ORDER):
        mapping[f"Ansi {i + 8} Color"] = bright[k]
    mapping["Background Color"] = pal["background"]
    mapping["Foreground Color"] = pal["foreground"]
    mapping["Cursor Color"] = pal["cursor"]
    mapping["Selection Color"] = pal["selection"]
    mapping["Cursor Text Color"] = pal["background"]
    mapping["Bold Color"] = pal["foreground"]
    body = []
    for key, val in mapping.items():
        body.append(f"  <key>{key}</key>\n  {color_block(val)}")
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" '
        '"http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n'
        '<plist version="1.0">\n<dict>\n' + "\n".join(body) + "\n</dict>\n</plist>\n"
    )
    with open(out_path, "w") as f:
        f.write(xml)


def gen_ghostty(pal, out_path):
    ansi = pal["ansi"]
    bright = pal["bright"]
    lines = [
        f"# {pal['name']} theme for Ghostty",
        f"background = {pal['background'].lstrip('#')}",
        f"foreground = {pal['foreground'].lstrip('#')}",
        f"cursor-color = {pal['cursor'].lstrip('#')}",
        f"selection-background = {pal['selection'].lstrip('#')}",
    ]
    for i, k in enumerate(ORDER):
        lines.append(f"palette = {i}={ansi[k]}")
    for i, k in enumerate(ORDER):
        lines.append(f"palette = {i + 8}={bright[k]}")
    lines.append("")
    with open(out_path, "w") as f:
        f.write("\n".join(lines))


def gen_alacritty(pal, out_path):
    ansi = pal["ansi"]
    bright = pal["bright"]
    ansi_list = [ansi[k] for k in ORDER]
    bright_list = [bright[k] for k in ORDER]
    toml = f'''# {pal['name']} theme for Alacritty
[colors.primary]
background = "{pal['background']}"
foreground = "{pal['foreground']}"

[colors.cursor]
text = "{pal['background']}"
cursor = "{pal['cursor']}"

[colors.selection]
text = "{pal['selection_text']}"
background = "{pal['selection']}"

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
    with open(out_path, "w") as f:
        f.write(toml)


def gen_wezterm(pal, out_path):
    ansi = pal["ansi"]
    bright = pal["bright"]
    ansi_list = [ansi[k] for k in ORDER]
    bright_list = [bright[k] for k in ORDER]
    toml = f'''# {pal['name']} theme for WezTerm
[colors]
background = "{pal['background']}"
foreground = "{pal['foreground']}"
cursor_bg = "{pal['cursor']}"
cursor_fg = "{pal['background']}"
selection_bg = "{pal['selection']}"
selection_fg = "{pal['selection_text']}"

ansi = {json.dumps(ansi_list)}
brights = {json.dumps(bright_list)}
'''
    with open(out_path, "w") as f:
        f.write(toml)


def gen_kitty(pal, out_path):
    ansi = pal["ansi"]
    bright = pal["bright"]
    lines = [
        f"# {pal['name']} theme for kitty",
        f"background {pal['background']}",
        f"foreground {pal['foreground']}",
        f"cursor {pal['cursor']}",
        f"selection_background {pal['selection']}",
        f"selection_foreground {pal['selection_text']}",
        "",
    ]
    for i, k in enumerate(ORDER):
        lines.append(f"color{i} {ansi[k]}")
    for i, k in enumerate(ORDER):
        lines.append(f"color{i + 8} {bright[k]}")
    lines.append("")
    with open(out_path, "w") as f:
        f.write("\n".join(lines))


def gen_windows_terminal(pal, out_path):
    ansi = pal["ansi"]
    bright = pal["bright"]
    scheme = {
        "name": pal["name"],
        "background": pal["background"],
        "foreground": pal["foreground"],
        "cursorColor": pal["cursor"],
        "selectionBackground": pal["selection"],
        "black": ansi["black"],
        "red": ansi["red"],
        "green": ansi["green"],
        "yellow": ansi["yellow"],
        "blue": ansi["blue"],
        "purple": ansi["magenta"],
        "cyan": ansi["cyan"],
        "white": ansi["white"],
        "brightBlack": bright["black"],
        "brightRed": bright["red"],
        "brightGreen": bright["green"],
        "brightYellow": bright["yellow"],
        "brightBlue": bright["blue"],
        "brightPurple": bright["magenta"],
        "brightCyan": bright["cyan"],
        "brightWhite": bright["white"],
    }
    with open(out_path, "w") as f:
        json.dump(scheme, f, indent=2)
        f.write("\n")


def gen_hyper(pal, out_path):
    ansi = pal["ansi"]
    bright = pal["bright"]
    r, g, b = hex2tuple(pal["selection"])
    js = f"""// {pal['name']} theme for Hyper
exports.decorateConfig = (config) => {{
  return Object.assign({{}}, config, {{
    backgroundColor: '{pal['background']}',
    foregroundColor: '{pal['foreground']}',
    borderColor: '{pal['border']}',
    cursorColor: '{pal['cursor']}',
    cursorAccentColor: '{pal['background']}',
    selectionColor: 'rgba({r}, {g}, {b}, 0.5)',
    colors: {{
      black: '{ansi['black']}',
      red: '{ansi['red']}',
      green: '{ansi['green']}',
      yellow: '{ansi['yellow']}',
      blue: '{ansi['blue']}',
      magenta: '{ansi['magenta']}',
      cyan: '{ansi['cyan']}',
      white: '{ansi['white']}',
      lightBlack: '{bright['black']}',
      lightRed: '{bright['red']}',
      lightGreen: '{bright['green']}',
      lightYellow: '{bright['yellow']}',
      lightBlue: '{bright['blue']}',
      lightMagenta: '{bright['magenta']}',
      lightCyan: '{bright['cyan']}',
      lightWhite: '{bright['white']}',
    }},
  }});
}};
"""
    with open(out_path, "w") as f:
        f.write(js)


def gen_tabby(pal, out_path):
    ansi = pal["ansi"]
    bright = pal["bright"]
    colors_list = [ansi[k] for k in ORDER] + [bright[k] for k in ORDER]
    lines = [
        f"name: {pal['name']}",
        f"foreground: '{pal['foreground']}'",
        f"background: '{pal['background']}'",
        f"cursor: '{pal['cursor']}'",
        f"selection: '{pal['selection']}'",
        "colors:",
    ]
    for c in colors_list:
        lines.append(f"  - '{c}'")
    lines.append("")
    with open(out_path, "w") as f:
        f.write("\n".join(lines))


def gen_rio(pal, out_path):
    ansi = pal["ansi"]
    bright = pal["bright"]
    toml = f"""# {pal['name']} theme for Rio
[colors]
background = "{pal['background']}"
foreground = "{pal['foreground']}"
cursor = "{pal['cursor']}"
tabs = "{pal['secondary']}"
tabs-active = "{pal['accent']}"
selection-background = "{pal['selection']}"
selection-foreground = "{pal['selection_text']}"
black = "{ansi['black']}"
red = "{ansi['red']}"
green = "{ansi['green']}"
yellow = "{ansi['yellow']}"
blue = "{ansi['blue']}"
magenta = "{ansi['magenta']}"
cyan = "{ansi['cyan']}"
white = "{ansi['white']}"
dim-black = "{pal['secondary']}"
dim-red = "{ansi['red']}"
dim-green = "{ansi['green']}"
dim-yellow = "{ansi['yellow']}"
dim-blue = "{ansi['blue']}"
dim-magenta = "{ansi['magenta']}"
dim-cyan = "{ansi['cyan']}"
dim-white = "{pal['muted']}"
light-black = "{bright['black']}"
light-red = "{bright['red']}"
light-green = "{bright['green']}"
light-yellow = "{bright['yellow']}"
light-blue = "{bright['blue']}"
light-magenta = "{bright['magenta']}"
light-cyan = "{bright['cyan']}"
light-white = "{bright['white']}"
"""
    with open(out_path, "w") as f:
        f.write(toml)


# ---------- Editor formats ----------

def gen_vscode(pal, out_path):
    ansi = [pal["ansi"][k] for k in ORDER]
    btn_fg = "#ffffff" if pal["type"] == "dark" else pal["background"]
    if pal["type"] == "dark":
        btn_fg = pal["background"]
    else:
        btn_fg = "#faf4eb"

    theme = {
        "name": pal["name"],
        "type": pal["type"],
        "colors": {
            "editor.background": pal["background"],
            "editor.foreground": pal["foreground"],
            "editorCursor.foreground": pal["cursor"],
            "editor.selectionBackground": pal["selection"],
            "editorLineNumber.foreground": pal["muted"],
            "editorLineNumber.activeForeground": pal["accent"],
            "activityBar.background": pal["sidebar"],
            "activityBar.foreground": pal["foreground"],
            "activityBar.activeBorder": pal["accent"],
            "sideBar.background": pal["sidebar"],
            "sideBar.foreground": pal["foreground"],
            "sideBarTitle.foreground": pal["accent"],
            "statusBar.background": pal["secondary"],
            "statusBar.foreground": pal["foreground"],
            "titleBar.activeBackground": pal["background"],
            "titleBar.activeForeground": pal["foreground"],
            "panel.background": pal["background"],
            "terminal.background": pal["background"],
            "terminal.foreground": pal["foreground"],
            "terminal.ansiBlack": ansi[0],
            "terminal.ansiRed": ansi[1],
            "terminal.ansiGreen": ansi[2],
            "terminal.ansiYellow": ansi[3],
            "terminal.ansiBlue": ansi[4],
            "terminal.ansiMagenta": ansi[5],
            "terminal.ansiCyan": ansi[6],
            "terminal.ansiWhite": ansi[7],
            "button.background": pal["accent"],
            "button.foreground": btn_fg,
            "input.background": pal["secondary"],
            "input.border": pal["border"],
            "focusBorder": pal["accent"],
            "list.activeSelectionBackground": pal["secondary"],
            "list.hoverBackground": pal["card"],
            "badge.background": pal["accent"],
            "badge.foreground": btn_fg,
        },
        "tokenColors": [
            {
                "scope": ["comment", "punctuation.definition.comment"],
                "settings": {"foreground": pal["muted"], "fontStyle": "italic"},
            },
            {
                "scope": ["keyword", "storage.type", "storage.modifier"],
                "settings": {"foreground": pal["accent"]},
            },
            {
                "scope": ["string", "string.quoted"],
                "settings": {"foreground": pal["success"]},
            },
            {
                "scope": ["constant.numeric"],
                "settings": {"foreground": pal["destructive"]},
            },
            {
                "scope": ["entity.name.function", "support.function"],
                "settings": {"foreground": pal["blue"]},
            },
            {
                "scope": ["variable", "variable.other"],
                "settings": {"foreground": pal["foreground"]},
            },
            {
                "scope": ["entity.name.type", "support.type", "support.class"],
                "settings": {"foreground": pal["magenta"]},
            },
            {
                "scope": ["keyword.operator"],
                "settings": {"foreground": pal["cyan"]},
            },
        ],
    }
    with open(out_path, "w") as f:
        json.dump(theme, f, indent=2)
        f.write("\n")


# ---------- App formats ----------

def gen_slack(pal, out_path):
    # Slack theme string: column_bg,menu_bg,active_item,active_item_text,hover_item,mention_badge,text_color,active_presence,mention_badge_text
    active_item_txt = pal["background"] if pal["type"] == "dark" else "#faf4eb"
    badge_txt = pal["destructive"] if pal["type"] == "dark" else "#faf4eb"
    s = ",".join([
        pal["background"],
        pal["secondary"],
        pal["accent"],
        active_item_txt,
        pal["card"],
        pal["foreground"],
        pal["foreground"],
        pal["success"],
        badge_txt,
    ])
    with open(out_path, "w") as f:
        f.write(s + "\n")


def gen_discord(pal, out_path):
    class_name = f".theme-{pal['type']}"
    css = f"""/* {pal['name']} theme for Discord (BetterDiscord) */
{class_name} {{
  --background-primary: {pal['background']};
  --background-secondary: {pal['secondary']};
  --background-secondary-alt: {pal['card']};
  --background-tertiary: {pal['sidebar']};
  --background-accent: {pal['accent']};
  --text-normal: {pal['foreground']};
  --text-muted: {pal['muted']};
  --interactive-normal: {pal['muted']};
  --interactive-hover: {pal['foreground']};
  --interactive-active: {pal['accent']};
  --brand-experiment: {pal['accent']};
  --status-positive: {pal['success']};
  --status-danger: {pal['destructive']};
}}
"""
    with open(out_path, "w") as f:
        f.write(css)


def gen_tmux(pal, out_path):
    conf = f"""# {pal['name']} theme for tmux
set -g status-style "bg={pal['secondary']},fg={pal['foreground']}"
set -g status-left-style "bg={pal['accent']},fg={pal['background']},bold"
set -g status-right-style "bg={pal['secondary']},fg={pal['muted']}"
set -g pane-border-style "fg={pal['border']}"
set -g pane-active-border-style "fg={pal['accent']}"
set -g message-style "bg={pal['accent']},fg={pal['background']}"
set -g mode-style "bg={pal['accent']},fg={pal['background']}"
setw -g window-status-style "fg={pal['muted']}"
setw -g window-status-current-style "fg={pal['accent']},bold"
"""
    with open(out_path, "w") as f:
        f.write(conf)


def gen_zsh(pal, out_path):
    conf = f"""# {pal['name']} theme for zsh prompt
PROMPT='%F{{{pal['accent']}}}%n%f@%F{{{pal['magenta']}}}%m%f %F{{{pal['muted']}}}%~%f %F{{{pal['accent']}}}❯%f '
# success/fail indicator colors
ZSH_HIGHLIGHT_STYLES[command]='fg={pal['success']}'
ZSH_HIGHLIGHT_STYLES[unknown-token]='fg={pal['destructive']}'
"""
    with open(out_path, "w") as f:
        f.write(conf)


def generate_dark_variant(base_dir):
    term = os.path.join(base_dir, "terminal")
    edit = os.path.join(base_dir, "editor")
    app = os.path.join(base_dir, "app")
    for d in (term, edit, app):
        ensure(d)

    gen_warp(DARK_PALETTE, os.path.join(term, "halloween.yaml"))
    gen_itermcolors(DARK_PALETTE, os.path.join(term, "halloween.itermcolors"))
    gen_ghostty(DARK_PALETTE, os.path.join(term, "halloween.ghostty"))
    gen_alacritty(DARK_PALETTE, os.path.join(term, "halloween.alacritty.toml"))
    gen_wezterm(DARK_PALETTE, os.path.join(term, "halloween.wezterm.toml"))
    gen_kitty(DARK_PALETTE, os.path.join(term, "halloween.kitty.conf"))
    gen_windows_terminal(DARK_PALETTE, os.path.join(term, "halloween.windows-terminal.json"))
    gen_hyper(DARK_PALETTE, os.path.join(term, "halloween.hyper.js"))
    gen_tabby(DARK_PALETTE, os.path.join(term, "halloween.tabby.yaml"))
    gen_rio(DARK_PALETTE, os.path.join(term, "halloween.rio.toml"))

    gen_vscode(DARK_PALETTE, os.path.join(edit, "halloween-vscode.json"))

    gen_slack(DARK_PALETTE, os.path.join(app, "halloween-slack.txt"))
    gen_discord(DARK_PALETTE, os.path.join(app, "halloween-discord.css"))
    gen_tmux(DARK_PALETTE, os.path.join(app, "halloween.tmux.conf"))
    gen_zsh(DARK_PALETTE, os.path.join(app, "halloween.zsh"))


def generate_light_variant(base_dir):
    light_dir = os.path.join(base_dir, "light")
    ensure(light_dir)

    gen_warp(LIGHT_PALETTE, os.path.join(light_dir, "halloween-light.yaml"))
    gen_itermcolors(LIGHT_PALETTE, os.path.join(light_dir, "halloween-light.itermcolors"))
    gen_ghostty(LIGHT_PALETTE, os.path.join(light_dir, "halloween-light.ghostty"))
    gen_alacritty(LIGHT_PALETTE, os.path.join(light_dir, "halloween-light.alacritty.toml"))
    gen_wezterm(LIGHT_PALETTE, os.path.join(light_dir, "halloween-light.wezterm.toml"))
    gen_kitty(LIGHT_PALETTE, os.path.join(light_dir, "halloween-light.kitty.conf"))
    gen_windows_terminal(LIGHT_PALETTE, os.path.join(light_dir, "halloween-light.windows-terminal.json"))
    gen_hyper(LIGHT_PALETTE, os.path.join(light_dir, "halloween-light.hyper.js"))
    gen_tabby(LIGHT_PALETTE, os.path.join(light_dir, "halloween-light.tabby.yaml"))
    gen_rio(LIGHT_PALETTE, os.path.join(light_dir, "halloween-light.rio.toml"))

    gen_vscode(LIGHT_PALETTE, os.path.join(light_dir, "halloween-light-vscode.json"))

    gen_slack(LIGHT_PALETTE, os.path.join(light_dir, "halloween-light-slack.txt"))
    gen_discord(LIGHT_PALETTE, os.path.join(light_dir, "halloween-light-discord.css"))
    gen_tmux(LIGHT_PALETTE, os.path.join(light_dir, "halloween-light.tmux.conf"))
    gen_zsh(LIGHT_PALETTE, os.path.join(light_dir, "halloween-light.zsh"))


def main():
    ap = argparse.ArgumentParser(description="Generate Halloween theme files.")
    ap.add_argument("--out", default="themes", help="Output directory (default: themes)")
    args = ap.parse_args()
    base = args.out
    ensure(base)

    generate_dark_variant(base)
    generate_light_variant(base)

    # Sync canonical Warp YAML to root if generating to default themes/
    if os.path.abspath(base) == os.path.abspath("themes"):
        gen_warp(DARK_PALETTE, "halloween.yaml")

    print(f"Generated theme files under {base}:")
    for root, _, files in os.walk(base):
        for fn in sorted(files):
            rel = os.path.relpath(os.path.join(root, fn), base)
            print(" ", rel)


if __name__ == "__main__":
    main()
