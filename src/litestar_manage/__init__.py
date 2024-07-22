from __future__ import annotations
from pathlib import Path
import os
import subprocess

from ruff.__main__ import find_ruff_bin

from copier import run_copy, Worker


def entrypoint() -> None:
    _SINGLE_FILE_TEMPLATE = Path(__file__).parent / "applet_templates" / "single_file"

    with Worker():
        run_copy(str(_SINGLE_FILE_TEMPLATE), ".")

    _run_ruff("check", "--select", "I", "--fix", "--unsafe-fixes", "app.py")
    _run_ruff("format", "app.py")


def _run_ruff(*options: str) -> None:
    ruff = os.fsdecode(find_ruff_bin())
    subprocess.run([ruff, *options])
