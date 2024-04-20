from abc import ABCMeta, abstractmethod


class UserUid(str):
    """Represents a unique identifier for a user."""


class BearerToken(str):
    """Represents a bearer token for authentication."""


class AuthenticationService(metaclass=ABCMeta):
    """Abstract base class for authentication services."""

    @abstractmethod
    def authenticate_by_token(self, token: BearerToken) -> UserUid:
        """Authenticate user by bearer token.

        Args:
            token (BearerToken): The bearer token for authentication.

        Returns:
            UserUid: The unique identifier of the authenticated user.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
