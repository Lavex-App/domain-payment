from typing import TypedDict

from efipay import EfiPay

from domain_payment.business.services import PixService
from domain_payment.models import PixModel


class PixFrameworkConfig(TypedDict):
    """Specification of the configurations required by the Pix framework."""

    certificate: str
    client_id: str
    client_secret: str
    sandbox: bool


class PixManager(PixService):
    def __init__(self, config: PixFrameworkConfig) -> None:
        self.__app = EfiPay(config)

    def generate_pix_qrcode(self, charge_model: PixModel) -> None:
        body = charge_model.model_dump()
        pix = self.__app.pix_create_immediate_charge(body=body)
        print(pix)
