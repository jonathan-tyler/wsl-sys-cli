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