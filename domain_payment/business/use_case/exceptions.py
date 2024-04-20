class BusinessException(RuntimeError):
    """
    Base class for business-related exceptions.

    This exception serves as the base class for all business-related exceptions. It provides
    a consistent interface for accessing the error message and type.

    Attributes:
        msg (str): A human-readable message describing the exception.
        type (str): The type of the exception.
    """

    def __init__(self, msg: str) -> None:
        """Initialize the BusinessException with the specified message."""
        super().__init__(msg)
        self.type = self.__class__.__name__
        self.msg = msg

    def __str__(self) -> str:
        """Return a string representation of the exception."""
        return f"[{self.type}] {self.msg}"
