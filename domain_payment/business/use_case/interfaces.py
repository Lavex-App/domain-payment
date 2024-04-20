from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar

from domain_payment.business.interfaces import InputPort, OutputPort, Service

T_input = TypeVar("T_input", bound=InputPort)
T_output_co = TypeVar("T_output_co", bound=OutputPort, covariant=True)


class UseCase(Generic[T_input, T_output_co], metaclass=ABCMeta):
    """
    A generic class representing a use case in the business logic layer.

    This class defines the base interface for implementing use cases in the application. Use cases are responsible
    for executing specific business rules or logic. They typically receive input data, perform some processing,
    and produce output data.

    Args:
        *service (Service): The service object(s) implemented in Frameworks layer required by the use case to execute its logic.

    Methods:
        __init__(self, service: T_service) -> None: Constructor method for initializing the use case with the required service(s).
        __call__(self, input_port: T_input) -> T_output_co: Method for executing the use case logic with the provided input data.
    """  # noqa: E501

    @abstractmethod
    def __init__(self, *service: Service) -> None:
        """
        Initialize the use case with the required service(s).

        Args:
            *service (Service): The service object(s) required by the use case to execute its logic.
        """

    @abstractmethod
    async def __call__(self, input_port: T_input) -> T_output_co:
        """
        Execute the use case logic with the provided input data.

        This method is responsible for executing the business logic associated with the use case.
        It receives input data via an input port, performs processing, and returns output data
        via an output port.

        Args:
            input_port (T_input): The input port containing the input data required by the use case.

        Returns:
            T_output_co: The output port containing the result of the use case execution.
        """
