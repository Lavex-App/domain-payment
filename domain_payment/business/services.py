from abc import ABCMeta, abstractmethod

from domain_payment.models import AccountModel, AuthenticatedUserModel, PixChargeResponseModel, PixModel

from .interfaces import Service


class PaymentService(Service, metaclass=ABCMeta):
    @abstractmethod
    async def generate_pix_qrcode(
        self, pix_model: PixModel, user_model: AuthenticatedUserModel
    ) -> PixChargeResponseModel: ...


class AdminService(Service, metaclass=ABCMeta):
    @property
    @abstractmethod
    async def pix_key(self) -> str: ...

    @property
    @abstractmethod
    async def pix_expiration_time(self) -> int: ...

    @property
    @abstractmethod
    async def pix_request_type(self) -> str: ...


class AccountService(Service, metaclass=ABCMeta):
    @abstractmethod
    async def retrieve_user(self, port: AuthenticatedUserModel) -> AccountModel: ...
