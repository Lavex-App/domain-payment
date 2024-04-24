from contextlib import _AsyncGeneratorContextManager, asynccontextmanager
from typing import AsyncGenerator, Callable

from fastapi import FastAPI

from domain_payment.containers_config import AppBinding, ProjectConfig
from domain_payment.frameworks.__factory__ import FrameworksFactory

LifespanType = Callable[[FastAPI], _AsyncGeneratorContextManager[None]]


def lifespan_dependencies(factory: FrameworksFactory) -> LifespanType:
    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
        await factory.connect()
        yield
        factory.close()

    return lifespan


def simple_app(app_binding: AppBinding) -> FastAPI:
    lifespan = lifespan_dependencies(factory=app_binding.frameworks)
    return FastAPI(lifespan=lifespan)


def register_routes(base_app: FastAPI, app_binding: AppBinding) -> None:
    app_binding.adapters.register_routes(base_app)


def create_app() -> FastAPI:
    project_config = ProjectConfig()
    app_binding = AppBinding(project_config.frameworks_config, project_config.adapters_config)
    app_binding.facade()
    base_app = simple_app(app_binding)
    register_routes(base_app, app_binding)
    return base_app


app = create_app()
