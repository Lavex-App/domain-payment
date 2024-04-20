from abc import ABCMeta
from typing import Generic, TypeVar

from domain_payment.adapters.interfaces.document_database_service import DocumentDatabaseService

T_provider = TypeVar("T_provider", bound=DocumentDatabaseService)


class Repository(Generic[T_provider], metaclass=ABCMeta):
    """A generic interface defining the contract for repositories.

    This interface serves as a blueprint for repositories that interact with various data sources,
    enforcing common patterns and methods.

    Args:
        provider (T_provider): An instance of `DocumentDatabaseService` or its subclass,
            providing access to the underlying data storage.

    Attributes:
        _provider (T_provider): The provider for accessing the data storage.

    """

    def __init__(self, provider: T_provider) -> None:
        """Initialize the Repository with a provider for data access.

        Args:
            provider (T_provider): An instance of `DocumentDatabaseService` or its subclass,
                providing access to the underlying data storage.

        """
        self._provider = provider
