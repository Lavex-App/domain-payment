from abc import ABCMeta, abstractmethod
from typing import Any

from domain_payment.models import PixChargeModel, PixModel


class _ABCMetaSingleton(ABCMeta):
    _instances: dict[type, object] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> object:
        if cls not in cls._instances:
            cls._instances[cls] = super(_ABCMetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class PixProvider(metaclass=_ABCMetaSingleton):
    @abstractmethod
    async def create_charge(self, pix_model: PixModel) -> PixChargeModel: ...
