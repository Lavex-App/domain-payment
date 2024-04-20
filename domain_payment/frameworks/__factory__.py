from typing import TypedDict

from domain_payment.adapters.__factory__ import FrameworksFactoryInterface

from .firebase import FirebaseFrameworkConfig, FirebaseManager
from .mongodb import MotorFrameworkConfig, MotorManager
from .pix_efi import PixFrameworkConfig, PixManager


class FrameworksConfig(FirebaseFrameworkConfig, MotorFrameworkConfig, PixFrameworkConfig):
    """Specification of the configurations required by the Frameworks."""


class FrameworksFactory(FrameworksFactoryInterface[MotorManager]):
    """Responsible for instantiating the Frameworks classes with their linked dependencies.

    This class is responsible for creating instances of framework classes with their required dependencies,
    particularly for interacting with MongoDB using Motor.

    Args:
        config (FrameworksConfig): A dictionary containing configuration parameters for the framework.
    """

    def __init__(self, config: FrameworksConfig) -> None:
        """Initialize the FrameworksFactory with the provided configuration.

        Args:
            config (FrameworksConfig): A dictionary containing configuration parameters for the frameworks.
        """
        self.__config = config
        self.__manager = MotorManager(config)

    async def connect(self) -> None:
        """Connect to the MongoDB database asynchronously."""
        await self.__manager.connect()

    def close(self) -> None:
        """Close the connection to the MongoDB database."""
        self.__manager.close()

    def database_framework(self) -> MotorManager:
        """Get the MotorManager instance representing the MongoDB database framework.

        Returns:
            MotorManager: An instance of MotorManager representing the MongoDB database framework.
        """
        return self.__manager

    def authentication_framework(self) -> FirebaseManager:
        """Get the FirebaseManager instance representing the Firebase authentication framework.

        Returns:
            FirebaseManager: An instance of FirebaseManager representing the Firebase authentication framework.
        """
        return FirebaseManager(self.__config)

    def pix_framework(self) -> FirebaseManager:
        """Get the PixManager instance representing the Pix framework.

        Returns:
            PixManager: An instance of PixManager representing the Pix framework.
        """
        return FirebaseManager(self.__config)
