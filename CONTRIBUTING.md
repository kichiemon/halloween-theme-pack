# Contributing to Halloween Theme Pack 🎃

Thank you for your interest in contributing to the Halloween Theme Pack! We welcome contributions of all kinds: adding new application theme formats, improving existing palettes, enhancing documentation, or reporting bugs.

## Code of Conduct

This project adheres to the [Contributor Covenant](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code of conduct. Please report unacceptable behavior to [kichiemon.dev@gmail.com](mailto:kichiemon.dev@gmail.com).

---

## Getting Started

### Prerequisites

- **Python 3.9+** (required for `generate.py` and `validate.py`)
- **Node.js 16+** (optional, for testing npm packaging and `bin/install-skill.js`)
- **Git**

### Development Setup

1. **Fork and clone the repository:**

   ```bash
   git clone https://github.com/kichiemon/halloween-theme-pack.git
   cd halloween-theme-pack
   ```

2. **Set up Python virtual environment:**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Verify the environment:**

   ```bash
   python3 generate.py
   python3 validate.py
   ```

   All checks should pass without any errors.

---

## Project Structure

```
halloween-theme-pack/
├── generate.py        # Single source of truth: palette definitions, format templates, CLI commands
├── validate.py        # Validation suite: WCAG AA/AAA contrast checks, hex syntax, file completeness
├── halloween.yaml     # Canonical Warp terminal theme definition
├── halloween.css      # App UI CSS overrides
├── themes/            # Output directory containing 280+ generated theme files
│   ├── terminal/      # Terminal & CLI TUI themes (Ghostty, Alacritty, Kitty, WezTerm, etc.)
│   ├── editor/        # Code editor themes (VS Code, Obsidian, Xcode, Helix, Neovim)
│   ├── app/           # Desktop & web apps (Raycast, Slack, Discord, Chrome, tmux, etc.)
│   ├── light/         # Light mode (Halloween Day) variants
│   └── variants/      # Extra variants (OLED, Pastel, Cyberpunk, Vampire Velvet, Phantom Mint)
├── preview/           # Interactive zero-dependency web theme studio
├── scripts/           # Ambient OS appearance auto-switcher daemon
├── bin/
│   └── install-skill.js  # Agent Skill installer for AI coding assistants
└── SKILL.md           # Agent Skill definition for Claude Code, Cursor, Codex
```

---

## How to Contribute

### 1. Adding a New Application Theme

We welcome templates for new terminal emulators, code editors, and developer tools!

1. Open `generate.py`.
2. Locate the existing generator functions (e.g., `gen_alacritty`, `gen_vscode`).
3. Add a new generator function following the format conventions:
   ```python
   def gen_my_app(p, out_path):
       content = ...  # Format template using palette dictionary `p`
       write(out_path, content)
   ```
4. Register your generator in:
   - `generate_dark_variant(base_dir)`
   - `generate_light_variant(base_dir)`
   - `generate_extra_variant(palette, variant_dir)`
5. If the application configuration can be auto-detected, consider adding it to the `candidates` list in `apply_themes()` and `interactive_install()`.
6. Open `validate.py` and add structural checks for the new format if needed.
7. Run `python3 generate.py && python3 validate.py` to regenerate all files and verify validity.

### 2. Modifying or Adding Palettes

Palettes are defined at the top of `generate.py`:
- `DARK_PALETTE` (Halloween Night)
- `LIGHT_PALETTE` (Halloween Day)
- `OLED_PALETTE` (Pure Void)
- `PASTEL_PALETTE` (Spooky Kawaii)
- `CYBERPUNK_PALETTE` (Neon Pumpkin)
- `VAMPIRE_PALETTE` (Vampire Velvet)
- `PHANTOM_PALETTE` (Phantom Mint)

**Accessibility Requirement:**
All text colors against background pairs **must meet or exceed WCAG AA standards** (minimum 4.5:1 contrast ratio for normal text). `validate.py` enforces this automatically during validation.

---

## Pull Request Guidelines

1. **Create a topic branch:**
   ```bash
   git checkout -b feat/my-new-app-support
   ```
2. **Make your changes:**
   - Keep changes focused and minimal.
   - Do not manually edit files inside `themes/` unless necessary; regenerate them using `python3 generate.py`.
3. **Run the validation suite:**
   ```bash
   python3 generate.py
   python3 validate.py
   ```
   Ensure `validate.py` reports `0 failed checks`.
4. **Commit with Conventional Commits format:**
   - `feat: add Rio terminal support`
   - `fix: resolve hex casing in WezTerm template`
   - `docs: update Ghostty installation instructions`
5. **Push and open a Pull Request:**
   - Describe the purpose and changes clearly.
   - Attach screenshots if proposing visual or preview studio enhancements.

Thank you for helping make the developer terminal a spookier and more accessible place! 🎃
