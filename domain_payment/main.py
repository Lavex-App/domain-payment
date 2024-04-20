# noinspection PyProtectedMember
from contextlib import _AsyncGeneratorContextManager, asynccontextmanager
from typing import AsyncGenerator, Callable

from environs import Env
from fastapi import FastAPI

from domain_payment.adapters.__factory__ import AdaptersFactory
from domain_payment.adapters.controllers.__dependencies__ import bind_controller_dependencies
from domain_payment.business.__factory__ import BusinessFactory
from domain_payment.frameworks.__factory__ import FrameworksConfig, FrameworksFactory

LifespanType = Callable[[FastAPI], _AsyncGeneratorContextManager[None]]


def lifespan_dependencies(factory: FrameworksFactory) -> LifespanType:
    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
        await factory.connect()
        yield
        factory.close()

    return lifespan


def configs() -> FrameworksConfig:
    env = Env(eager=True)
    env.read_env()
    return FrameworksConfig(
        database_name=env.str("DB_NAME"),
        database_uri=env.str("DB_URI"),
        service_name=env.str("SERVICE_NAME"),
        credentials=env.str("GOOGLE_APPLICATION_CREDENTIALS", None),
        auth_app_options={"projectId": env.str("PROJECT_ID")},
        client_id=env.str("CLIENT_ID"),
        client_secret=env.str("CLIENT_SECRET"),
        certificate=env.str("CERTIFICATE"),
        sandbox=env.bool("SANDBOX"),
    )


class AppBinding:
    """Bind all dependency inversion of the project"""
    business: BusinessFactory
    adapters: AdaptersFactory
    frameworks: FrameworksFactory

    def __init__(self, config: FrameworksConfig) -> None:
        self.config = config

    def bind_frameworks(self) -> None:
        self.frameworks = FrameworksFactory(self.config)

    def bind_adapters(self) -> None:
        self.adapters = AdaptersFactory(self.frameworks)

    def bind_business(self) -> None:
        self.business = BusinessFactory(self.adapters)

    def bind_controllers(self) -> None:
        authentication_framework = self.frameworks.authentication_framework()
        bind_controller_dependencies(self.business, authentication_framework)

    def facade(self) -> None:
        self.bind_frameworks()
        self.bind_adapters()
        self.bind_business()
        self.bind_controllers()


def simple_app(app_binding: AppBinding) -> FastAPI:
    lifespan = lifespan_dependencies(factory=app_binding.frameworks)
    return FastAPI(lifespan=lifespan)


def register_routes(base_app: FastAPI, app_binding: AppBinding) -> None:
    app_binding.adapters.register_routes(base_app)


def create_app() -> FastAPI:
    config = configs()
    app_binding = AppBinding(config)
    app_binding.facade()
    base_app = simple_app(app_binding)
    register_routes(base_app, app_binding)
    return base_app


app = create_app()
