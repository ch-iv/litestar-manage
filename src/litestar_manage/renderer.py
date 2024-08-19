from __future__ import annotations

import os
import shutil
import subprocess
import sys
import sysconfig
from dataclasses import dataclass
from pathlib import Path

from jinja2 import Template


def render_template(
    template_dir: Path,
    output_dir: Path,
    ctx: RenderingContext,
    run_ruff: bool = True,
) -> None:
    """Renders a template from template_dir to output_dir using the provided context.
    Optionally runs ruff on the generated files.
    """
    _render_jinja_dir(template_dir, output_dir, ctx)

    if run_ruff:
        _run_ruff(
            "check",
            "--select",
            "I",
            "--fix",
            "--unsafe-fixes",
            "--silent",
            str(output_dir.absolute()),
        )
        _run_ruff("format", "--silent", str(output_dir.absolute()))


@dataclass
class RenderingContext:
    """Context for rendering an application template."""

    app_name: str


def _render_jinja_dir(
    input_directory: Path,
    output_directory: Path,
    ctx: RenderingContext,
) -> list[Path]:
    """Recursively renders all files in the input directory to the output directory,
    while preserving the file-tree structure. Returns the list of paths to the created files.

    Only files with extensions .jinja and .jinja2 are rendered, while the rest are copied.
    """
    files_written = []

    for path in input_directory.iterdir():
        rendered_name = Template(path.name).render(ctx.__dict__)
        render_body = False

        if path.suffix in [".jinja", ".jinja2"]:
            rendered_name = rendered_name.removesuffix(path.suffix)
            render_body = True

        if rendered_name == "":
            continue

        if path.is_file():
            output_directory.mkdir(parents=True, exist_ok=True)

            if render_body:
                with (
                    Path.open(path, encoding="utf-8") as input_file,
                    Path.open(
                        output_directory / rendered_name,
                        "w",
                        encoding="utf-8",
                    ) as output_file,
                ):
                    output_file.write(Template(input_file.read()).render(ctx.__dict__))

            else:
                shutil.copy(path, output_directory / rendered_name)

            files_written.append(output_directory / rendered_name)

        elif path.is_dir():
            files_written.extend(
                _render_jinja_dir(path, output_directory / rendered_name, ctx),
            )

    return files_written


def find_ruff_bin() -> Path:
    """Return the ruff binary path."""

    ruff_exe = Path("ruff" + sysconfig.get_config_var("EXE"))

    scripts_path = Path(sysconfig.get_path("scripts")) / ruff_exe
    if scripts_path.is_file():
        return scripts_path

    if sys.version_info >= (3, 10): # noqa: UP036
        user_scheme = sysconfig.get_preferred_scheme("user")
    elif os.name == "nt":
        user_scheme = "nt_user"
    elif sys.platform == "darwin" and sys._framework:
        user_scheme = "osx_framework_user"
    else:
        user_scheme = "posix_user"

    user_path = Path(sysconfig.get_path("scripts", scheme=user_scheme)) / ruff_exe
    if user_path.is_file():
        return user_path

    # Search in `bin` adjacent to package root (as created by `pip install --target`).
    pkg_root = Path(__file__).parent.parent
    target_path = pkg_root / "bin" / ruff_exe
    if target_path.is_file():
        return target_path

    raise FileNotFoundError(scripts_path)


def _run_ruff(*options: str) -> None:
    """Runs ruff with provided options"""
    ruff = os.fsdecode(find_ruff_bin())
    subprocess.run([ruff, *options], check=False)
