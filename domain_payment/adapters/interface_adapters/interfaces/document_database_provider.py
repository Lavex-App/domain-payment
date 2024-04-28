from abc import ABCMeta, abstractmethod
from enum import UNIQUE, Enum, verify
from typing import Generic, TypeVar

ClientT = TypeVar("ClientT")
DatabaseT = TypeVar("DatabaseT")


@verify(UNIQUE)
class DatabaseName(Enum):
    ACCOUNT = "domain-account"
    ADMIN = "configuration"


class DocumentDatabaseProvider(Generic[ClientT, DatabaseT], metaclass=ABCMeta):
    @property
    @abstractmethod
    def client(self) -> ClientT: ...

    @property
    @abstractmethod
    def database(self) -> DatabaseT: ...

    @database.setter
    @abstractmethod
    def database(self, database_name: DatabaseName) -> None: ...
