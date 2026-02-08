# System Automation

## Purpose

Windows automation and utility CLI.  Linux-first and intended to be run from WSL directly.

This repo assumes:

- You develop/run `sys` from WSL.
- Windows calls into WSL for most commands via `wsl.exe`.
- Windows-only features (like switching the Windows audio output device) are executed by `python.exe` (Windows Python), even when invoked from WSL.

## CLI

```bash
sys switch {device_name} -> (@windows) pycaw-audio-device-switcher {device_name}
sys backup windows -> mswin/backup
sys backup linux -> linux/backup
sys play {path/to/sound} [-d device] -> (@windows) sounddevice-audio-player {file} [--device name]
sys clip {path/to/media} -> linux/clipper
sys dl video {url} -> linux/yt-dlp-container
sys dl audio {url} -> linux/yt-dlp-container
sys startup windows -> mswin/startup
sys startup linux -> linux/startup
```

Notes:

- `sys switch` and `sys play` are implemented.
- The other commands are placeholders and will error until their target scripts exist.

## Setup

Everything is run from a WSL terminal. There are two pieces:

1. **Windows Python deps** — `mswin/` sub-projects run via `python.exe` (Windows Python), so their packages must be installed there.
2. **WSL CLI** — the `sys` command itself is installed in WSL via `pipx`.

### 1. Windows Python dependencies

```bash
# Verify Windows Python is reachable from WSL
python.exe --version

# Install deps for each mswin sub-project
python.exe -m pip install -r mswin/pycaw-audio-device-switcher/requirements.txt
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