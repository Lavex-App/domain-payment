import logging
from typing import TypedDict

import certifi
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.errors import ConnectionFailure

from domain_payment.adapters.interfaces import DocumentDatabaseService


class MotorFrameworkConfig(TypedDict):
    """Specification of the configurations required by the Motor framework."""

    database_name: str
    database_uri: str
    service_name: str


class MotorManager(DocumentDatabaseService[AsyncIOMotorClient, AsyncIOMotorDatabase]):
    """Manager for Motor (Async MongoDB Client).

    This class manages connections to a MongoDB database using the Motor asynchronous client.

    Args:
        config (MotorFrameworkConfig): Configuration object with the following attributes:
            service_name (str): The name of the service using the MotorManager.
            database_name (str): The name of the MongoDB database.
            database_uri (str): The URI of the MongoDB instance.

    Attributes:
        _logger (Logger): An instance of the logger for logging messages.
        _service_name (str): The name of the service using the MotorManager.
        _database_name (str): The name of the MongoDB database.
        _database_uri (str): The URI of the MongoDB instance.
        _client (AsyncIOMotorClient | None): The Motor asynchronous client instance.
    """

    def __init__(self, config: MotorFrameworkConfig) -> None:
        """Initialize the MotorManager with the provided parameters."""
        self._logger = logging.getLogger(f"{self.__class__.__name__}")
        self._service_name = config["service_name"]
        self._database_name = config["database_name"]
        self._database_uri = config["database_uri"]
        self._client: AsyncIOMotorClient | None = None

    async def connect(self) -> None:
        """Connect to a MongoDB cluster asynchronously.

        Raises:
            ConnectionFailure: If a connection to the MongoDB cluster cannot be established.

        """
        self.close()
        try:
            # ca = certifi.where()
            # self._client = AsyncIOMotorClient(self._database_uri, appname=self._service_name, tls=True, tlsCAFile=ca)
            self._client = AsyncIOMotorClient(self._database_uri, appname=self._service_name)
            await self._client.admin.command("ping")
        except ConnectionFailure:  # pragma: no cover
            self._logger.info("Server [%s] not available!", self._database_uri)
        else:
            self._logger.info("Connected to MongoDB [%s].", self._database_name)

    def close(self) -> None:
        """Close the current database connection."""
        if self._client is None:
            return
        self._client.close()
        self._logger.info("Closed MongoDB connection.")

    @property
    def client(self) -> AsyncIOMotorClient:
        """Return the instantiated MongoDB client.

        Returns:
            AsyncIOMotorClient: The instantiated MongoDB client.

        Raises:
            ValueError: If there is no MongoDB client instantiated.

        """
        if self._client is None:
            raise ValueError("There is no MongoDB client.")
        return self._client

    @property
    def database(self) -> AsyncIOMotorDatabase:
        """Return the current instance of a Database client based on the provided database name.

        Returns:
            AsyncIOMotorDatabase: The current instance of a Database client.

        """
        return self.client[self._database_name]
