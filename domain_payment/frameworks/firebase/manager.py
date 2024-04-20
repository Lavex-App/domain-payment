from typing import TypedDict

import firebase_admin
import firebase_admin.auth
from fastapi import status
from fastapi.exceptions import HTTPException
from firebase_admin import credentials

from domain_payment.adapters.interfaces.authentication_service import AuthenticationService, BearerToken, UserUid


class FirebaseFrameworkConfig(TypedDict):
    """Specification of the configurations required by the Firebase framework."""

    credentials: str | None
    auth_app_options: dict[str, str]


class FirebaseManager(AuthenticationService):
    """
    Implementation of the AuthenticationService interface using Firebase Authentication.

    This class provides methods to authenticate users using Firebase Authentication service.
    """

    def __init__(self, config: FirebaseFrameworkConfig) -> None:
        """
        Initialize FirebaseManager with Firebase credentials and app options.

        Args:
            config (FirebaseFrameworkConfig): Firebase credentials and other options.
        """
        credential = config.get("credentials")
        app_options = config.get("auth_app_options")
        if credential is None:
            self.__firebase_app = firebase_admin.initialize_app()
        else:
            self.__firebase_app = firebase_admin.initialize_app(
                credentials.Certificate(credential), options=app_options
            )

    def authenticate_by_token(self, token: BearerToken) -> UserUid:
        """
        Authenticate user by bearer token using Firebase Authentication service.

        Args:
            token (BearerToken): The bearer token for authentication.

        Returns:
            UserUid: The unique identifier of the authenticated user.

        Raises:
            HTTPException: If the token is invalid or expired.
        """
        try:
            decoded_token = firebase_admin.auth.verify_id_token(token, self.__firebase_app)
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication",
                headers={"WWW-Authenticate": 'Bearer error="invalid_token"'},
            ) from error

        uid = decoded_token["uid"]
        return UserUid(uid)
