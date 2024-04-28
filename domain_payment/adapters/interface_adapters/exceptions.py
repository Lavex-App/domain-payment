class InterfaceAdaptersException(RuntimeError):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)
        self.type = self.__class__.__name__
        self.msg = msg

    def __str__(self) -> str:
        return f"[{self.type}] {self.msg}"


class UserNotFound(InterfaceAdaptersException):
    def __init__(self) -> None:
        super().__init__("There is no User related to the provided UID")


class AdminIsNotProperlyConfigured(InterfaceAdaptersException):
    def __init__(self) -> None:
        super().__init__("Admin collection is not configured properly")


class PixQRCodeImageTemporarilyUnavailable(InterfaceAdaptersException):
    def __init__(self) -> None:
        super().__init__("Pix service cannot generate QR Code images temporarily")
