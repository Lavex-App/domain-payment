from abc import ABCMeta
from functools import lru_cache

from environs import Env

from domain_payment.adapters.__factory__ import AdaptersConfig, AdaptersFactory
from domain_payment.adapters.controllers.__dependencies__ import bind_controller_dependencies
from domain_payment.business.__factory__ import BusinessFactory
from domain_payment.frameworks.__factory__ import FrameworksConfig, FrameworksFactory
from domain_payment.frameworks.firebase import FirebaseFrameworkConfig
from domain_payment.frameworks.gcp_storage import GCPStorageFrameworkConfig
from domain_payment.frameworks.mongodb import MotorFrameworkConfig
from domain_payment.frameworks.pix_efi import PixFrameworkConfig


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
            motor_framework_config=self.__motor_framework_config,
            firebase_framework_config=self.__firebase_framework_config,
            pix_framework_config=self.__pix_framework_config,
            gcp_storage_framework_config=self.__gcp_storage_framework_config,
        )

    @property
    @lru_cache
    def adapters_config(self) -> AdaptersConfig:
        return AdaptersConfig(
            pix_qrcode_bucket_name=self._env.str("PIX_QRCODE_BUCKET_NAME"),
        )

    @property
    @lru_cache
    def __motor_framework_config(self) -> MotorFrameworkConfig:
        return MotorFrameworkConfig(
            database_uri=self._env.str("DB_URI"),
            service_name=self._env.str("SERVICE_NAME"),
            sandbox=self.is_local or self.is_staging,
        )

    @property
    @lru_cache
    def __firebase_framework_config(self) -> FirebaseFrameworkConfig:
        return FirebaseFrameworkConfig(
            credentials=self._env.str("GOOGLE_APPLICATION_CREDENTIALS", None),
            auth_app_options={"projectId": self._env.str("PROJECT_ID")},
        )

    @property
    @lru_cache
    def __pix_framework_config(self) -> PixFrameworkConfig:
        return PixFrameworkConfig(
            project_id=self._env.str("PROJECT_ID"),
            service_tag=self._env.str("SERVICE_TAG"),
            env=self._get_project_env,
            credentials=self._env.str("GOOGLE_APPLICATION_CREDENTIALS", None),
            client_id=self._env.str("CLIENT_ID"),
            client_secret=self._env.str("CLIENT_SECRET"),
            sandbox=self.is_local or self.is_staging,
        )

    @property
    @lru_cache
    def __gcp_storage_framework_config(self) -> GCPStorageFrameworkConfig:
        return GCPStorageFrameworkConfig(
            storage_credentials=self._env.str("GOOGLE_APPLICATION_CREDENTIALS", None),
            service_account_email=self._env.str("SERVICE_ACCOUNT_EMAIL"),
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
