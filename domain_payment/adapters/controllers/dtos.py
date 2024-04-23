from domain_payment.models import PixChargeModel

from .interfaces import InputDTO, OutputDTO


class ChargePixInputDTO(InputDTO):
    charge_value: float


class ChargePixOutputDTO(PixChargeModel, OutputDTO):
    msg: str
