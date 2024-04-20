from .interfaces import InputDTO, OutputDTO


class RetrieveAccountInputDTO(InputDTO):
    """Input DTO for retrieve an authenticated user"""

    uid: str


class ChargePixInputDTO(InputDTO):
    """Input DTO for charge via pix"""

    charge_value: float


class ChargePixOutputDTO(OutputDTO):
    """Output DTO for charge via pix"""

    msg: str
