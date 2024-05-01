from domain_payment.models import PixChargeResponseModel

from .interfaces import InputDTO, OutputDTO


class ChargePixInputDTO(InputDTO):
    charge_value: float


class ChargePixOutputDTO(PixChargeResponseModel, OutputDTO):
    msg: str
