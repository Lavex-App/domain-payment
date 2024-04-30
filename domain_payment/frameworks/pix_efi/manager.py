import base64
from pathlib import Path
from typing import TypedDict

import aiofiles
from efipay import EfiPay
from google.cloud import secretmanager

from domain_payment.adapters.interface_adapters.exceptions import PixQRCodeImageTemporarilyUnavailable
from domain_payment.adapters.interface_adapters.interfaces import PixProvider
from domain_payment.models import AuthenticatedUserModel, PixChargeModel, PixModel


class GCPSecretConfig(TypedDict):
    project_id: str
    service_tag: str
    env: str
    credentials: str | None


class PixFrameworkConfig(GCPSecretConfig):
    client_id: str
    client_secret: str
    sandbox: bool


class PixManager(PixProvider):
    __app: EfiPay

    def __init__(self, config: PixFrameworkConfig) -> None:
        self.__certificate_filename = "efi-certificate.pem"
        self.__config = config

    async def connect(self) -> None:
        await self.__create_certificate_file()
        self.__app = EfiPay({**self.__config, "certificate": self.__certificate_filename})

    def close(self) -> None: ...

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

    async def __create_certificate_file(self) -> None:
        secret_manager = SecretManager(self.__config)
        certificate = await secret_manager.retrieve_secret("CERTIFICATE")
        if not Path(self.__certificate_filename).exists():
            with open(self.__certificate_filename, mode="w", encoding="utf-8") as cert_file:
                cert_file.write(certificate)


class SecretManager:
    def __init__(self, config: GCPSecretConfig) -> None:
        self.__project_id = config["project_id"]
        self.__credentials = config["credentials"]
        self.__service_tag = config["service_tag"]
        self.__env = config["env"]
        self.__app = self.__get_app()

    async def retrieve_secret(self, secret_name: str) -> str:
        secret_id = f"{self.__env}_{self.__service_tag}_{secret_name}"
        secret_path = f"projects/{self.__project_id}/secrets/{secret_id}/versions/latest"
        request = secretmanager.AccessSecretVersionRequest(name=secret_path)
        response = await self.__app.access_secret_version(request=request)
        return response.payload.data.decode("utf-8")

    def __get_app(self) -> secretmanager.SecretManagerServiceAsyncClient:
        if self.__credentials:
            return secretmanager.SecretManagerServiceAsyncClient(credentials=self.__credentials)
        return secretmanager.SecretManagerServiceAsyncClient()
