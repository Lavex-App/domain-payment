from abc import ABCMeta
from typing import Any

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from domain_payment.adapters.interfaces.authentication_service import AuthenticationService, BearerToken
from domain_payment.business.__factory__ import BusinessFactory
from domain_payment.business.use_case import ChargePixUseCase


def bind_controller_dependencies(
    business_factory: BusinessFactory, authentication_service: AuthenticationService
) -> None:
    """Bind controller dependencies to the provided business factory and authentication service.

    This function binds the provided business factory and authentication service to the controller dependencies.

    Args:
        business_factory (BusinessFactory): An instance of the BusinessFactory class providing business use cases.
        authentication_service (AuthenticationService): An instance of the AuthenticationService class for authentication.

    """  # noqa: E501
    _ControllerDependencyManager(business_factory, authentication_service)


class ControllerDependencyManagerIsNotInitializedException(RuntimeError):
    """Raised when the Controller Dependency Manager is used but has not been initialized

    Attributes:
        type (str): The type of the exception.
        msg (str): The message describing the exception.
    """

    def __init__(self) -> None:
        """Initialize the exception with a default message."""
        self.type = "Dependency Manager"
        self.msg = "Something is trying to use the ControllerDependencyManager without initialize it"
        super().__init__(self.msg)


class _Singleton(type):
    """Singleton pattern created to be used by ControllerDependencyManager"""

    _instances: dict[type, object] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> object:
        """Implement the __call__ method for the Singleton pattern."""
        if cls not in cls._instances:
            cls._instances[cls] = super(_Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class _ControllerDependencyManager(metaclass=_Singleton):
    """Responsible for retrieving the Use Cases and Authentication service already instantiated to the Controllers

    Args:
        business_factory (BusinessFactory | None): An instance of the BusinessFactory class providing business use cases.
        authentication_service (AuthenticationService | None): An instance of the AuthenticationService class for authentication.

    """  # noqa: E501

    def __init__(
        self,
        business_factory: BusinessFactory | None = None,
        authentication_service: AuthenticationService | None = None,
    ) -> None:
        """Initialize the ControllerDependencyManager with the provided factory and service."""
        if business_factory:
            self.__factory = business_factory
        if authentication_service:
            self.__auth = authentication_service

    def auth_service(self) -> AuthenticationService:
        """Retrieve the authentication service.

        Returns:
            AuthenticationService: An instance of the AuthenticationService.

        Raises:
            ControllerDependencyManagerIsNotInitializedException: If the authentication service is not initialized.

        """

        if self.__auth:
            return self.__auth
        raise ControllerDependencyManagerIsNotInitializedException()

    def charge_pix_use_case(self) -> ChargePixUseCase:
        """Instantiate and return a RegisterUseCase with the configured account service.

        Returns:
            RegisterUseCase: An instance of RegisterUseCase with the configured account service.

        Raises:
            ControllerDependencyManagerIsNotInitializedException: If the factory is not initialized.

        """
        if self.__factory:
            return self.__factory.charge_pix_use_case()
        raise ControllerDependencyManagerIsNotInitializedException()


class _ControllerDependency(metaclass=ABCMeta):
    """Base class which emulates the Dependency Injection of FastAPI

    Args:
        credential (HTTPAuthorizationCredentials): An instance of HTTPAuthorizationCredentials.

    """

    def __init__(self, credential: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False))) -> None:
        """Initialize the ControllerDependency with the provided credential.

        Args:
            credential (HTTPAuthorizationCredentials, optional): An instance of HTTPAuthorizationCredentials. Defaults to Depends(HTTPBearer(auto_error=False)).

        Raises:
            HTTPException: If bearer authentication is needed and not provided.

        """  # noqa: E501
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
    """Brings the Register Use Case to the Register Controller through the Fast API 'Depends'"""

    def __init__(self, credential: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False))) -> None:
        """Initialize the RegisterControllerDependencies with the provided credential.

        Args:
            credential (HTTPAuthorizationCredentials, optional): An instance of HTTPAuthorizationCredentials. Defaults to Depends(HTTPBearer(auto_error=False)).

        Attributes:
            charge_pix_use_case (RegisterUseCase): An instance of RegisterUseCase configured with the provided dependencies.

        """  # noqa: E501
        super().__init__(credential)
        self.charge_pix_use_case: ChargePixUseCase = self._dependency_manager.charge_pix_use_case()
