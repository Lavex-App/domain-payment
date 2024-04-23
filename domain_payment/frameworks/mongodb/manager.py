import logging
from typing import TypedDict

import certifi
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.errors import ConnectionFailure

from domain_payment.adapters.interface_adapters.interfaces import DatabaseName, DocumentDatabaseProvider


class MotorFrameworkConfig(TypedDict):
    database_uri: str
    service_name: str


class MotorManager(DocumentDatabaseProvider[AsyncIOMotorClient, AsyncIOMotorDatabase]):
    _database_name: str

    def __init__(self, config: MotorFrameworkConfig) -> None:
        self._logger = logging.getLogger(f"{self.__class__.__name__}")
        self._service_name = config["service_name"]
        self._database_uri = config["database_uri"]
        self._client: AsyncIOMotorClient | None = None

    async def connect(self) -> None:
        self.close()
        try:
            ca = certifi.where()
            self._client = AsyncIOMotorClient(self._database_uri, appname=self._service_name, tls=True, tlsCAFile=ca)
            await self._client.admin.command("ping")
        except ConnectionFailure:  # pragma: no cover
            self._logger.info("Server [%s] not available!", self._database_uri)
        else:
            self._logger.info("Connected to MongoDB")

    def close(self) -> None:
        if self._client is None:
            return
        self._client.close()
        self._logger.info("Closed MongoDB connection.")

    @property
    def client(self) -> AsyncIOMotorClient:
        if self._client is None:
            raise ValueError("There is no MongoDB client.")
        return self._client

    @property
    def database(self) -> AsyncIOMotorDatabase:
        return self.client[self._database_name]

    @database.setter
    def database(self, database_name: DatabaseName) -> None:
        self._database_name = database_name.value
