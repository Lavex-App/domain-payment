from functools import lru_cache

from environs import Env

from domain_payment.adapters.__factory__ import AdaptersConfig, AdaptersFactory
from domain_payment.adapters.controllers.__dependencies__ import bind_controller_dependencies
from domain_payment.business.__factory__ import BusinessFactory
from domain_payment.frameworks.__factory__ import FrameworksConfig, FrameworksFactory


class ProjectConfig:
    def __init__(self) -> None:
        self.__env = Env(eager=True)
        self.__env.read_env()

    @property
    @lru_cache
    def frameworks_config(self) -> FrameworksConfig:
        return FrameworksConfig(
            database_uri=self.__env.str("DB_URI"),
            service_name=self.__env.str("SERVICE_NAME"),
            credentials=self.__env.str("GOOGLE_APPLICATION_CREDENTIALS", None),
            auth_app_options={"projectId": self.__env.str("PROJECT_ID")},
            client_id=self.__env.str("CLIENT_ID"),
            client_secret=self.__env.str("CLIENT_SECRET"),
            certificate=self.__env.str("CERTIFICATE"),
            sandbox=self.__env.bool("ENV"),
            storage_credentials=self.__env.str("GOOGLE_APPLICATION_CREDENTIALS", None),
        )

    @property
    @lru_cache
    def adapters_config(self) -> AdaptersConfig:
        return AdaptersConfig(
            pix_qrcode_bucket_name=self.__env.str("PIX_QRCODE_BUCKET_NAME"),
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
