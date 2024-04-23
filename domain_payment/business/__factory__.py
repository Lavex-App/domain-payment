from abc import ABCMeta, abstractmethod
from typing import Generic

from typing_extensions import TypeVar

from domain_payment.business.use_case import ChargePixServices, ChargePixUseCase

from .services import AccountService, AdminService, PaymentService

T_payment_service_co = TypeVar("T_payment_service_co", bound=PaymentService, covariant=True)
T_account_service_co = TypeVar("T_account_service_co", bound=AccountService, covariant=True)
T_admin_service_co = TypeVar("T_admin_service_co", bound=AdminService, covariant=True)


# noinspection PyTypeHints
class AdaptersFactoryInterface(
    Generic[T_payment_service_co, T_account_service_co, T_admin_service_co],
    metaclass=ABCMeta,
):
    @abstractmethod
    def admin_service(self) -> T_admin_service_co: ...

    @abstractmethod
    def account_service(self) -> T_account_service_co: ...

    @abstractmethod
    def payment_service(self) -> T_payment_service_co: ...


class BusinessFactory:
    def __init__(self, adapters_factory: AdaptersFactoryInterface) -> None:
        self.__factory = adapters_factory

    def charge_pix_use_case(self) -> ChargePixUseCase:
        services = ChargePixServices(
            payment_service=self.__factory.payment_service(),
            admin_service=self.__factory.admin_service(),
            account_service=self.__factory.account_service(),
        )
        return ChargePixUseCase(services)
