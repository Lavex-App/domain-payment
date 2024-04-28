from abc import ABCMeta, abstractmethod

from domain_payment.models import AuthenticatedUserModel, PixChargeModel, PixModel


class PixProvider(metaclass=ABCMeta):
    @abstractmethod
    async def create_charge(self, pix_model: PixModel, user_model: AuthenticatedUserModel) -> PixChargeModel: ...
