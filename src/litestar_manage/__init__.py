from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os
import subprocess
from typing import List
import shutil

from ruff.__main__ import find_ruff_bin

from jinja2 import Template


def entrypoint() -> None:
    _SINGLE_FILE_TEMPLATE = Path(__file__).parent / "templates" / "basic"
    _OUTPUT_DIR = Path(__file__).parent.parent.parent / "rendered"

    ctx = RenderingContext(init_templates=True, app_name="")

    _render_jinja_dir(_SINGLE_FILE_TEMPLATE, _OUTPUT_DIR, ctx)

    _run_ruff(
        "check", "--select", "I", "--fix", "--unsafe-fixes", str(_OUTPUT_DIR.absolute())
    )
    _run_ruff("format", str(_OUTPUT_DIR.absolute()))


@dataclass
class RenderingContext:
    app_name: str
    init_templates: bool


def _render_jinja_dir(
    input_directory: Path, output_directory: Path, ctx: RenderingContext
) -> List[Path]:
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
                    open(path, "r", encoding="utf-8") as input_file,
                    open(
                        output_directory / rendered_name, "w", encoding="utf-8"
                    ) as output_file,
                ):
                    output_file.write(Template(input_file.read()).render(ctx.__dict__))

            else:
                shutil.copy(path, output_directory / rendered_name)

            files_written.append(output_directory / rendered_name)

        elif path.is_dir():
            files_written.extend(
                _render_jinja_dir(path, output_directory / rendered_name, ctx)
            )

    return files_written


def _run_ruff(*options: str) -> None:
    ruff = os.fsdecode(find_ruff_bin())
    subprocess.run([ruff, *options])
