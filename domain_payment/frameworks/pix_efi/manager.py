import base64
from typing import TypedDict

import aiofiles
from efipay import EfiPay

from domain_payment.adapters.interface_adapters.exceptions import PixQRCodeImageTemporarilyUnavailable
from domain_payment.adapters.interface_adapters.interfaces import PixProvider
from domain_payment.models import AuthenticatedUserModel, PixChargeModel, PixModel


class PixFrameworkConfig(TypedDict):
    certificate: str
    client_id: str
    client_secret: str
    sandbox: bool


class PixManager(PixProvider):
    def __init__(self, config: PixFrameworkConfig) -> None:
        self.__app = EfiPay(config)

    async def create_charge(self, pix_model: PixModel, user_model: AuthenticatedUserModel) -> PixChargeModel:
        body = pix_model.model_dump()
        pix = self.__app.pix_create_immediate_charge(body=body)
        params = {"id": pix["loc"]["id"]}
        qrcode_response = self.__app.pix_generate_qrcode(params=params)
        if "imagemQrcode" in qrcode_response:
            filename = f"{user_model.uid}.png"
            async with aiofiles.open(filename, mode="wb") as fh:
                await fh.write(base64.b64decode(qrcode_response["imagemQrcode"].replace("data:image/png;base64,", "")))
            return PixChargeModel(pix_qrcode_path=filename, pix_copy_paste=qrcode_response["qrcode"])
        raise PixQRCodeImageTemporarilyUnavailable()
