# Orca Halloween Theme

A Halloween-themed color set for Orca (stablyai/orca), modern terminals, editors, Kubernetes/Git TUIs, and messaging apps.

[![Release](https://github.com/kichiemon/halloween-theme-pack/actions/workflows/release.yml/badge.svg)](https://github.com/kichiemon/halloween-theme-pack/actions/workflows/release.yml)

![Preview](assets/preview.png)

Open `preview/index.html` in your browser for an **interactive live preview & theme studio** featuring 5 theme variants, live hex tweaker with multi-format export, real-time WCAG AA/AAA contrast inspector, colorblind vision simulator, and clickable palette swatches (pure HTML/CSS/JS, zero dependencies).

---

## 🎨 Palettes & Variants

### 1. Halloween (Night / Dark)
High-contrast deep purple night with pumpkin orange, slime green, and blood red accents.

| Role | Hex | Notes |
|---|---|---|
| Background (deep purple night) | `#1a0d2e` | Base background |
| Foreground (bone) | `#f4e7d3` | Contrast 15.09:1 (WCAG AAA) |
| Accent (pumpkin) | `#ff6b35` | Primary brand & active elements (6.49:1) |
| Success (slime green) | `#39ff14` | High-visibility status & commands |
| Destructive (blood red) | `#ff4d6d` | Errors & warnings |
| Secondary | `#2d1b4e` | Toolbars & active tabs |
| Card / Panel | `#241340` | Surface cards |
| Muted (dusty lilac) | `#b8a9d9` | Comments & line numbers |
| Border | `#3d2a5e` | Dividers |
| Sidebar | `#150a24` | Side navigation panels |

### 2. Halloween Day (Light)
Warm cream parchment background with deep purple typography, pumpkin orange accent, and forest/witch green accents. Fully WCAG AA compliant (4.5:1+ text contrast).

| Role | Hex | Notes |
|---|---|---|
| Background (warm cream) | `#faf4eb` | Base background |
| Foreground (dark purple) | `#241432` | Contrast 15.73:1 (WCAG AAA) |
| Accent (rich pumpkin) | `#bf4904` | Contrast 4.61:1 (WCAG AA Pass) |
| Success (witch green) | `#1b772d` | Contrast 5.16:1 (WCAG AA Pass) |
| Destructive (blood crimson) | `#b81438` | Contrast 6.01:1 (WCAG AA Pass) |
| Secondary | `#e8dcce` | Surface & active backgrounds |
| Card | `#f2e7d8` | Elevated containers |
| Muted | `#756388` | Contrast 5.00:1 (WCAG AA Pass) |
| Border | `#d8c8b4` | Parchment borders |
| Sidebar | `#f4ece1` | Side navigation panels |

### 3. Halloween OLED (Pure Void / Dark)
True `#000000` pitch black background designed for OLED / Liquid Retina XDR displays. Reduces power draw while pushing luminous pumpkin and neon slime accents to extreme contrast (17.22:1 text contrast).

### 4. Halloween Pastel (Spooky Kawaii / Light)
Soft lavender mist (`#faf5fc`) with deep plum typography (`#3c2a4d`) and pastel-friendly accents, balancing cute aesthetic with strict WCAG AA readability (11.98:1 text contrast).

### 5. Halloween Cyberpunk (Neon Pumpkin & Plasma / Dark)
Deep synthwave plasma void (`#0d0221`) paired with hyper-saturated neon pumpkin (`#ff6d00`), laser slime cyan (`#00f5d4`), and plasma red (`#ff0054`) for an aggressive nocturnal aesthetic (18.98:1 text contrast).

---

## 📁 Generated Files (31 Formats / 64 Files)

Generated via `generate.py` (or the pre-built `bin/halloween-gen` binary):

### Dark Mode (`themes/`)
- **Terminals & Shells**:
  - `themes/terminal/halloween.yaml` — Warp / Orca
  - `themes/terminal/halloween.itermcolors` — iTerm2
  - `themes/terminal/halloween.ghostty` — Ghostty
  - `themes/terminal/halloween.alacritty.toml` — Alacritty
  - `themes/terminal/halloween.wezterm.toml` — WezTerm
  - `themes/terminal/halloween.kitty.conf` — kitty
  - `themes/terminal/halloween.windows-terminal.json` — Windows Terminal
  - `themes/terminal/halloween.hyper.js` — Hyper terminal module
  - `themes/terminal/halloween.tabby.yaml` — Tabby
  - `themes/terminal/halloween.rio.toml` — Rio terminal
  - `themes/terminal/halloween.k9s.yaml` — K9s Kubernetes TUI
  - `themes/terminal/halloween.base16.yaml` — Base16 / Tinted Theming scheme
  - `themes/terminal/halloween.yazi.toml` — Yazi terminal file manager
  - `themes/terminal/halloween.glamour.json` — Glamour / Glow Markdown styler
  - `themes/terminal/halloween.colors-wal.json` — Pywal Linux rice colors
  - `themes/terminal/halloween.btop.theme` — btop++ system monitor
- **Editors**:
  - `themes/editor/halloween-vscode.json` — VS Code
  - `themes/editor/halloween.obsidian.css` & `themes/editor/halloween-obsidian-manifest.json` — Obsidian community theme
  - `themes/editor/halloween.xccolortheme` — Apple Xcode theme
- **Apps, Prompts & CLI Tools**:
  - `themes/app/halloween.raycast.json` — Raycast launcher custom theme
  - `themes/app/halloween.lazydocker.yaml` — Lazydocker container manager
  - `themes/app/halloween.tokens.json` — W3C Design Tokens (Figma / Tokens Studio)
  - `themes/app/halloween.fish` — fish shell syntax colors
  - `themes/app/halloween.starship.toml` — Starship cross-shell prompt palette
  - `themes/app/halloween.omp.json` — oh-my-posh prompt theme
  - `themes/app/halloween.tigrc` — tig Git TUI colors
  - `themes/app/halloween.gitui.toml` — GitUI terminal client
  - `themes/app/halloween-slack.txt` — Slack theme string
  - `themes/app/halloween-discord.css` — Discord (BetterDiscord)
  - `themes/app/halloween.tmux.conf` — tmux status & pane styles
  - `themes/app/halloween.zsh` — zsh prompt & syntax highlighting

### Light Mode (`themes/light/`)
- All 31 formats above are mirrored with dedicated light mode palettes in `themes/light/halloween-light.*`.

### Extra Variants (`themes/variants/`)
- `themes/variants/oled/` — Halloween OLED (Pure Void)
- `themes/variants/pastel/` — Halloween Pastel (Spooky Kawaii)
- `themes/variants/cyberpunk/` — Halloween Cyberpunk (Neon Pumpkin & Plasma)

### Orca (UI & Root)
- `halloween.yaml` — Terminal theme (Warp format, synchronized with canonical dark theme)
- `halloween.css` — App UI theme (chat/sidebar/panels) as CSS variable overrides

---

## ⚡ One-Command Auto Apply (`halloween apply`)

Auto-detects installed applications on your system and places theme files into their respective configuration folders automatically:

```bash
# Auto-detect installed apps and apply dark theme
./bin/halloween-gen apply

# Apply light or variant themes
./bin/halloween-gen apply --variant light
./bin/halloween-gen apply --variant oled
./bin/halloween-gen apply --variant pastel
./bin/halloween-gen apply --variant cyberpunk

# Preview detection without modifying files
./bin/halloween-gen apply --dry-run
```

Detected apps include: Ghostty, Alacritty, Kitty, WezTerm, K9s, Yazi, btop++, Lazydocker, Fish, tmux, and more.

---

## 🚀 Quick Start

Download `bin/halloween-gen` (or grab cross-platform binaries from [GitHub Releases](https://github.com/kichiemon/halloween-theme-pack/releases)):

```bash
./bin/halloween-gen            # generates all 31 formats to ./themes/
./bin/halloween-gen --out DIR  # custom output directory
```

No Python required — single self-contained binary.

---

## 🔧 Regenerate & Validate (from source)

```bash
# Generate theme files
python3 generate.py            # writes to ./themes/
python3 generate.py --out DIR  # custom output dir

# Run validation suite
python3 validate.py            # validates all 64 generated theme files & variants
```

### Validation Suite (`validate.py`)
Checks:
- **WCAG AA Contrast**: Verifies foreground/background and accent pairs meet $\ge 4.5:1$ text contrast ratio across all 5 variants.
- **Theme Name Uniqueness**: Ensures no collisions across variants.
- **Hex Syntax**: Strict validation of `#RGB` / `#RRGGBB` format across all generated files.
- **Required Fields**: Verifies structure for all 31 formats (YAML, TOML, JSON, XML, Plist, CSS, fish, etc.).

### Building the Single Binary
```bash
python3 -m venv .venv
.venv/bin/pip install pyinstaller
.venv/bin/pyinstaller --onefile --name halloween-gen generate.py
cp dist/halloween-gen bin/
```

---

## 📦 Installation Guide

### Terminals & Multiplexers
- **Orca terminal**: Settings → Appearance → Terminal → Import from YAML → pick `halloween.yaml`.
- **iTerm2**: Preferences → Profiles → Colors → Color Presets → Import → pick `.itermcolors`.
- **Ghostty**: Copy `halloween.ghostty` into `~/.config/ghostty/themes/` and set `theme = halloween`.
- **Alacritty**: Import into `~/.config/alacritty/alacritty.toml` via `import = ["path/to/halloween.alacritty.toml"]`.
- **WezTerm**: Include in `colors` within `~/.wezterm.lua`.
- **kitty**: Include in `~/.config/kitty/kitty.conf` via `include path/to/halloween.kitty.conf`.
- **Windows Terminal**: Add scheme object from `.windows-terminal.json` to the `schemes` array in `settings.json`.
- **Hyper**: Place `halloween.hyper.js` into `~/.hyper_plugins/local/` and add to `localPlugins` in `.hyper.js`.
- **Tabby**: Paste the contents of `.tabby.yaml` under `terminal.colorScheme` in `config.yaml`.
- **Rio terminal**: Copy `.rio.toml` to `~/.config/rio/themes/` and set `theme = "halloween"`.
- **tmux**: Add `source-file /path/to/halloween.tmux.conf` in `~/.tmux.conf`.

### DevOps, TUIs & Tools
- **K9s**: Copy `themes/terminal/halloween.k9s.yaml` to `~/.config/k9s/skins/skin.yaml` (or reference in `config.yaml`).
- **Yazi**: Copy `themes/terminal/halloween.yazi.toml` to `~/.config/yazi/theme.toml`.
- **Lazydocker**: Copy `themes/app/halloween.lazydocker.yaml` to `~/.config/lazydocker/config.yml` under `gui.theme`.
- **btop++**: Copy `themes/terminal/halloween.btop.theme` to `~/.config/btop/themes/` and set `color_theme = "halloween"`.
- **tig**: Include in `~/.tigrc` via `source /path/to/halloween.tigrc`.
- **gitui**: Copy `themes/app/halloween.gitui.toml` to `~/.config/gitui/theme.ron`.
- **Glamour / Glow**: Render markdown with `glow -s themes/terminal/halloween.glamour.json README.md` or set `GLAMOUR_STYLE`.
- **Pywal**: Run `wal --theme themes/terminal/halloween.colors-wal.json`.
- **Base16 / Tinted**: Copy `themes/terminal/halloween.base16.yaml` to your Base16 scheme repository.

### Shells & Prompts
- **fish shell**: Copy `themes/app/halloween.fish` to `~/.config/fish/conf.d/halloween.fish` or source in `config.fish`.
- **Starship**: Append palette from `themes/app/halloween.starship.toml` into `~/.config/starship.toml`.
- **oh-my-posh**: Load via `eval "$(oh-my-posh init zsh --config themes/app/halloween.omp.json)"`.
- **zsh**: Source `halloween.zsh` in your `~/.zshrc`.

### Editors & Design
- **VS Code**: Place `*-vscode.json` under `~/.vscode/extensions/` or load as a custom color theme.
- **Obsidian**: Create directory `.obsidian/themes/halloween/` and copy `halloween.obsidian.css` (renamed to `theme.css`) and `manifest.json`.
- **Xcode**: Copy `themes/editor/halloween.xccolortheme` to `~/Library/Developer/Xcode/UserData/FontAndColorThemes/`.
- **Raycast**: Import `themes/app/halloween.raycast.json` in Settings → Appearance → Import Theme, or click the generated `shareUrl`.
- **Figma / Tokens Studio**: Import `themes/app/halloween.tokens.json` directly into Tokens Studio for Figma.

### Messaging
- **Slack**: Paste the comma-separated string from `halloween-slack.txt` into Preferences → Themes → Custom.
- **Discord**: Apply `*-discord.css` in BetterDiscord custom CSS settings.

---

## 🌐 Interactive Preview & Web Theme Studio

Open `preview/index.html` directly in any web browser to explore:
- **5 Theme Variants**: Halloween Night (Dark), Halloween Day (Light), Halloween OLED (Pure Void), Halloween Pastel (Spooky Kawaii), and Halloween Cyberpunk (Neon Pumpkin).
- **Web Theme Studio**: Live hex tweaker with real-time mockup updates and instant export to Warp YAML, VS Code JSON, CSS Variables, Alacritty TOML, Raycast JSON, and W3C Tokens.
- **WCAG Contrast Inspector**: Interactive color picker calculating Relative Luminance and contrast ratios against WCAG 2.1 AA / AAA standards in real time.
- **Colorblind-Safe Vision Simulator**: Real-time SVG filter simulation for Deuteranopia (Deutan), Protanopia (Protan), Tritanopia (Tritan), and Achromatopsia (Monochrome).
- **Terminal Mockup**: ANSI 16-color test pattern and realistic command output.
- **VS Code Editor Mockup**: Accurate syntax token highlighting for Python / TypeScript.
- **Design System Showcase**: Buttons, callouts, and swatch cards with one-click hex copying.

---

## 📄 License

[MIT](LICENSE) — Copyright (c) 2026 kichiemon. Feel free to fork, remix, and redistribute.

---

## ⚠️ Disclaimer

The app UI theme (`halloween.css`) overrides Orca's internal CSS custom properties, which are implementation details and may change between Orca versions. It is unofficial and provided as-is. The terminal themes (Warp YAML and other formats) use stable, documented formats and are safe to use.
