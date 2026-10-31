---
name: halloween-theme-pack
description: "Apply Halloween themes (200+ variants) to terminals, editors, chat apps, and TUIs. Use when user wants to theme their dev environment, change terminal colors, or apply a Halloween aesthetic. Supports Ghostty, iTerm2, Alacritty, Kitty, WezTerm, VS Code, Neovim, Slack, Discord, tmux, and 20+ more apps."
---

# Halloween Theme Pack — Agent Skill

A Halloween-themed color set for 30+ apps with 200+ theme variants (Dark, Light, OLED, Pastel, Cyberpunk, Phantom, Vampire). Single source of truth palette → generates all formats.

## When to Use

- User asks to theme, color, or style their terminal/editor/chat app
- User mentions Halloween, spooky, pumpkin, cyberpunk, or neon terminal
- User wants to apply a color scheme to Ghostty, iTerm2, Alacritty, Kitty, WezTerm, VS Code, Neovim, Slack, Discord, tmux, etc.
- User asks to generate a custom theme or palette
- User wants to check WCAG contrast of a theme

## Available Commands

All commands use the `halloween-gen` binary (or `python3 generate.py`):

```bash
# Generate all theme files to ./themes/
halloween-gen

# Generate to custom directory
halloween-gen --out DIR

# Auto-detect installed apps and apply themes
halloween-gen apply
halloween-gen apply --variant cyberpunk
halloween-gen apply --dry-run

# Interactive installer (choose apps and variant)
halloween-gen install
halloween-gen install --variant dark --dry-run

# Ambient auto-switcher (dark/light mode)
halloween-gen switcher
halloween-gen switcher --once
```

## Theme Variants

| Variant | Style | Background | Accent |
|---|---|---|---|
| dark | Halloween Night | `#1a0d2e` (deep purple) | `#ff6b35` (pumpkin) |
| light | Halloween Day | `#faf4eb` (warm cream) | `#bf4904` (dark orange) |
| oled | Pure Void | `#000000` (pure black) | `#ff6b35` (pumpkin) |
| pastel | Spooky Kawaii | `#faf5fc` (light lilac) | `#bf4904` (dark orange) |
| cyberpunk | Neon Pumpkin | `#0d0221` (deep void) | `#ff6d00` (neon orange) |
| phantom | Phantom Mint | `#0e1626` (dark blue) | `#2ef8a0` (mint) |
| vampire | Vampire Velvet | `#4a0e17` (dark red) | `#d4af37` (gold) |

## How to Apply Themes

### Quick Apply (auto-detect)
```bash
halloween-gen apply --variant dark
```

### Manual Apply

**Ghostty:** Append `themes/terminal/halloween.ghostty` to `~/.config/ghostty/config`

**iTerm2:** Import `themes/terminal/halloween.itermcolors` (double-click or Preferences → Profiles → Colors → Import)

**Alacritty:** Copy `themes/terminal/halloween.alacritty.toml` to `~/.config/alacritty/alacritty.toml`

**Kitty:** Copy `themes/terminal/halloween.kitty.conf` to `~/.config/kitty/kitty.conf`

**WezTerm:** Copy `themes/terminal/halloween.wezterm.toml` to `~/.config/wezterm/wezterm.lua`

**VS Code:** Copy `themes/editor/halloween-vscode.json` to `~/.vscode/extensions/`

**Neovim:** Copy `themes/editor/halloween-nvim.vim` to `~/.config/nvim/colors/`

**Slack:** Import `themes/app/halloween.slack` via Slack preferences

**Discord:** Use `themes/app/halloween.discord.css` with BetterDiscord

**tmux:** Add `source-file /path/to/halloween.tmux.conf` to `~/.tmux.conf`

## Palette (Single Source of Truth)

The canonical palette is defined in `generate.py` as `DARK_PALETTE`:

```python
{
    "background": "#1a0d2e",      # deep purple night
    "foreground": "#f4e7d3",      # bone
    "accent": "#ff6b35",          # pumpkin (primary brand)
    "success": "#39ff14",         # slime green
    "destructive": "#ff4d6d",     # blood red
    "card": "#241340",
    "secondary": "#2d1b4e",
    "muted": "#b8a9d9",
    "border": "#3d2a5e",
    "blue": "#6b8cff",
    "magenta": "#c77dff",
    "cyan": "#5ffbf1",
    "yellow": "#ffb347",
}
```

## WCAG Accessibility

All themes are WCAG AA/AAA compliant. Run validation:

```bash
python3 validate.py
```

## Generated Files Structure

```
themes/
├── terminal/     # Warp, iTerm2, Ghostty, Alacritty, WezTerm, kitty, Windows Terminal, Hyper, Tabby, Rio, K9s, Base16, Yazi, Glamour, Pywal, btop
├── editor/       # VS Code, Obsidian, Xcode, Neovim
├── app/          # Raycast, Lazydocker, Tokens, fish, Starship, oh-my-posh, tig, gitui, Slack, Discord, tmux, zsh, Chrome
├── light/        # Light mode variants
└── variants/     # OLED, Pastel, Cyberpunk, Phantom, Vampire
```

## Interactive Preview

Open `preview/index.html` in a browser for live preview with:
- 5 theme variants with instant switching
- Live hex tweaker with multi-format export
- Real-time WCAG contrast inspector
- Colorblind vision simulator (deuteranopia, protanopia, tritanopia, achromatopsia)
- Clickable palette swatches

## For AI Agents

When a user asks to theme their environment:

1. Run `halloween-gen apply --dry-run` first to show what would change
2. Ask which variant they prefer (show the 7 options)
3. Apply with `halloween-gen apply --variant <choice>`
4. Verify with `python3 validate.py` if they want accessibility check
5. If they want a custom palette, edit `DARK_PALETTE` in `generate.py` and regenerate

When a user provides an image or description for a custom theme:
1. Extract dominant colors from the description/image
2. Create a new palette dict following the `DARK_PALETTE` structure
3. Replace `DARK_PALETTE` in `generate.py` (or create a new palette file)
4. Run `halloween-gen` to generate all formats
5. Run `halloween-gen apply` to apply

## Links

- Repository: https://github.com/kichiemon/halloween-theme-pack
- Releases: https://github.com/kichiemon/halloween-theme-pack/releases
- Preview: preview/index.html (open in browser)
