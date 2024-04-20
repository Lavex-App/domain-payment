from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar

ClientT = TypeVar("ClientT")
DatabaseT = TypeVar("DatabaseT")


class DocumentDatabaseService(Generic[ClientT, DatabaseT], metaclass=ABCMeta):
    """A service to give access to database client features."""

    @property
    @abstractmethod
    def client(self) -> ClientT:
        """Return the instantiated MongoDB client."""

    @property
    @abstractmethod
    def database(self) -> DatabaseT:
        """Return the current instance of a Database client."""
