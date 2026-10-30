# 🎃 Halloween Theme Pack

A Halloween-themed color set for Orca (stablyai/orca), modern terminals, editors, Kubernetes/Git TUIs, and messaging apps.

[![Release](https://github.com/kichiemon/halloween-theme-pack/actions/workflows/release.yml/badge.svg)](https://github.com/kichiemon/halloween-theme-pack/actions/workflows/release.yml)

![Preview](assets/preview.png)

Open `preview/index.html` in your browser for an **interactive live preview & theme studio** featuring 5 theme variants, live hex tweaker with multi-format export, real-time WCAG AA/AAA contrast inspector, colorblind vision simulator, and clickable palette swatches (pure HTML/CSS/JS, zero dependencies).

---

## 🚀 Quick Start

Download `bin/halloween-gen` (or grab cross-platform binaries from [GitHub Releases](https://github.com/kichiemon/halloween-theme-pack/releases)):

```bash
./bin/halloween-gen            # generates all formats to ./themes/
./bin/halloween-gen --out DIR  # custom output directory
```

### Interactive Installer
Talk to the tool and install themes to only the apps you choose:

```bash
./bin/halloween-gen install
```

The installer will:
1. Ask which variant (dark / light / oled / pastel / cyberpunk)
2. Detect installed apps and show their config paths
3. Let you pick which apps to install to (comma-separated numbers, or "all")
4. Show a summary and ask for confirmation before writing anything

```bash
./bin/halloween-gen install --variant dark --dry-run  # preview without writing
```

No Python required — single self-contained binary.

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
- **Apple Terminal**: Double-click `.terminal` file to import into Terminal.app.

### DevOps, TUIs & Tools
- **K9s**: Copy `themes/terminal/halloween.k9s.yaml` to `~/.config/k9s/skins/skin.yaml`.
- **Yazi**: Copy `themes/terminal/halloween.yazi.toml` to `~/.config/yazi/theme.toml`.
- **Lazydocker**: Copy `themes/app/halloween.lazydocker.yaml` to `~/.config/lazydocker/config.yml`.
- **btop++**: Copy `themes/terminal/halloween.btop.theme` to `~/.config/btop/themes/`.
- **tig**: Include in `~/.tigrc` via `source /path/to/halloween.tigrc`.
- **gitui**: Copy `themes/app/halloween.gitui.toml` to `~/.config/gitui/theme.ron`.
- **Glamour / Glow**: Render with `glow -s themes/terminal/halloween.glamour.json README.md`.
- **Pywal**: Run `wal --theme themes/terminal/halloween.colors-wal.json`.
- **Base16 / Tinted**: Copy `themes/terminal/halloween.base16.yaml` to your Base16 scheme repository.

### Shells & Prompts
- **fish shell**: Copy `themes/app/halloween.fish` to `~/.config/fish/conf.d/halloween.fish`.
- **Starship**: Append palette from `themes/app/halloween.starship.toml` into `~/.config/starship.toml`.
- **oh-my-posh**: Load via `eval "$(oh-my-posh init zsh --config themes/app/halloween.omp.json)"`.
- **zsh**: Source `halloween.zsh` in your `~/.zshrc`.
- **Chrome/Chromium**: Load `halloween-chrome.json` as an unpacked extension (chrome://extensions → Developer mode → Load unpacked).

### Editors & Design
- **VS Code**: Place `*-vscode.json` under `~/.vscode/extensions/` or load as a custom color theme.
- **Obsidian**: Create `.obsidian/themes/halloween/` and copy `halloween.obsidian.css` (renamed to `theme.css`) + `manifest.json`.
- **Xcode**: Copy `themes/editor/halloween.xccolortheme` to `~/Library/Developer/Xcode/UserData/FontAndColorThemes/`.
- **Raycast**: Import `themes/app/halloween.raycast.json` in Settings → Appearance → Import Theme.
- **Figma / Tokens Studio**: Import `themes/app/halloween.tokens.json` into Tokens Studio.
- **Neovim / Vim**: Copy colorscheme files from `themes/` to `~/.config/nvim/colors/` (if applicable).

### Messaging
- **Slack**: Paste the comma-separated string from `halloween-slack.txt` into Preferences → Themes → Custom.
- **Discord**: Apply `*-discord.css` in BetterDiscord custom CSS settings.

---

## ⚡ One-Command Auto Apply (`halloween apply`)

Auto-detects installed applications and places theme files into their config folders:

```bash
./bin/halloween-gen apply            # auto-detect and apply dark theme
./bin/halloween-gen apply --variant light
./bin/halloween-gen apply --variant oled
./bin/halloween-gen apply --dry-run  # preview without modifying
```

Detected apps: Ghostty, Alacritty, Kitty, WezTerm, K9s, Yazi, btop++, Lazydocker, Fish, tmux, and more.

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
True `#000000` pitch black background designed for OLED / Liquid Retina XDR displays.

### 4. Halloween Pastel (Spooky Kawaii / Light)
Soft lavender mist (`#faf5fc`) with deep plum typography (`#3c2a4d`) and pastel-friendly accents.

### 5. Halloween Cyberpunk (Neon Pumpkin & Plasma / Dark)
Deep synthwave plasma void (`#0d0221`) paired with hyper-saturated neon pumpkin (`#ff6d00`), laser slime cyan (`#00f5d4`), and plasma red (`#ff0054`).

---

## 📁 Generated Files

Generated via `generate.py` (or the pre-built `bin/halloween-gen` binary). Full list in `themes/`:

```
themes/
├── terminal/     # Warp, iTerm2, Ghostty, Alacritty, WezTerm, kitty, Windows Terminal, Hyper, Tabby, Rio, K9s, Base16, Yazi, Glamour, Pywal, btop
├── editor/       # VS Code, Obsidian, Xcode
├── app/          # Raycast, Lazydocker, Tokens, fish, Starship, oh-my-posh, tig, gitui, Slack, Discord, tmux, zsh, Chrome
├── light/        # Light mode variants of all above
└── variants/     # OLED, Pastel, Cyberpunk (each with full format set)
```

---

## 🔧 Regenerate & Validate (from source)

```bash
python3 generate.py            # writes to ./themes/
python3 generate.py --out DIR  # custom output dir
python3 validate.py            # validates all generated theme files & variants
```

### Validation Suite (`validate.py`)
Checks:
- **WCAG AA Contrast**: Verifies foreground/background and accent pairs meet ≥4.5:1 text contrast ratio across all 5 variants.
- **Theme Name Uniqueness**: Ensures no collisions across variants.
- **Hex Syntax**: Strict validation of `#RGB` / `#RRGGBB` format across all generated files.
- **Required Fields**: Verifies structure for all formats (YAML, TOML, JSON, XML, Plist, CSS, fish, etc.).

### Building the Single Binary
```bash
python3 -m venv .venv
.venv/bin/pip install pyinstaller
.venv/bin/pyinstaller --onefile --name halloween-gen generate.py
cp dist/halloween-gen bin/
```

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
EOF
echo "written"