from abc import ABCMeta, abstractmethod


class UserUid(str): ...


class BearerToken(str): ...


class AuthenticationProvider(metaclass=ABCMeta):
    @abstractmethod
    def authenticate_by_token(self, token: BearerToken) -> UserUid: ...
