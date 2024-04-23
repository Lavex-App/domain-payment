from typing import Any, NamedTuple

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from domain_payment.business.services import AccountService
from domain_payment.models import AccountModel, AuthenticatedUserModel

from .exceptions import UserNotFound
from .interfaces.document_database_provider import DatabaseName, DocumentDatabaseProvider
from .interfaces.interfaces import InterfaceAdapter
from .interfaces.user_provider import UserProvider

ProviderType = DocumentDatabaseProvider[AsyncIOMotorClient, AsyncIOMotorDatabase]


class AccountProviders(NamedTuple):
    document_database_provider: ProviderType
    user_provider: UserProvider


class AccountAdapter(InterfaceAdapter, AccountService):
    def __init__(self, providers: AccountProviders) -> None:
        database_provider = providers.document_database_provider
        database_provider.database = DatabaseName.ACCOUNT  # type: ignore
        self.__users_collection = database_provider.database["users"]
        self.__user_provider = providers.user_provider

    async def retrieve_user(self, port: AuthenticatedUserModel) -> AccountModel:
        user: dict[str, Any] | None = await self.__users_collection.find_one({"uid": port.uid})
        username = await self.__user_provider.get_username(port)
        if user:
            return AccountModel(**user, username=username)
        raise UserNotFound()
