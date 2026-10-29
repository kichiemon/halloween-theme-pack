# Orca Halloween Theme

A Halloween-themed color set for Orca (stablyai/orca) and friends.

![Preview](assets/preview.png)

## Palette

| Role | Hex |
|---|---|
| Background (deep purple night) | `#1a0d2e` |
| Foreground (bone) | `#f4e7d3` |
| Accent (pumpkin) | `#ff6b35` |
| Success (slime green) | `#39ff14` |
| Destructive (blood red) | `#ff4d6d` |
| Secondary | `#2d1b4e` |
| Border | `#3d2a5e` |
| Sidebar | `#150a24` |

## Files

### Orca (primary)
- `halloween.yaml` — Terminal theme (Warp format, importable via Settings → Terminal → Import from YAML)
- `halloween.css` — App UI theme (chat/sidebar/panels) as CSS variable overrides (early-access feature)

### Generated (`themes/`, via `generate.py`)
- `themes/terminal/halloween.yaml` — Warp / Orca
- `themes/terminal/halloween.itermcolors` — iTerm2
- `themes/terminal/halloween.ghostty` — Ghostty
- `themes/terminal/halloween.alacritty.toml` — Alacritty
- `themes/terminal/halloween.wezterm.toml` — WezTerm
- `themes/terminal/halloween.kitty.conf` — kitty
- `themes/editor/halloween-vscode.json` — VS Code
- `themes/app/halloween-slack.txt` — Slack theme string
- `themes/app/halloween-discord.css` — Discord (BetterDiscord)
- `themes/app/halloween.tmux.conf` — tmux
- `themes/app/halloween.zsh` — zsh prompt

## Regenerate

```bash
python3 generate.py            # writes to ./themes/
python3 generate.py --out DIR  # custom output dir
```

Edit the palette in `generate.py` (the `P`, `ANSI`, `BRIGHT` dicts) and re-run to produce a new variant.

## Install

- **Orca terminal**: Settings → Appearance → Terminal → Import from YAML → pick `halloween.yaml`
- **iTerm2**: Preferences → Profiles → Colors → Color Presets → Import
- **Ghostty/Alacritty/WezTerm/kitty**: copy the file to the app's config dir
- **VS Code**: place `halloween-vscode.json` under `~/.vscode/extensions/` or load as color theme
- **Slack**: paste the string from `halloween-slack.txt` into Preferences → Themes → Custom
- **tmux**: `source-file themes/app/halloween.tmux.conf`

## Status

- Private repo (will be made public later)
- App UI theme depends on Orca internals (stablyai/orca discussion #25456) — version-specific, unofficial
