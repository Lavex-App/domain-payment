from domain_payment.models import AuthenticatedUserModel

from .interfaces import InputPort, OutputPort


class ChargePixInputPort(AuthenticatedUserModel, InputPort):
    """Input Port for charge via pix"""

    charge_value: float


class ChargePixOutputPort(OutputPort):
    """Output Port for charge via pix"""

    msg: str
