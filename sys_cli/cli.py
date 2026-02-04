from __future__ import annotations

import os
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

import click
import yaml


@dataclass(frozen=True)
class AppContext:
    repo_root: Path
    config: dict[str, Any]
    verbose: bool
    dry_run: bool


def _default_repo_root() -> Path:
    override = os.environ.get("SYS_REPO_ROOT")
    if override:
        return Path(override).expanduser().resolve()

    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "linux").is_dir() and (parent / "mswin").is_dir():
            return parent

    return Path.cwd().resolve()


def _load_config(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return cast(dict[str, Any], data) if isinstance(data, dict) else {}


def _run(cmd: list[str], *, dry_run: bool, verbose: bool) -> int:
    if verbose or dry_run:
        click.echo("$ " + " ".join(cmd))
    if dry_run:
        return 0
    completed = subprocess.run(cmd)
    return int(completed.returncode)


def _wslpath_windows(p: Path) -> str:
    completed = subprocess.run(
        ["wslpath", "-w", str(p)],
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def _windows_python_exe() -> str:
    exe = shutil.which("python.exe")
    if exe:
        return exe
    raise click.ClickException(
        "python.exe not found on PATH in WSL. "
        "Ensure Windows interop is enabled and Windows Python is installed."
    )


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.option("--config", "config_path", default="~/.config/sys-cli.yaml", show_default=True)
@click.option("--verbose", is_flag=True, help="Print commands being executed.")
@click.option("--dry-run", is_flag=True, help="Print what would run, but do nothing.")
@click.pass_context
def cli(ctx: click.Context, config_path: str, verbose: bool, dry_run: bool) -> None:
    cfg_path = Path(os.path.expanduser(config_path))
    repo_root = _default_repo_root()
    cfg = _load_config(cfg_path)
    ctx.obj = AppContext(repo_root=repo_root, config=cfg, verbose=verbose, dry_run=dry_run)


@cli.command("switch")
@click.argument("device_name", type=str)
@click.pass_obj
def switch_audio(app: AppContext, device_name: str) -> None:
    """Switch Windows audio output device by name."""

    script = app.repo_root / "mswin" / "pycaw-audio-device-switcher" / "__main__.py"
    if not script.exists():
        raise click.ClickException(f"Missing audio switcher script: {script}")

    windows_script_path = _wslpath_windows(script)
    py = _windows_python_exe()

    cmd = [py, windows_script_path, "--switch-audio-device", device_name]
    raise SystemExit(_run(cmd, dry_run=app.dry_run, verbose=app.verbose))


@cli.group("backup")
def backup_group() -> None:
    """Backup helpers."""


@backup_group.command("windows")
@click.pass_obj
def backup_windows(app: AppContext) -> None:
    target = app.repo_root / "mswin" / "backup"
    raise click.ClickException(f"Not implemented yet (target folder is empty): {target}")


@backup_group.command("linux")
@click.pass_obj
def backup_linux(app: AppContext) -> None:
    target = app.repo_root / "linux" / "backup"
    raise click.ClickException(f"Not implemented yet (target folder is empty): {target}")


@cli.command("play")
@click.argument("media_path", type=click.Path(path_type=Path))
@click.pass_obj
def play_media(app: AppContext, media_path: Path) -> None:
    raise click.ClickException("Not implemented yet (mswin/play-media is missing).")


@cli.command("clip")
@click.argument("media_path", type=click.Path(path_type=Path))
@click.pass_obj
def clip_media(app: AppContext, media_path: Path) -> None:
    raise click.ClickException("Not implemented yet (linux/clipper is missing).")


@cli.group("dl")
def dl_group() -> None:
    """yt-dlp helpers."""


@dl_group.command("video")
@click.argument("url", type=str)
@click.pass_obj
def dl_video(app: AppContext, url: str) -> None:
    raise click.ClickException("Not implemented yet (linux/yt-dlp-container is missing).")


@dl_group.command("audio")
@click.argument("url", type=str)
@click.pass_obj
def dl_audio(app: AppContext, url: str) -> None:
    raise click.ClickException("Not implemented yet (linux/yt-dlp-container is missing).")


def main() -> None:
    cli(prog_name="sys")
