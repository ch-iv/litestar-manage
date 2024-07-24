from __future__ import annotations

import os
from pathlib import Path

from click import group, option
from litestar.cli._utils import LitestarGroup

from litestar_manage.renderer import RenderingContext, render_template


@group(cls=LitestarGroup, name="project")
def project_group() -> None:
    """Manage Scaffolding Tasks."""


@project_group.command(name="init", help="Initialize a new Litestar project.")
@option(
    "--app-name",
    type=str,
    required=True,
)
def init_project(app_name: str) -> None:
    """CLI command to initialize a Litestar project"""
    template_dir = Path(__file__).parent / "template"
    output_dir = Path(os.getcwd())
    ctx = RenderingContext(app_name=app_name)

    render_template(template_dir, output_dir, ctx, run_ruff=True)
