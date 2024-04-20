from fastapi.applications import FastAPI

from .pix_controller import account_controller


class Binding:
    """Register all controllers by including its routes"""

    def register_all(self, app: FastAPI) -> None:
        app.include_router(account_controller)
