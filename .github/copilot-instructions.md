# Copilot Instructions — sys repo

## Architecture

- **WSL-first CLI**: `sys_cli/` is a Click-based CLI installed in WSL via `pipx`.
- **Windows sub-projects**: Live under `mswin/`. Each is a standalone Python script invoked by `sys_cli` via `python.exe` subprocess (not imported).
- **Linux sub-projects**: Live under `linux/`.
- The CLI bridges WSL→Windows by converting paths with `wslpath -w` and calling `python.exe`.

## Adding a new `mswin/` sub-project

1. Create a kebab-case folder: `mswin/<project-name>/`
2. Required files, following `mswin/pycaw-audio-device-switcher/` as the canonical example:
   - `__main__.py` — Entry point with `register_args(parser)`, `run(args)`, and `if __name__ == "__main__"` block. Use `try/except ImportError` for relative vs direct imports.
   - `<snake_case_module>.py` — Core logic in a PascalCase class.
   - `pyproject.toml` — Minimal metadata (name, version, readme, requires-python, authors, platforms).
   - `pyrightconfig.json` — `{"include": ["."]}`, add `"stubPath"` if needed.
   - `requirements.txt` — Pinned or minimum-version dependencies.
   - `README.md` — Setup and usage.
3. Wire it into `sys_cli/cli.py`: add a Click command that locates the script via `app.repo_root / "mswin" / "<project>" / "__main__.py"`, converts paths with `_wslpath_windows()`, and runs via `_run()`.
   - **Always use blocking `_run()`** — never fire-and-forget `subprocess.Popen`. Sub-projects need stdout/stderr visible for debugging, and the process must complete before the CLI exits.

## Gotchas

- **`mswin/` dependencies live in Windows Python.** Install via `python.exe -m pip install -r requirements.txt`, not the WSL pip.
- **`sd.query_devices()`** returns a `DeviceList`, not a `list`. Use `isinstance(devices, dict)` to detect the single-device case, not `not isinstance(devices, list)`.

## Conventions

- Folder names: `kebab-case`
- Python modules: `snake_case`
- Classes: `PascalCase`
- Private methods: `__double_underscore` (name-mangled)
- CLI subcommand names: short, lowercase (e.g. `switch`, `play`, `backup`)
- Type hints: use `from __future__ import annotations` in all files
- Python version: `>=3.8` for sub-projects, `>=3.10` for sys_cli

## AHK integration

- AHK scripts under `mswin/ahk/extensions/` call `sys` via `wsl.exe -e zsh -lc "sys ..."`.
