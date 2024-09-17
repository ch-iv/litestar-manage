from typing import Dict


class AppService:
    """App Service"""

    app_name = ""
    app_version = "0.1.0"

    async def app_info(self) -> Dict[str, str]:
        """Return info about the app"""
        return {"app_name": self.app_name, "verion": self.app_version}


def provide_app_service():
    return AppService()
