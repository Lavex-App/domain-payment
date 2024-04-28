from abc import ABCMeta, abstractmethod

from domain_payment.models.user_model import AuthenticatedUserModel


class UserProvider(metaclass=ABCMeta):
    @abstractmethod
    async def get_username(self, user: AuthenticatedUserModel) -> str: ...
