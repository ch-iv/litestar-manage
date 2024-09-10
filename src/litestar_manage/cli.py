from __future__ import annotations

from pathlib import Path

import click
from click import group, option
from litestar.cli._utils import LitestarGroup

from litestar_manage.constants import VENV_NAME
from litestar_manage.renderer import RenderingContext, render_template
from litestar_manage.venv_builder import PipVenvBuilder, init_venv


def is_project_initialized() -> bool:
    output_dir = Path.cwd()
    return (output_dir / "src").exists() or (output_dir / "venv").exists()


@click.group(cls=LitestarGroup)
def project():
    pass


@project.command(name="new", help="Initialize a new Litestar project.")
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

    template_dir = Path(__file__).parent / "templates" / "app"
    output_dir = Path.cwd()

    if is_project_initialized():
        click.echo("Project already initialized.")
        return

    ctx = RenderingContext(app_name=app_name)
    render_template(template_dir, output_dir, ctx, run_ruff=True)

    packages_to_install = ["litestar"]
    if venv == "pip":
        builder = PipVenvBuilder()
        init_venv(output_dir / VENV_NAME, builder, packages_to_install)


@project.command(name="resource")
@option(
    "--resource-name",
    "-n",
    type=str,
    required=True,
)
def generate_resource(resource_name: str) -> None:
    """CLI command to generate a new resource (controller, service, dto, models, repository)"""

    if not is_project_initialized():
        click.echo("Project not initialized. Please initialize the project first.")
        return

    template_dir = Path(__file__).parent / "templates" / "resource"
    output_dir = Path.cwd() / "src" / f"{resource_name.lower()}"
    ctx = RenderingContext(app_name=resource_name)

    render_template(template_dir, output_dir, ctx, run_ruff=True)
