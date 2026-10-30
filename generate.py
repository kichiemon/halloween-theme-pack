#!/usr/bin/env python3
"""Generate Halloween theme files for multiple apps from one palette.

Usage:
    python3 generate.py            # writes to ./themes/
    python3 generate.py --out DIR  # custom output dir
    python3 generate.py apply      # auto-detect and apply to installed apps
"""
import argparse
import json
import os
import shutil
import sys
import urllib.parse

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

# Variant: Halloween OLED / Pure Void (#000000 background)
OLED_PALETTE = {
    "id": "halloween-oled",
    "name": "Halloween OLED",
    "type": "dark",
    "details": "darker",
    "background": "#000000",
    "foreground": "#f4e7d3",
    "card": "#12091c",
    "secondary": "#1a0a2a",
    "muted": "#b8a9d9",
    "border": "#2c1845",
    "sidebar": "#08040d",
    "accent": "#ff6b35",
    "success": "#39ff14",
    "destructive": "#ff4d6d",
    "cursor": "#ff6b35",
    "selection": "#2c1845",
    "selection_text": "#f4e7d3",
    "blue": "#6b8cff",
    "magenta": "#c77dff",
    "cyan": "#5ffbf1",
    "yellow": "#ffb347",
    "ansi": {
        "black": "#1a0a2a",
        "red": "#ff4d6d",
        "green": "#39ff14",
        "yellow": "#ffb347",
        "blue": "#6b8cff",
        "magenta": "#c77dff",
        "cyan": "#5ffbf1",
        "white": "#f4e7d3",
    },
    "bright": {
        "black": "#3b1e5c",
        "red": "#ff7a95",
        "green": "#7fff6b",
        "yellow": "#ffd28a",
        "blue": "#9db3ff",
        "magenta": "#ddb3ff",
        "cyan": "#9dfff7",
        "white": "#ffffff",
    },
}

# Variant: Halloween Pastel / Spooky Kawaii
PASTEL_PALETTE = {
    "id": "halloween-pastel",
    "name": "Halloween Pastel",
    "type": "light",
    "details": "lighter",
    "background": "#faf5fc",
    "foreground": "#3c2a4d",
    "card": "#f2e8f7",
    "secondary": "#e9daf2",
    "muted": "#756388",
    "border": "#dcc9e8",
    "sidebar": "#f5ecfa",
    "accent": "#bf4904",
    "success": "#1b772d",
    "destructive": "#b81438",
    "cursor": "#bf4904",
    "selection": "#e5d0f0",
    "selection_text": "#3c2a4d",
    "blue": "#2b4acb",
    "magenta": "#8b3da8",
    "cyan": "#0e7490",
    "yellow": "#9e6000",
    "ansi": {
        "black": "#3c2a4d",
        "red": "#b81438",
        "green": "#1b772d",
        "yellow": "#9e6000",
        "blue": "#2b4acb",
        "magenta": "#8b3da8",
        "cyan": "#0e7490",
        "white": "#dcc9e8",
    },
    "bright": {
        "black": "#674f78",
        "red": "#cf2248",
        "green": "#228b37",
        "yellow": "#b56f00",
        "blue": "#3b5bdb",
        "magenta": "#a855f7",
        "cyan": "#0284c7",
        "white": "#3c2a4d",
    },
}

# Variant: Halloween Cyberpunk (Neon Pumpkin & Plasma)
CYBERPUNK_PALETTE = {
    "id": "halloween-cyberpunk",
    "name": "Halloween Cyberpunk",
    "type": "dark",
    "details": "darker",
    "background": "#0d0221",
    "foreground": "#fcf7ff",
    "card": "#19053b",
    "secondary": "#240046",
    "muted": "#9d79bc",
    "border": "#5a189a",
    "sidebar": "#090014",
    "accent": "#ff6d00",
    "success": "#00f5d4",
    "destructive": "#ff0054",
    "cursor": "#ff6d00",
    "selection": "#3c096c",
    "selection_text": "#fcf7ff",
    "blue": "#7000ff",
    "magenta": "#c77dff",
    "cyan": "#00f5d4",
    "yellow": "#ffee32",
    "ansi": {
        "black": "#240046",
        "red": "#ff0054",
        "green": "#00f5d4",
        "yellow": "#ffee32",
        "blue": "#7000ff",
        "magenta": "#c77dff",
        "cyan": "#00f5d4",
        "white": "#fcf7ff",
    },
    "bright": {
        "black": "#5a189a",
        "red": "#ff3377",
        "green": "#5cffee",
        "yellow": "#fff275",
        "blue": "#9d4edd",
        "magenta": "#e0aaff",
        "cyan": "#70fff3",
        "white": "#ffffff",
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


# ---------- New Terminal / CLI formats ----------

def gen_k9s(pal, out_path):
    bg = pal["background"]
    fg = pal["foreground"]
    accent = pal["accent"]
    success = pal["success"]
    destructive = pal["destructive"]
    card = pal["card"]
    border = pal["border"]
    muted = pal["muted"]
    yellow = pal["yellow"]
    cyan = pal["cyan"]
    magenta = pal["magenta"]
    yaml_str = f"""# {pal['name']} theme for K9s
k9s:
  body:
    fgColor: "{fg}"
    bgColor: "{bg}"
    logoColor: "{accent}"
  prompt:
    fgColor: "{fg}"
    bgColor: "{card}"
    suggestColor: "{yellow}"
  info:
    fgColor: "{muted}"
    sectionColor: "{accent}"
  dialog:
    fgColor: "{fg}"
    bgColor: "{card}"
    buttonFgColor: "{bg}"
    buttonBgColor: "{accent}"
    buttonActiveFgColor: "{fg}"
    buttonActiveBgColor: "{destructive}"
    labelFgColor: "{yellow}"
    fieldFgColor: "{fg}"
  frame:
    border:
      fgColor: "{border}"
      focusColor: "{accent}"
    menu:
      fgColor: "{fg}"
      keyColor: "{accent}"
      numKeyColor: "{magenta}"
    crumbs:
      fgColor: "{bg}"
      bgColor: "{accent}"
      activeColor: "{success}"
    status:
      completedColor: "{success}"
      errorColor: "{destructive}"
      highlightColor: "{accent}"
    title:
      fgColor: "{accent}"
      bgColor: "{card}"
      highlightColor: "{success}"
      counterColor: "{magenta}"
  views:
    table:
      fgColor: "{fg}"
      bgColor: "{bg}"
      cursorFgColor: "{bg}"
      cursorBgColor: "{accent}"
      markColor: "{yellow}"
      header:
        fgColor: "{accent}"
        bgColor: "{card}"
        sorterColor: "{cyan}"
    xray:
      fgColor: "{fg}"
      bgColor: "{bg}"
      cursorColor: "{accent}"
    yaml:
      keyColor: "{magenta}"
      colonColor: "{border}"
      valueColor: "{fg}"
    logs:
      fgColor: "{fg}"
      bgColor: "{bg}"
      indicator:
        fgColor: "{accent}"
        bgColor: "{card}"
"""
    with open(out_path, "w") as f:
        f.write(yaml_str)


def gen_base16(pal, out_path):
    yaml_str = f"""# {pal['name']} Base16 / Tinted Theming scheme
scheme: "{pal['name']}"
author: "kichiemon"
system: "base16"
base00: "{pal['background']}"
base01: "{pal['card']}"
base02: "{pal['secondary']}"
base03: "{pal['muted']}"
base04: "{pal['border']}"
base05: "{pal['foreground']}"
base06: "{pal['bright']['white']}"
base07: "{pal['foreground']}"
base08: "{pal['destructive']}"
base09: "{pal['accent']}"
base0A: "{pal['yellow']}"
base0B: "{pal['success']}"
base0C: "{pal['cyan']}"
base0D: "{pal['blue']}"
base0E: "{pal['magenta']}"
base0F: "{pal['ansi']['red']}"
"""
    with open(out_path, "w") as f:
        f.write(yaml_str)


def gen_yazi(pal, out_path):
    toml = f"""# {pal['name']} theme for Yazi
[mgr]
cwd = {{ fg = "{pal['cyan']}" }}
hovered = {{ fg = "{pal['background']}", bg = "{pal['accent']}" }}
preview_hovered = {{ underline = true }}
find_keyword = {{ fg = "{pal['yellow']}", bold = true }}
marker_copied = {{ fg = "{pal['success']}", bg = "{pal['card']}" }}
marker_cut = {{ fg = "{pal['destructive']}", bg = "{pal['card']}" }}
marker_selected = {{ fg = "{pal['accent']}", bg = "{pal['card']}" }}
tab_active = {{ fg = "{pal['background']}", bg = "{pal['accent']}" }}
tab_inactive = {{ fg = "{pal['muted']}", bg = "{pal['card']}" }}
border_style = {{ fg = "{pal['border']}" }}

[status]
separator_open = ""
separator_close = ""
progress_label = {{ fg = "{pal['foreground']}", bold = true }}
progress_normal = {{ fg = "{pal['blue']}", bg = "{pal['card']}" }}
progress_error = {{ fg = "{pal['destructive']}", bg = "{pal['card']}" }}

[select]
border = {{ fg = "{pal['accent']}" }}
active = {{ fg = "{pal['yellow']}" }}
inactive = {{ fg = "{pal['foreground']}" }}

[input]
border = {{ fg = "{pal['accent']}" }}
title = {{ fg = "{pal['foreground']}" }}
value = {{ fg = "{pal['foreground']}" }}
selected = {{ bg = "{pal['selection']}" }}

[completion]
border = {{ fg = "{pal['accent']}" }}
active = {{ fg = "{pal['background']}", bg = "{pal['accent']}" }}
inactive = {{ fg = "{pal['foreground']}" }}
"""
    with open(out_path, "w") as f:
        f.write(toml)


def gen_glamour(pal, out_path):
    style = {
        "document": {"margin": 2},
        "block_quote": {"indent": 1, "indent_token": "│ ", "color": pal["muted"]},
        "paragraph": {},
        "list": {"level_indent": 2},
        "heading": {"color": pal["accent"], "bold": True},
        "h1": {"color": pal["accent"], "bold": True},
        "h2": {"color": pal["yellow"], "bold": True},
        "h3": {"color": pal["magenta"], "bold": True},
        "text": {"color": pal["foreground"]},
        "strong": {"bold": True, "color": pal["yellow"]},
        "emphasis": {"italic": True, "color": pal["muted"]},
        "item": {"block_prefix": "• ", "color": pal["accent"]},
        "link": {"color": pal["cyan"], "underline": True},
        "code": {"color": pal["success"], "background_color": pal["card"]},
        "code_block": {"color": pal["foreground"], "margin": 1},
    }
    with open(out_path, "w") as f:
        json.dump(style, f, indent=2)
        f.write("\n")


def gen_pywal(pal, out_path):
    ansi = [pal["ansi"][k] for k in ORDER]
    bright = [pal["bright"][k] for k in ORDER]
    wal_colors = {}
    for i, c in enumerate(ansi):
        wal_colors[f"color{i}"] = c
    for i, c in enumerate(bright):
        wal_colors[f"color{i+8}"] = c
    data = {
        "wallpaper": "None",
        "alpha": "100",
        "special": {
            "background": pal["background"],
            "foreground": pal["foreground"],
            "cursor": pal["cursor"],
        },
        "colors": wal_colors,
    }
    with open(out_path, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def gen_btop(pal, out_path):
    content = f"""# {pal['name']} theme for btop++
theme[main_bg]="{pal['background']}"
theme[main_fg]="{pal['foreground']}"
theme[title]="{pal['accent']}"
theme[hi_fg]="{pal['accent']}"
theme[selected_bg]="{pal['selection']}"
theme[selected_fg]="{pal['foreground']}"
theme[inactive_fg]="{pal['muted']}"
theme[proc_misc]="{pal['magenta']}"
theme[cpu_box]="{pal['border']}"
theme[mem_box]="{pal['border']}"
theme[net_box]="{pal['border']}"
theme[proc_box]="{pal['border']}"
theme[div_line]="{pal['border']}"
theme[temp_start]="{pal['success']}"
theme[temp_mid]="{pal['yellow']}"
theme[temp_end]="{pal['destructive']}"
theme[cpu_start]="{pal['success']}"
theme[cpu_mid]="{pal['yellow']}"
theme[cpu_end]="{pal['destructive']}"
theme[free_start]="{pal['success']}"
theme[free_mid]="{pal['yellow']}"
theme[free_end]="{pal['destructive']}"
theme[cached_start]="{pal['blue']}"
theme[cached_mid]="{pal['magenta']}"
theme[cached_end]="{pal['destructive']}"
theme[available_start]="{pal['success']}"
theme[available_mid]="{pal['yellow']}"
theme[available_end]="{pal['destructive']}"
theme[used_start]="{pal['success']}"
theme[used_mid]="{pal['yellow']}"
theme[used_end]="{pal['destructive']}"
theme[download_start]="{pal['blue']}"
theme[download_mid]="{pal['cyan']}"
theme[download_end]="{pal['success']}"
theme[upload_start]="{pal['magenta']}"
theme[upload_mid]="{pal['accent']}"
theme[upload_end]="{pal['destructive']}"
"""
    with open(out_path, "w") as f:
        f.write(content)


# ---------- Editor formats ----------

def gen_vscode(pal, out_path):
    ansi = [pal["ansi"][k] for k in ORDER]
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


def gen_obsidian(pal, css_out_path, manifest_out_path):
    cls = f".theme-{pal['type']}"
    css = f"""/* {pal['name']} theme for Obsidian */
{cls} {{
  --background-primary: {pal['background']};
  --background-primary-alt: {pal['sidebar']};
  --background-secondary: {pal['card']};
  --background-secondary-alt: {pal['secondary']};
  --background-modifier-border: {pal['border']};
  --text-normal: {pal['foreground']};
  --text-muted: {pal['muted']};
  --text-faint: {pal['muted']};
  --text-accent: {pal['accent']};
  --text-accent-hover: {pal['yellow']};
  --interactive-accent: {pal['accent']};
  --interactive-accent-hover: {pal['yellow']};
  --interactive-normal: {pal['card']};
  --interactive-hover: {pal['secondary']};
  --scrollbar-bg: {pal['background']};
  --scrollbar-thumb-bg: {pal['border']};
}}
"""
    with open(css_out_path, "w") as f:
        f.write(css)

    manifest = {
        "name": pal["name"],
        "version": "1.0.0",
        "minAppVersion": "1.0.0",
        "author": "kichiemon",
    }
    with open(manifest_out_path, "w") as f:
        json.dump(manifest, f, indent=2)
        f.write("\n")


def gen_xcode(pal, out_path):
    def cstr(hexv):
        r, g, b = hex2rgb(hexv)
        return f"{r:.6f} {g:.6f} {b:.6f} 1"

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <!-- Hex Background: {pal['background']} -->
  <!-- Hex Foreground: {pal['foreground']} -->
  <!-- Hex Accent: {pal['accent']} -->
  <!-- Hex Success: {pal['success']} -->
  <!-- Hex Destructive: {pal['destructive']} -->
  <!-- Hex Selection: {pal['selection']} -->
  <key>DVTSourceTextBackground</key>
  <string>{cstr(pal['background'])}</string>
  <key>DVTSourceTextBlockDimBackground</key>
  <string>{cstr(pal['secondary'])}</string>
  <key>DVTSourceTextForeground</key>
  <string>{cstr(pal['foreground'])}</string>
  <key>DVTSourceTextInsertionPointColor</key>
  <string>{cstr(pal['cursor'])}</string>
  <key>DVTSourceTextSelectionColor</key>
  <string>{cstr(pal['selection'])}</string>
  <key>DVTSourceTextSyntaxColors</key>
  <dict>
    <key>xcode.syntax.attribute</key>
    <string>{cstr(pal['cyan'])}</string>
    <key>xcode.syntax.character</key>
    <string>{cstr(pal['yellow'])}</string>
    <key>xcode.syntax.comment</key>
    <string>{cstr(pal['muted'])}</string>
    <key>xcode.syntax.comment.doc</key>
    <string>{cstr(pal['muted'])}</string>
    <key>xcode.syntax.keyword</key>
    <string>{cstr(pal['accent'])}</string>
    <key>xcode.syntax.number</key>
    <string>{cstr(pal['destructive'])}</string>
    <key>xcode.syntax.plain</key>
    <string>{cstr(pal['foreground'])}</string>
    <key>xcode.syntax.string</key>
    <string>{cstr(pal['success'])}</string>
    <key>xcode.syntax.type</key>
    <string>{cstr(pal['magenta'])}</string>
    <key>xcode.syntax.url</key>
    <string>{cstr(pal['blue'])}</string>
  </dict>
</dict>
</plist>
"""
    with open(out_path, "w") as f:
        f.write(xml)


# ---------- App formats ----------

def gen_slack(pal, out_path):
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


def gen_raycast(pal, out_path):
    theme_data = {
        "version": "1",
        "name": pal["name"],
        "appearance": pal["type"],
        "colors": {
            "background": pal["background"],
            "backgroundSecondary": pal["card"],
            "text": pal["foreground"],
            "textMuted": pal["muted"],
            "selection": pal["selection"],
            "accent": pal["accent"],
            "red": pal["destructive"],
            "orange": pal["accent"],
            "yellow": pal["yellow"],
            "green": pal["success"],
            "blue": pal["blue"],
            "purple": pal["magenta"],
            "magenta": pal["magenta"],
            "cyan": pal["cyan"],
        },
    }
    encoded = urllib.parse.quote(json.dumps(theme_data))
    theme_data["shareUrl"] = f"raycast://theme?data={encoded}"
    with open(out_path, "w") as f:
        json.dump(theme_data, f, indent=2)
        f.write("\n")


def gen_lazydocker(pal, out_path):
    yaml_str = f"""# {pal['name']} theme for Lazydocker
gui:
  theme:
    activeBorderColor:
      - "{pal['accent']}"
      - bold
    inactiveBorderColor:
      - "{pal['border']}"
    selectedLineBgColor:
      - "{pal['secondary']}"
    selectedRangeBgColor:
      - "{pal['selection']}"
    optionsTextColor:
      - "{pal['blue']}"
"""
    with open(out_path, "w") as f:
        f.write(yaml_str)


def gen_tokens(pal, out_path):
    data = {
        "color": {
            "background": {"$value": pal["background"], "$type": "color", "$description": "Canvas background"},
            "foreground": {"$value": pal["foreground"], "$type": "color", "$description": "Primary readable text"},
            "accent": {"$value": pal["accent"], "$type": "color", "$description": "Pumpkin orange brand accent"},
            "success": {"$value": pal["success"], "$type": "color", "$description": "Slime green success indicator"},
            "destructive": {"$value": pal["destructive"], "$type": "color", "$description": "Blood red error and warning"},
            "secondary": {"$value": pal["secondary"], "$type": "color"},
            "card": {"$value": pal["card"], "$type": "color"},
            "muted": {"$value": pal["muted"], "$type": "color"},
            "border": {"$value": pal["border"], "$type": "color"},
            "sidebar": {"$value": pal["sidebar"], "$type": "color"},
            "blue": {"$value": pal["blue"], "$type": "color"},
            "magenta": {"$value": pal["magenta"], "$type": "color"},
            "cyan": {"$value": pal["cyan"], "$type": "color"},
            "yellow": {"$value": pal["yellow"], "$type": "color"},
        }
    }
    with open(out_path, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def gen_fish(pal, out_path):
    script = f"""# {pal['name']} theme for fish shell
set -g fish_color_normal '{pal['foreground']}'
set -g fish_color_command '{pal['success']}'
set -g fish_color_keyword '{pal['magenta']}'
set -g fish_color_quote '{pal['yellow']}'
set -g fish_color_redirection '{pal['accent']}'
set -g fish_color_end '{pal['cyan']}'
set -g fish_color_error '{pal['destructive']}'
set -g fish_color_param '{pal['foreground']}'
set -g fish_color_comment '{pal['muted']}'
set -g fish_color_selection --background='{pal['selection']}'
set -g fish_color_search_match --background='{pal['secondary']}'
set -g fish_color_operator '{pal['cyan']}'
set -g fish_color_escape '{pal['destructive']}'
set -g fish_color_autosuggestion '{pal['muted']}'
set -g fish_pager_color_prefix '{pal['accent']}' --bold
set -g fish_pager_color_completion '{pal['foreground']}'
set -g fish_pager_color_description '{pal['muted']}'
set -g fish_pager_color_progress '{pal['cyan']}'
"""
    with open(out_path, "w") as f:
        f.write(script)


def gen_starship(pal, out_path):
    palette_id = pal["id"]
    toml = f"""# {pal['name']} palette for Starship
palette = "{palette_id}"

[palettes.{palette_id}]
background = "{pal['background']}"
foreground = "{pal['foreground']}"
accent = "{pal['accent']}"
success = "{pal['success']}"
destructive = "{pal['destructive']}"
card = "{pal['card']}"
secondary = "{pal['secondary']}"
muted = "{pal['muted']}"
border = "{pal['border']}"
blue = "{pal['blue']}"
magenta = "{pal['magenta']}"
cyan = "{pal['cyan']}"
yellow = "{pal['yellow']}"
"""
    with open(out_path, "w") as f:
        f.write(toml)


def gen_oh_my_posh(pal, out_path):
    theme = {
        "$schema": "https://raw.githubusercontent.com/JanDeDobbeleer/oh-my-posh/main/themes/schema.json",
        "version": 2,
        "final_space": True,
        "palette": {
            "background": pal["background"],
            "foreground": pal["foreground"],
            "accent": pal["accent"],
            "success": pal["success"],
            "destructive": pal["destructive"],
            "secondary": pal["secondary"],
            "card": pal["card"],
            "muted": pal["muted"],
            "blue": pal["blue"],
            "magenta": pal["magenta"],
            "cyan": pal["cyan"],
            "yellow": pal["yellow"],
        },
        "blocks": [
            {
                "type": "prompt",
                "alignment": "left",
                "segments": [
                    {
                        "type": "path",
                        "style": "powerline",
                        "powerline_symbol": "",
                        "foreground": "p:background",
                        "background": "p:accent",
                        "properties": {"style": "folder"},
                    },
                    {
                        "type": "git",
                        "style": "powerline",
                        "powerline_symbol": "",
                        "foreground": "p:background",
                        "background": "p:success",
                        "properties": {"branch_icon": " "},
                    },
                    {
                        "type": "text",
                        "style": "plain",
                        "foreground": "p:accent",
                        "properties": {"text": " ❯"},
                    },
                ],
            }
        ],
    }
    with open(out_path, "w") as f:
        json.dump(theme, f, indent=2)
        f.write("\n")


def gen_tig(pal, out_path):
    content = f"""# {pal['name']} theme for tig
color default "{pal['foreground']}" "{pal['background']}" normal
color cursor "{pal['background']}" "{pal['accent']}" bold
color status.untracked "{pal['destructive']}" default
color status.modified "{pal['yellow']}" default
color diff-header "{pal['accent']}" default bold
color diff-index "{pal['cyan']}" default
color diff-chunk "{pal['magenta']}" default
color diff-add "{pal['success']}" default
color diff-del "{pal['destructive']}" default
color line-number "{pal['muted']}" default
color title-blur "{pal['muted']}" "{pal['card']}"
color title-focus "{pal['accent']}" "{pal['card']}" bold
"""
    with open(out_path, "w") as f:
        f.write(content)


def gen_gitui(pal, out_path):
    content = f"""# {pal['name']} theme for gitui
selected_tab = "{pal['accent']}"
command_fg = "{pal['foreground']}"
selection_bg = "{pal['selection']}"
selection_fg = "{pal['foreground']}"
cmdbar_bg = "{pal['secondary']}"
cmdbar_extra_lines_bg = "{pal['card']}"
disabled_fg = "{pal['muted']}"
diff_line_add = "{pal['success']}"
diff_line_delete = "{pal['destructive']}"
diff_file_added = "{pal['success']}"
diff_file_removed = "{pal['destructive']}"
diff_file_moved = "{pal['blue']}"
diff_file_modified = "{pal['yellow']}"
commit_hash = "{pal['magenta']}"
commit_time = "{pal['cyan']}"
commit_author = "{pal['blue']}"
danger_fg = "{pal['destructive']}"
push_gauge_bg = "{pal['blue']}"
push_gauge_fg = "{pal['background']}"
tag_fg = "{pal['yellow']}"
branch_fg = "{pal['success']}"
"""
    with open(out_path, "w") as f:
        f.write(content)


# ---------- Variant Generators ----------

def generate_dark_variant(base_dir):
    term = os.path.join(base_dir, "terminal")
    edit = os.path.join(base_dir, "editor")
    app = os.path.join(base_dir, "app")
    for d in (term, edit, app):
        ensure(d)

    # Existing terminal formats
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

    # New terminal / CLI formats
    gen_k9s(DARK_PALETTE, os.path.join(term, "halloween.k9s.yaml"))
    gen_base16(DARK_PALETTE, os.path.join(term, "halloween.base16.yaml"))
    gen_yazi(DARK_PALETTE, os.path.join(term, "halloween.yazi.toml"))
    gen_glamour(DARK_PALETTE, os.path.join(term, "halloween.glamour.json"))
    gen_pywal(DARK_PALETTE, os.path.join(term, "halloween.colors-wal.json"))
    gen_btop(DARK_PALETTE, os.path.join(term, "halloween.btop.theme"))

    # Editor formats
    gen_vscode(DARK_PALETTE, os.path.join(edit, "halloween-vscode.json"))
    gen_obsidian(DARK_PALETTE, os.path.join(edit, "halloween.obsidian.css"), os.path.join(edit, "halloween-obsidian-manifest.json"))
    gen_xcode(DARK_PALETTE, os.path.join(edit, "halloween.xccolortheme"))

    # Existing app formats
    gen_slack(DARK_PALETTE, os.path.join(app, "halloween-slack.txt"))
    gen_discord(DARK_PALETTE, os.path.join(app, "halloween-discord.css"))
    gen_tmux(DARK_PALETTE, os.path.join(app, "halloween.tmux.conf"))
    gen_zsh(DARK_PALETTE, os.path.join(app, "halloween.zsh"))

    # New app formats
    gen_raycast(DARK_PALETTE, os.path.join(app, "halloween.raycast.json"))
    gen_lazydocker(DARK_PALETTE, os.path.join(app, "halloween.lazydocker.yaml"))
    gen_tokens(DARK_PALETTE, os.path.join(app, "halloween.tokens.json"))
    gen_fish(DARK_PALETTE, os.path.join(app, "halloween.fish"))
    gen_starship(DARK_PALETTE, os.path.join(app, "halloween.starship.toml"))
    gen_oh_my_posh(DARK_PALETTE, os.path.join(app, "halloween.omp.json"))
    gen_tig(DARK_PALETTE, os.path.join(app, "halloween.tigrc"))
    gen_gitui(DARK_PALETTE, os.path.join(app, "halloween.gitui.toml"))


def generate_light_variant(base_dir):
    light_dir = os.path.join(base_dir, "light")
    ensure(light_dir)

    # Existing formats
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

    # New terminal / CLI formats
    gen_k9s(LIGHT_PALETTE, os.path.join(light_dir, "halloween-light.k9s.yaml"))
    gen_base16(LIGHT_PALETTE, os.path.join(light_dir, "halloween-light.base16.yaml"))
    gen_yazi(LIGHT_PALETTE, os.path.join(light_dir, "halloween-light.yazi.toml"))
    gen_glamour(LIGHT_PALETTE, os.path.join(light_dir, "halloween-light.glamour.json"))
    gen_pywal(LIGHT_PALETTE, os.path.join(light_dir, "halloween-light.colors-wal.json"))
    gen_btop(LIGHT_PALETTE, os.path.join(light_dir, "halloween-light.btop.theme"))

    # New editor formats
    gen_obsidian(LIGHT_PALETTE, os.path.join(light_dir, "halloween-light.obsidian.css"), os.path.join(light_dir, "halloween-light-obsidian-manifest.json"))
    gen_xcode(LIGHT_PALETTE, os.path.join(light_dir, "halloween-light.xccolortheme"))

    # New app formats
    gen_raycast(LIGHT_PALETTE, os.path.join(light_dir, "halloween-light.raycast.json"))
    gen_lazydocker(LIGHT_PALETTE, os.path.join(light_dir, "halloween-light.lazydocker.yaml"))
    gen_tokens(LIGHT_PALETTE, os.path.join(light_dir, "halloween-light.tokens.json"))
    gen_fish(LIGHT_PALETTE, os.path.join(light_dir, "halloween-light.fish"))
    gen_starship(LIGHT_PALETTE, os.path.join(light_dir, "halloween-light.starship.toml"))
    gen_oh_my_posh(LIGHT_PALETTE, os.path.join(light_dir, "halloween-light.omp.json"))
    gen_tig(LIGHT_PALETTE, os.path.join(light_dir, "halloween-light.tigrc"))
    gen_gitui(LIGHT_PALETTE, os.path.join(light_dir, "halloween-light.gitui.toml"))


def generate_extra_variant(pal, out_dir):
    ensure(out_dir)
    pfx = pal["id"]
    gen_warp(pal, os.path.join(out_dir, f"{pfx}.yaml"))
    gen_itermcolors(pal, os.path.join(out_dir, f"{pfx}.itermcolors"))
    gen_ghostty(pal, os.path.join(out_dir, f"{pfx}.ghostty"))
    gen_alacritty(pal, os.path.join(out_dir, f"{pfx}.alacritty.toml"))
    gen_wezterm(pal, os.path.join(out_dir, f"{pfx}.wezterm.toml"))
    gen_kitty(pal, os.path.join(out_dir, f"{pfx}.kitty.conf"))
    gen_windows_terminal(pal, os.path.join(out_dir, f"{pfx}.windows-terminal.json"))
    gen_vscode(pal, os.path.join(out_dir, f"{pfx}-vscode.json"))
    gen_tmux(pal, os.path.join(out_dir, f"{pfx}.tmux.conf"))
    gen_zsh(pal, os.path.join(out_dir, f"{pfx}.zsh"))
    gen_k9s(pal, os.path.join(out_dir, f"{pfx}.k9s.yaml"))
    gen_base16(pal, os.path.join(out_dir, f"{pfx}.base16.yaml"))
    gen_yazi(pal, os.path.join(out_dir, f"{pfx}.yazi.toml"))
    gen_btop(pal, os.path.join(out_dir, f"{pfx}.btop.theme"))
    gen_raycast(pal, os.path.join(out_dir, f"{pfx}.raycast.json"))
    gen_fish(pal, os.path.join(out_dir, f"{pfx}.fish"))
    gen_starship(pal, os.path.join(out_dir, f"{pfx}.starship.toml"))
    gen_lazydocker(pal, os.path.join(out_dir, f"{pfx}.lazydocker.yaml"))
    gen_gitui(pal, os.path.join(out_dir, f"{pfx}.gitui.toml"))
    gen_tig(pal, os.path.join(out_dir, f"{pfx}.tigrc"))
    gen_glamour(pal, os.path.join(out_dir, f"{pfx}.glamour.json"))
    gen_pywal(pal, os.path.join(out_dir, f"{pfx}.colors-wal.json"))
    gen_tokens(pal, os.path.join(out_dir, f"{pfx}.tokens.json"))
    gen_oh_my_posh(pal, os.path.join(out_dir, f"{pfx}.omp.json"))
    gen_xcode(pal, os.path.join(out_dir, f"{pfx}.xccolortheme"))
    gen_obsidian(pal, os.path.join(out_dir, f"{pfx}.obsidian.css"), os.path.join(out_dir, f"{pfx}-obsidian-manifest.json"))
    gen_slack(pal, os.path.join(out_dir, f"{pfx}-slack.txt"))
    gen_discord(pal, os.path.join(out_dir, f"{pfx}-discord.css"))
    gen_hyper(pal, os.path.join(out_dir, f"{pfx}.hyper.js"))
    gen_tabby(pal, os.path.join(out_dir, f"{pfx}.tabby.yaml"))
    gen_rio(pal, os.path.join(out_dir, f"{pfx}.rio.toml"))


def generate_all_variants(base_dir):
    generate_dark_variant(base_dir)
    generate_light_variant(base_dir)

    # Generate extra variants under themes/variants/
    variants_dir = os.path.join(base_dir, "variants")
    generate_extra_variant(OLED_PALETTE, os.path.join(variants_dir, "oled"))
    generate_extra_variant(PASTEL_PALETTE, os.path.join(variants_dir, "pastel"))
    generate_extra_variant(CYBERPUNK_PALETTE, os.path.join(variants_dir, "cyberpunk"))


# ---------- Apply CLI Command ----------

def apply_themes(variant="dark", dry_run=False):
    home = os.path.expanduser("~")

    if variant == "dark":
        pfx = "halloween"
        def get_src(cat, fn):
            return f"themes/{cat}/{pfx}.{fn}"
    elif variant == "light":
        pfx = "halloween-light"
        def get_src(cat, fn):
            return f"themes/light/{pfx}.{fn}"
    else:
        pfx = f"halloween-{variant}"
        def get_src(cat, fn):
            return f"themes/variants/{variant}/{pfx}.{fn}"

    # Candidates for auto-application
    candidates = [
        ("Ghostty",
         os.path.join(home, ".config", "ghostty", "themes"),
         f"{pfx}.ghostty",
         get_src("terminal", "ghostty")),
        ("Alacritty",
         os.path.join(home, ".config", "alacritty"),
         f"{pfx}.toml",
         get_src("terminal", "alacritty.toml")),
        ("Kitty",
         os.path.join(home, ".config", "kitty"),
         f"{pfx}.conf",
         get_src("terminal", "kitty.conf")),
        ("WezTerm",
         os.path.join(home, ".config", "wezterm", "colors"),
         f"{pfx}.toml",
         get_src("terminal", "wezterm.toml")),
        ("K9s",
         os.path.join(home, ".config", "k9s", "skins"),
         f"{pfx}.yaml",
         get_src("terminal", "k9s.yaml")),
        ("Yazi",
         os.path.join(home, ".config", "yazi"),
         "theme.toml",
         get_src("terminal", "yazi.toml")),
        ("Btop",
         os.path.join(home, ".config", "btop", "themes"),
         f"{pfx}.theme",
         get_src("terminal", "btop.theme")),
        ("Lazydocker",
         os.path.join(home, ".config", "lazydocker"),
         f"{pfx}.yaml",
         get_src("app", "lazydocker.yaml")),
        ("Fish",
         os.path.join(home, ".config", "fish", "conf.d"),
         f"{pfx}.fish",
         get_src("app", "fish")),
        ("tmux",
         os.path.join(home, ".tmux"),
         f"{pfx}.tmux.conf",
         get_src("app", "tmux.conf")),
    ]

    print(f"🎃 Scanning installed applications for Halloween Theme auto-apply (variant: {variant})...\n")
    applied = 0
    if getattr(sys, "frozen", False):
        base_repo = os.getcwd()
        if not os.path.isdir(os.path.join(base_repo, "themes")):
            bin_dir = os.path.dirname(os.path.abspath(sys.executable))
            parent_dir = os.path.dirname(bin_dir)
            if os.path.isdir(os.path.join(parent_dir, "themes")):
                base_repo = parent_dir
            elif os.path.isdir(os.path.join(bin_dir, "themes")):
                base_repo = bin_dir
    else:
        base_repo = os.path.dirname(os.path.abspath(__file__))

    for app_name, target_dir, target_fn, rel_src in candidates:
        src_path = os.path.join(base_repo, rel_src)
        if not os.path.exists(src_path):
            continue

        parent_dir = os.path.dirname(target_dir) if not os.path.isdir(target_dir) and target_dir.endswith(".toml") else target_dir
        if os.path.exists(target_dir) or os.path.exists(parent_dir):
            dest_file = os.path.join(target_dir, target_fn)
            if dry_run:
                print(f"  [DRY-RUN] Would install {app_name} theme to: {dest_file}")
            else:
                os.makedirs(target_dir, exist_ok=True)
                shutil.copyfile(src_path, dest_file)
                print(f"  ✓ Installed {app_name} theme -> {dest_file}")
            applied += 1
        else:
            print(f"  - {app_name}: config directory not found (skipped)")

    mode_str = "would be applied (dry-run)" if dry_run else "applied successfully"
    print(f"\n✨ Done! {applied} themes {mode_str}.")


# ---------- Main ----------

def main():
    # If the first non-option argument is 'apply', run apply
    args_list = sys.argv[1:]
    if "apply" in args_list:
        ap_apply = argparse.ArgumentParser(description="Auto-detect installed apps and apply Halloween themes.")
        ap_apply.add_argument("apply_cmd", nargs="?", default="apply")
        ap_apply.add_argument("--variant", default="dark", choices=["dark", "light", "oled", "pastel", "cyberpunk"], help="Theme variant (default: dark)")
        ap_apply.add_argument("--dry-run", action="store_true", help="Preview actions without modifying files")
        parsed = ap_apply.parse_args(args_list)
        apply_themes(variant=parsed.variant, dry_run=parsed.dry_run)
        return

    ap = argparse.ArgumentParser(description="Generate Halloween theme files.")
    ap.add_argument("--out", default="themes", help="Output directory (default: themes)")
    args = ap.parse_args()
    base = args.out
    ensure(base)

    generate_all_variants(base)

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
