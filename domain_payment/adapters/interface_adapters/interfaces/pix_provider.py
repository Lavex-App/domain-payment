from abc import ABCMeta, abstractmethod

from domain_payment.models import PixChargeModel, PixModel


class PixProvider(metaclass=ABCMeta):
    @abstractmethod
    async def create_charge(self, pix_model: PixModel) -> PixChargeModel: ...
