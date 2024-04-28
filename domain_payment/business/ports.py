from domain_payment.models import AuthenticatedUserModel, PixChargeModel

from .interfaces import InputPort, OutputPort


class ChargePixInputPort(AuthenticatedUserModel, InputPort):
    charge_value: float


class ChargePixOutputPort(PixChargeModel, OutputPort):
    msg: str
