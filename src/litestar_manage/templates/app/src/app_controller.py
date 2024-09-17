from typing import Dict

from litestar import Controller, get
from litestar.di import Provide
from litestar.enums import MediaType
from litestar.status_codes import HTTP_200_OK
from src.app_service import AppService, provide_app_service


class AppController(Controller):
    """App controller."""

    dependencies = {"app_service": Provide(provide_app_service)}

    @get(path="/", status_code=HTTP_200_OK, media_type=MediaType.JSON)
    async def index(self, app_service: AppService) -> Dict:
        """App index"""
        return await app_service.app_info()
