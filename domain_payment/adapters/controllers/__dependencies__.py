from abc import ABCMeta
from typing import Any

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from domain_payment.adapters.interface_adapters.interfaces import AuthenticationProvider, BearerToken
from domain_payment.business.__factory__ import BusinessFactory
from domain_payment.business.use_case import ChargePixUseCase


def bind_controller_dependencies(
    business_factory: BusinessFactory, authentication_service: AuthenticationProvider
) -> None:
    _ControllerDependencyManager(business_factory, authentication_service)


class ControllerDependencyManagerIsNotInitializedException(RuntimeError):
    def __init__(self) -> None:
        self.type = "Dependency Manager"
        self.msg = "Something is trying to use the ControllerDependencyManager without initialize it"
        super().__init__(self.msg)


class _Singleton(type):
    _instances: dict[type, object] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> object:
        if cls not in cls._instances:
            cls._instances[cls] = super(_Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class _ControllerDependencyManager(metaclass=_Singleton):
    def __init__(
        self,
        business_factory: BusinessFactory | None = None,
        authentication_service: AuthenticationProvider | None = None,
    ) -> None:
        if business_factory:
            self.__factory = business_factory
        if authentication_service:
            self.__auth = authentication_service

    def auth_service(self) -> AuthenticationProvider:
        if self.__auth:
            return self.__auth
        raise ControllerDependencyManagerIsNotInitializedException()

    def charge_pix_use_case(self) -> ChargePixUseCase:
        if self.__factory:
            return self.__factory.charge_pix_use_case()
        raise ControllerDependencyManagerIsNotInitializedException()


class _ControllerDependency(metaclass=ABCMeta):
    def __init__(self, credential: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False))) -> None:
        self._dependency_manager = _ControllerDependencyManager()
        auth = self._dependency_manager.auth_service()
        if credential is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Bearer authentication is needed",
                headers={"WWW-Authenticate": 'Bearer realm="auth_required"'},
            )
        bearer_token = BearerToken(credential.credentials)
        self.uid = auth.authenticate_by_token(bearer_token)


class RegisterControllerDependencies(_ControllerDependency):
    def __init__(self, credential: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False))) -> None:
        super().__init__(credential)
        self.charge_pix_use_case: ChargePixUseCase = self._dependency_manager.charge_pix_use_case()
