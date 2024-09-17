# SPDX-FileCopyrightText: 2023-present Cody Fincher <cody.fincher@gmail.com>
#
# SPDX-License-Identifier: MIT
from __future__ import annotations

from typing import cast

from rich_click import RichCommand


def run_cli() -> None:
    """Application Entrypoint."""
    import sys

    from litestar_manage.cli import project

    try:
        from litestar.__main__ import run_cli as run_litestar_cli
        from litestar.cli.main import litestar_group

    except ImportError as exc:
        print(  # noqa: T201
            "Could not load required libraries.  ",
            "Please check your installation and make sure you activated any necessary virtual environment",
        )
        print(exc)  # noqa: T201
        sys.exit(1)
    else:
        litestar_group.add_command(cast(RichCommand, project))
        run_litestar_cli()


if __name__ == "__main__":
    run_cli()
