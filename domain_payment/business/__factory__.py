from abc import ABCMeta, abstractmethod
from typing import Generic

from typing_extensions import TypeVar

from domain_payment.business.use_case import ChargePixUseCase

from .services import PixService

T_pix_service_co = TypeVar("T_pix_service_co", bound=PixService, covariant=True)


class AdaptersFactoryInterface(Generic[T_pix_service_co], metaclass=ABCMeta):
    """Interface for the Adapters Factory according to the Business layer needs.

    This interface defines the contract for a factory that provides adapter services,
    such as pix management, to the business layer.

    """

    @abstractmethod
    def account_service(self) -> T_pix_service_co:
        """Abstract method to retrieve the pix service instance."""


class BusinessFactory:
    """
    Responsible for instantiating the Business classes with their linked dependencies.

    This class is responsible for creating instances of business classes with their required dependencies,
    particularly for the account-related use cases.

    Args:
        adapters_factory (AdaptersFactoryInterface): An instance of a factory implementing the
            `AdaptersFactoryInterface`, providing access to the necessary adapter services.

    Methods:
        example_use_case(): Instantiate and return a ExampleUseCase with the configured pix service.
    """

    def __init__(self, adapters_factory: AdaptersFactoryInterface) -> None:
        """Initialize the BusinessFactory with the provided adapters factory.

        Args:
            adapters_factory (AdaptersFactoryInterface): An instance of a factory implementing the
                `AdaptersFactoryInterface`.

        """
        self.__factory = adapters_factory

    def charge_pix_use_case(self) -> ChargePixUseCase:
        """Instantiate and return a ChargePixUseCase with the configured pix service.

        Returns:
            ExampleUseCase: An instance of ChargePixUseCase with the configured pix service.

        """
        return ChargePixUseCase(service=self.__pix_service)

    @property
    def __pix_service(self) -> PixService:
        """
        Retrieve the pix service instance.

        Returns:
            PixService: An instance of the pix service.
        """
        return self.__factory.account_service()
