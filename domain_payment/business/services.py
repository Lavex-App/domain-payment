from abc import ABCMeta, abstractmethod

from domain_payment.models import AccountModel, AuthenticatedUserModel, PixModel

from .interfaces import Service


class PixService(Service, metaclass=ABCMeta):
    """A service providing access to features outside Business Layer.

    Methods:
        register(port): Register a new user.
    """

    @abstractmethod
    def generate_pix_qrcode(self, port: PixModel) -> None:
        """Register a new user.

        Args:
            port (PixModel): The input port containing user account information.
        """


class AdminService(Service, metaclass=ABCMeta):
    @abstractmethod
    async def pix_key(self) -> str:
        """"""

    @abstractmethod
    async def pix_expiration_time(self) -> str:
        """"""

    @abstractmethod
    async def pix_request_type(self) -> str:
        """"""


class AccountService(Service, metaclass=ABCMeta):
    @abstractmethod
    async def retrieve_user(self, port: AuthenticatedUserModel) -> AccountModel:
        """"""
