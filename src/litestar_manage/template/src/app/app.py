from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from litestar import Litestar


def create_app() -> Litestar:
    """Create ASGI application."""
    from os import urandom

    from litestar import Litestar
    from litestar.contrib.jinja import JinjaTemplateEngine
    from litestar.logging.config import LoggingConfig
    from litestar.middleware.logging import LoggingMiddlewareConfig
    from litestar.middleware.session.client_side import CookieBackendConfig
    from litestar.static_files import create_static_files_router
    from litestar.template.config import TemplateConfig

    from app.config import assets_path, templates_path
    from app.controllers.web import WebController

    logging_middleware_config = LoggingMiddlewareConfig()
    session_config = CookieBackendConfig(secret=urandom(16))  # type: ignore

    return Litestar(
        route_handlers=[
            WebController,
            create_static_files_router(path="/static", directories=[assets_path]),
        ],
        middleware=[session_config.middleware, logging_middleware_config.middleware],
        template_config=TemplateConfig(
            directory=templates_path,
            engine=JinjaTemplateEngine,
        ),
        logging_config=LoggingConfig(),
    )


app = create_app()
