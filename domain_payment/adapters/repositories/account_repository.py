from typing import Any

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from domain_payment.adapters.interfaces.document_database_service import DocumentDatabaseService
from domain_payment.business.ports import (
    RegisterInputPort,
    RetrieveUserInputPort,
    UpdateAddressInputPort,
    UpdateCpfInputPort,
)
from domain_payment.business.services import AccountService
from domain_payment.models import User

from .exceptions import UserNotFound
from .interfaces import Repository

ProviderType = DocumentDatabaseService[AsyncIOMotorClient, AsyncIOMotorDatabase]


class AccountRepository(
    Repository[DocumentDatabaseService[AsyncIOMotorClient, AsyncIOMotorDatabase]],
    AccountService,
):
    """A repository class responsible for interacting with a document database to manage user accounts.

    This class extends `Repository`, which defines the basic repository interface, and `AccountService`,
    which provides business logic for account-related operations.

    Args:
        provider (ProviderType): An instance of `DocumentDatabaseService` providing access to the document database.

    Attributes:
        _provider (ProviderType): The provider for accessing the document database.
        __users_collection: Collection in the document database where user records are stored.

    Methods:
        register(port): Registers a new user account in the database.
        get_user(port): Retrieves a user from the database by UID.
        update_address(port): Updates a user's address in the database.
        update_cpf(port): Updates a user's CPF in the database.
    """

    def __init__(self, provider: ProviderType) -> None:
        """Initialize the AccountRepository with a document database provider."""
        super().__init__(provider)
        self.__users_collection = self._provider.database["users"]

    async def register(self, port: RegisterInputPort) -> None:
        """Register a new user account in the database.

        Args:
            port (RegisterInputPort): The input port containing user account information.
        """
        await self.__users_collection.insert_one(port.model_dump())

    async def get_user(self, port: RetrieveUserInputPort) -> User:
        """Retrieve a user from the database by UID.

        Args:
            port (RetrieveUserInputPort): The input port containing the UID of the user to retrieve.

        Returns:
            User: The user retrieved from the database.

        Raises:
            UserNotFound: If no user is found with the provided UID.
        """
        user: dict[str, Any] | None = await self.__users_collection.find_one({"uid": port.uid})
        if user:
            return User(**user)
        raise UserNotFound()

    async def update_address(self, port: UpdateAddressInputPort) -> None:
        """Update a user's address in the database.

        Args:
            port (UpdateAddressInputPort): The input port containing the UID and updated address information.
        """
        update = port.model_dump()
        uid = update.pop("uid")
        await self.__users_collection.update_one({"uid": uid}, {"$set": {"address": update}})

    async def update_cpf(self, port: UpdateCpfInputPort) -> None:
        """Update a user's CPF in the database.

        Args:
            port (UpdateCpfInputPort): The input port containing the UID and updated CPF information.
        """
        await self.__users_collection.update_one({"uid": port.uid}, {"$set": {"cpf": port.cpf}})
