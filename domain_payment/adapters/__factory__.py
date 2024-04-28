from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar

from fastapi import FastAPI

from domain_payment.business.__factory__ import AdaptersFactoryInterface

from .controllers.__binding__ import Binding
from .interface_adapters import (
    AccountAdapter,
    AccountProviders,
    AdminAdapter,
    AdminProviders,
    PaymentAdapter,
    PaymentAdapterConfig,
    PaymentProviders,
)
from .interface_adapters.interfaces import (
    AuthenticationProvider,
    BucketProvider,
    DocumentDatabaseProvider,
    PixProvider,
    UserProvider,
)

T_database_co = TypeVar("T_database_co", bound=DocumentDatabaseProvider, covariant=True)
T_bucket_co = TypeVar("T_bucket_co", bound=BucketProvider, covariant=True)
T_authentication_co = TypeVar("T_authentication_co", bound=AuthenticationProvider, covariant=True)
T_user_co = TypeVar("T_user_co", bound=UserProvider, covariant=True)
T_pix_provider_co = TypeVar("T_pix_provider_co", bound=PixProvider, covariant=True)


class FrameworksFactoryInterface(
    Generic[T_database_co, T_bucket_co, T_authentication_co, T_user_co, T_pix_provider_co],
    metaclass=ABCMeta,
):
    @abstractmethod
    def database_provider(self) -> T_database_co: ...

    @abstractmethod
    def bucket_provider(self) -> T_bucket_co: ...

    @abstractmethod
    def authentication_provider(self) -> T_authentication_co: ...

    @abstractmethod
    def user_provider(self) -> T_user_co: ...

    @abstractmethod
    def pix_provider(self) -> T_pix_provider_co: ...


class AdaptersConfig(PaymentAdapterConfig): ...


class AdaptersFactory(AdaptersFactoryInterface[PaymentAdapter, AccountAdapter, AdminAdapter]):
    def __init__(self, frameworks_factory: FrameworksFactoryInterface, config: AdaptersConfig) -> None:
        self.__factory = frameworks_factory
        self.__config = config

    def admin_service(self) -> AdminAdapter:
        admin_providers = AdminProviders(document_database_provider=self.__factory.database_provider())
        return AdminAdapter(admin_providers)

    def account_service(self) -> AccountAdapter:
        account_providers = AccountProviders(
            document_database_provider=self.__factory.database_provider(),
            user_provider=self.__factory.user_provider(),
        )
        return AccountAdapter(account_providers)

    def payment_service(self) -> PaymentAdapter:
        payment_providers = PaymentProviders(
            pix_provider=self.__factory.pix_provider(),
            bucket_provider=self.__factory.bucket_provider(),
        )
        return PaymentAdapter(payment_providers, self.__config)

    @staticmethod
    def register_routes(app: FastAPI) -> None:
        Binding().register_all(app)
