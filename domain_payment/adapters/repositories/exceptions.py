class RepositoriesException(RuntimeError):
    """
    Base class for repositories-related exceptions.

    This exception serves as the base class for all repositories-related exceptions. It provides
    a consistent interface for accessing the error message and type.

    Attributes:
        msg (str): A human-readable message describing the exception.
        type (str): The type of the exception.
    """

    def __init__(self, msg: str) -> None:
        """
        Initialize the RepositoriesException with the specified message.

        Args:
            msg (str): A human-readable message describing the exception.
        """
        super().__init__(msg)
        self.type = self.__class__.__name__
        self.msg = msg

    def __str__(self) -> str:
        """Return a string representation of the exception."""
        return f"[{self.type}] {self.msg}"


class UserNotFound(RepositoriesException):
    """
    Exception raised when a user is not found in the repository.

    This exception is raised when attempting to retrieve a user from the repository by UID,
    but no user is found with the provided UID.
    """

    def __init__(self) -> None:
        """Initialize the UserNotFound exception."""
        super().__init__("There is no User related to the provided UID")
