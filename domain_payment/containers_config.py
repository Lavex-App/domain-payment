from abc import ABCMeta
from functools import lru_cache

from environs import Env

from domain_payment.adapters.__factory__ import AdaptersConfig, AdaptersFactory
from domain_payment.adapters.controllers.__dependencies__ import bind_controller_dependencies
from domain_payment.business.__factory__ import BusinessFactory
from domain_payment.frameworks.__factory__ import FrameworksConfig, FrameworksFactory


class Config(metaclass=ABCMeta):
    def __init__(self) -> None:
        self._env = Env(eager=True)
        self._env.read_env()

    @property
    @lru_cache
    def is_local(self) -> bool:
        return self._get_project_env == "local"

    @property
    @lru_cache
    def is_staging(self) -> bool:
        return self._get_project_env in ["dev", "staging"]

    @property
    @lru_cache
    def is_production(self) -> bool:
        return self._get_project_env == "main"

    @property
    @lru_cache
    def _get_project_env(self) -> str:
        return self._env.str("ENV", "main")


class ProjectConfig(Config):
    @property
    @lru_cache
    def frameworks_config(self) -> FrameworksConfig:
        return FrameworksConfig(
            database_uri=self._env.str("DB_URI"),
            service_name=self._env.str("SERVICE_NAME"),
            credentials=self._env.str("GOOGLE_APPLICATION_CREDENTIALS", None),
            auth_app_options={"projectId": self._env.str("PROJECT_ID")},
            client_id=self._env.str("CLIENT_ID"),
            client_secret=self._env.str("CLIENT_SECRET"),
            certificate=self._env.str("CERTIFICATE"),
            sandbox=self.is_local or self.is_staging,
            storage_credentials=self._env.str("GOOGLE_APPLICATION_CREDENTIALS", None),
        )

    @property
    @lru_cache
    def adapters_config(self) -> AdaptersConfig:
        return AdaptersConfig(
            pix_qrcode_bucket_name=self._env.str("PIX_QRCODE_BUCKET_NAME"),
        )


class AppBinding:
    business: BusinessFactory
    adapters: AdaptersFactory
    frameworks: FrameworksFactory

    def __init__(self, frameworks_config: FrameworksConfig, adapters_config: AdaptersConfig) -> None:
        self.frameworks_config = frameworks_config
        self.adapters_config = adapters_config

    def bind_frameworks(self) -> None:
        self.frameworks = FrameworksFactory(self.frameworks_config)

    def bind_adapters(self) -> None:
        self.adapters = AdaptersFactory(self.frameworks, self.adapters_config)

    def bind_business(self) -> None:
        self.business = BusinessFactory(self.adapters)

    def bind_controllers(self) -> None:
        authentication_framework = self.frameworks.authentication_provider()
        bind_controller_dependencies(self.business, authentication_framework)

    def facade(self) -> None:
        self.bind_frameworks()
        self.bind_adapters()
        self.bind_business()
        self.bind_controllers()
