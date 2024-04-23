from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar

from domain_payment.business.interfaces import InputPort, OutputPort, Service

T_input = TypeVar("T_input", bound=InputPort)
T_output_co = TypeVar("T_output_co", bound=OutputPort, covariant=True)


class UseCase(Generic[T_input, T_output_co], metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, *service: Service) -> None: ...

    @abstractmethod
    async def __call__(self, input_port: T_input) -> T_output_co: ...
