from functools import lru_cache

import aiohttp

from domain_payment.adapters.__factory__ import FrameworksFactoryInterface

from .firebase import FirebaseFrameworkConfig, FirebaseManager
from .gcp_storage import GCPStorageFrameworkConfig, GCPStorageManager
from .mongodb import MotorFrameworkConfig, MotorManager
from .pix_efi import PixFrameworkConfig, PixManager


class FrameworksConfig:
    def __init__(
        self,
        firebase_framework_config: FirebaseFrameworkConfig,
        motor_framework_config: MotorFrameworkConfig,
        gcp_storage_framework_config: GCPStorageFrameworkConfig,
        pix_framework_config: PixFrameworkConfig,
    ) -> None:
        self.firebase_framework_config = firebase_framework_config
        self.motor_framework_config = motor_framework_config
        self.gcp_storage_framework_config = gcp_storage_framework_config
        self.pix_framework_config = pix_framework_config


class FrameworksFactory(
    FrameworksFactoryInterface[
        MotorManager,
        GCPStorageManager,
        FirebaseManager,
        FirebaseManager,
        PixManager,
    ]
):
    __session: aiohttp.ClientSession

    def __init__(self, config: FrameworksConfig) -> None:
        self.__config = config
        self.__manager = MotorManager(config.motor_framework_config)

    async def connect(self) -> None:
        await self.__manager.connect()
        self.__session = aiohttp.ClientSession()

    async def close(self) -> None:
        self.__manager.close()
        await self.__session.close()

    def database_provider(self) -> MotorManager:
        return self.__manager

    def bucket_provider(self) -> GCPStorageManager:
        return GCPStorageManager(self.__config.gcp_storage_framework_config, self.__session)

    def authentication_provider(self) -> FirebaseManager:
        return self.__firebase_manager

    def user_provider(self) -> FirebaseManager:
        return self.__firebase_manager

    def pix_provider(self) -> PixManager:
        return PixManager(self.__config.pix_framework_config)

    @property
    @lru_cache
    def __firebase_manager(self) -> FirebaseManager:
        return FirebaseManager(self.__config.firebase_framework_config)
