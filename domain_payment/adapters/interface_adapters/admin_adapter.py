from typing import NamedTuple

from async_property import async_cached_property
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from domain_payment.business.services import AdminService

from .exceptions import AdminIsNotProperlyConfigured
from .interfaces.document_database_provider import DatabaseName, DocumentDatabaseProvider
from .interfaces.interfaces import InterfaceAdapter

ProviderType = DocumentDatabaseProvider[AsyncIOMotorClient, AsyncIOMotorDatabase]


class AdminProviders(NamedTuple):
    document_database_provider: ProviderType


class AdminAdapter(InterfaceAdapter, AdminService):
    def __init__(self, providers: AdminProviders) -> None:
        database_provider = providers.document_database_provider
        database_provider.database = DatabaseName.ADMIN  # type: ignore
        self.__admin_collection = database_provider.database["payment"]

    @async_cached_property
    async def pix_key(self) -> str:
        admin: dict[str, str] | None = await self.__admin_collection.find().next()
        if admin:
            return admin["pix_key"]
        raise AdminIsNotProperlyConfigured()

    @async_cached_property
    async def pix_request_type(self) -> str:
        admin: dict[str, dict[str, str]] | None = await self.__admin_collection.find().next()
        if admin:
            payment_request_types = admin["payment_request_types"]
            return payment_request_types["pix_service_payment"]
        raise AdminIsNotProperlyConfigured()

    @async_cached_property
    async def pix_expiration_time(self) -> int:
        admin: dict[str, str] | None = await self.__admin_collection.find().next()
        if admin:
            return int(admin["pix_expiration_time"])
        raise AdminIsNotProperlyConfigured()
