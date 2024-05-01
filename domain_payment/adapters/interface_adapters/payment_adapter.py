from typing import NamedTuple

from domain_payment.business.services import PaymentService
from domain_payment.models import AuthenticatedUserModel, PixChargeResponseModel, PixModel

from .interfaces import BucketProvider, ImageUploadInput, PixProvider


class PaymentAdapterConfig(NamedTuple):
    pix_qrcode_bucket_name: str


class PaymentProviders(NamedTuple):
    pix_provider: PixProvider
    bucket_provider: BucketProvider


class PaymentAdapter(PaymentService):
    def __init__(self, providers: PaymentProviders, config: PaymentAdapterConfig):
        self.__pix_provider = providers.pix_provider
        self.__bucket_provider = providers.bucket_provider
        self.__bucket_name = config.pix_qrcode_bucket_name

    async def generate_pix_qrcode(
        self, pix_model: PixModel, user_model: AuthenticatedUserModel
    ) -> PixChargeResponseModel:
        pix_charge_model = await self.__pix_provider.create_charge(pix_model)
        pix_qrcode_image_path = f"{user_model.uid}.png"
        async with self.__bucket_provider as bucket_uploader:
            image_upload_result = await bucket_uploader.upload(
                ImageUploadInput(
                    image=pix_charge_model.pix_qrcode_image,
                    bucket_name=self.__bucket_name,
                    image_name_on_bucket=f"pixQRCodeImages/{pix_qrcode_image_path}",
                )
            )
            return PixChargeResponseModel(
                pix_copy_paste=pix_charge_model.pix_copy_paste,
                pix_qrcode_path=image_upload_result.image_uri,
            )
