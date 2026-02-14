# System Automation

## Purpose

Windows automation and utility CLI.  Linux-first and intended to be run from WSL directly.

This repo assumes:

- You develop/run `sys` from WSL.
- Windows calls into WSL for most commands via `wsl.exe`.
- Windows-only features (like switching the Windows audio output device) are executed by `python.exe` (Windows Python), even when invoked from WSL.

## CLI

```bash
sys switch {device_name} -> (@windows) audio-device-switcher-pycaw {device_name}
sys play {path/to/sound} [-d device] -> (@windows) sounddevice-audio-player {file} [--device name]
```

## Setup

Everything is run from a WSL terminal. There are two pieces:

1. **WSL CLI** — the `sys` command itself is installed in WSL via `pipx`.
2. **Windows Python deps** — `mswin/` sub-projects run via `python.exe` (Windows Python), so their packages must be installed there.

### 1. Windows Python dependencies

```bash
# Verify Windows Python is reachable from WSL
python.exe --version

# Install deps for each mswin sub-project
python.exe -m pip install -r mswin/audio-device-switcher-pycaw/requirements.txt
python.exe -m pip install -r mswin/sounddevice-audio-player/requirements.txt
```

### 2. WSL CLI (`sys`)

```bash
# Install pipx if you don't have it
sudo dnf install pipx    # Fedora
python3 -m pipx ensurepath

# Install the CLI in editable mode (picks up code changes without reinstalling)
pipx install --editable .

# Verify
sys --help
```

## Type Stubs (Pylance/Pyright)

This repo is a multi-tool workspace. Each Windows sub-project under `mswin/` can keep its own local stubs under:

- `mswin/<tool>/typings/`

However, Pylance effectively wants a single `python.analysis.stubPath` per workspace folder, so we also maintain an aggregate stub directory at:

- `typings/` (top-level)

The aggregate directory contains symlinks pointing back to the per-tool stubs.

### Workflow

1. Add/update stubs inside the owning tool’s `mswin/<tool>/typings/`.
2. Regenerate the aggregate symlinks:

```bash
sys typings
```

### Conventions

- If the dependency is imported as a *module* (e.g. `import sounddevice`), prefer a module stub: `sounddevice.pyi`.
- If the dependency is imported as a *package* (e.g. `from pycaw.utils import ...`), use a package stub directory: `pycaw/__init__.pyi` (plus any submodule `.pyi` files).