#!/usr/bin/env python3
"""Halloween Theme Pack - Ambient Auto-Switcher Daemon.

Automatically synchronizes terminal, editor, and desktop app themes with the
host operating system's appearance (Light vs Dark mode).

Supported platforms:
  - macOS (defaults read -g AppleInterfaceStyle)
  - Linux GNOME / FreeDesktop (gsettings / XDG desktop portal)
  - Windows (registry AppsUseLightTheme)

Usage:
    python3 scripts/ambient_switcher.py --once
    python3 scripts/ambient_switcher.py --interval 5
    python3 scripts/ambient_switcher.py --dark-variant vampire --light-variant pastel
"""
import argparse
import os
import platform
import subprocess
import sys
import time


def detect_os_dark_mode() -> bool:
    """Detect whether host OS is currently in Dark Mode."""
    sys_name = platform.system()
    if sys_name == "Darwin":
        try:
            res = subprocess.run(
                ["defaults", "read", "-g", "AppleInterfaceStyle"],
                capture_output=True,
                text=True,
            )
            return res.returncode == 0 and "Dark" in res.stdout
        except Exception:
            return True
    elif sys_name == "Linux":
        try:
            res = subprocess.run(
                ["gsettings", "get", "org.gnome.desktop.interface", "color-scheme"],
                capture_output=True,
                text=True,
            )
            if res.returncode == 0 and "prefer-dark" in res.stdout:
                return True
            res2 = subprocess.run(
                ["gsettings", "get", "org.gnome.desktop.interface", "gtk-theme"],
                capture_output=True,
                text=True,
            )
            if res2.returncode == 0 and "dark" in res2.stdout.lower():
                return True
        except Exception:
            pass
        return True
    elif sys_name == "Windows":
        try:
            import winreg

            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
            )
            val, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            return val == 0
        except Exception:
            return True
    return True


def run_switcher(
    dark_variant: str = "dark",
    light_variant: str = "light",
    daemon: bool = False,
    interval: int = 5,
    dry_run: bool = False,
):
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    gen_py = os.path.join(repo_root, "generate.py")
    bin_path = os.path.join(repo_root, "bin", "halloween-gen")

    last_mode = None
    print("🎃 Halloween Ambient Theme Auto-Switcher Daemon")
    print(f"   Platform:      {platform.system()}")
    print(f"   Dark Variant:  {dark_variant}")
    print(f"   Light Variant: {light_variant}")
    print(
        f"   Mode:          {'Daemon (polling every ' + str(interval) + 's)' if daemon else 'One-shot'}"
    )
    if dry_run:
        print("   Flags:         DRY RUN (no file writes)")

    while True:
        is_dark = detect_os_dark_mode()
        current_mode = "dark" if is_dark else "light"
        chosen_variant = dark_variant if is_dark else light_variant

        if current_mode != last_mode:
            print(
                f"\n✨ OS Appearance: {current_mode.upper()} mode detected -> applying variant '{chosen_variant}'"
            )
            if os.path.exists(bin_path) and os.access(bin_path, os.X_OK):
                cmd = [bin_path, "apply", "--variant", chosen_variant]
            else:
                cmd = [sys.executable, gen_py, "apply", "--variant", chosen_variant]
            if dry_run:
                cmd.append("--dry-run")
            subprocess.run(cmd)
            last_mode = current_mode

        if not daemon:
            break
        try:
            time.sleep(interval)
        except KeyboardInterrupt:
            print("\n👋 Ambient Auto-Switcher daemon stopped.")
            break


def main():
    parser = argparse.ArgumentParser(
        description="Halloween Ambient Auto-Switcher based on OS appearance."
    )
    parser.add_argument("--once", action="store_true", help="Run once and exit")
    parser.add_argument(
        "--interval",
        type=int,
        default=5,
        help="Polling interval in seconds for daemon mode (default: 5)",
    )
    parser.add_argument(
        "--dark-variant",
        default="dark",
        choices=["dark", "oled", "cyberpunk", "vampire", "phantom"],
        help="Variant for Dark mode (default: dark)",
    )
    parser.add_argument(
        "--light-variant",
        default="light",
        choices=["light", "pastel"],
        help="Variant for Light mode (default: light)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview actions without modifying files",
    )
    args = parser.parse_args()

    run_switcher(
        dark_variant=args.dark_variant,
        light_variant=args.light_variant,
        daemon=not args.once,
        interval=args.interval,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()
