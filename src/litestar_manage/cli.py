from __future__ import annotations

from pathlib import Path

import click
from click import group, option
from litestar.cli._utils import LitestarGroup

from litestar_manage.renderer import RenderingContext, render_template
from litestar_manage.venv_builder import PipVenvBuilder, init_venv


@group(cls=LitestarGroup, name="project")
def project_group() -> None:
    """Manage Scaffolding Tasks."""


@project_group.command(name="init", help="Initialize a new Litestar project.")
@option(
    "--app-name",
    type=str,
    required=True,
)
@option(
    "--venv",
    "-v",
    required=False,
    default=None,
    type=click.Choice(["pip"]),
)
def init_project(app_name: str, venv: str | None) -> None:
    """CLI command to initialize a Litestar project"""

    template_dir = Path(__file__).parent / "template"
    output_dir = Path.cwd()
    ctx = RenderingContext(app_name=app_name)

    render_template(template_dir, output_dir, ctx, run_ruff=True)

    packages_to_install = ["litestar"]
    venv_name = "venv"
    if venv == "pip":
        builder = PipVenvBuilder()
        init_venv(output_dir / venv_name, builder, packages_to_install)
