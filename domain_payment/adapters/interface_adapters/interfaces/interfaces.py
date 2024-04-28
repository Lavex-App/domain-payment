from abc import ABCMeta, abstractmethod

from .authentication_provider import AuthenticationProvider
from .document_database_provider import DocumentDatabaseProvider
from .user_provider import UserProvider


class InterfaceAdapter(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, *providers: DocumentDatabaseProvider | AuthenticationProvider | UserProvider) -> None: ...
