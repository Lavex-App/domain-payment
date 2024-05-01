from domain_payment.models import AuthenticatedUserModel, PixChargeResponseModel

from .interfaces import InputPort, OutputPort


class ChargePixInputPort(AuthenticatedUserModel, InputPort):
    charge_value: float


class ChargePixOutputPort(PixChargeResponseModel, OutputPort):
    msg: str
