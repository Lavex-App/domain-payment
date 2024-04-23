from typing import NamedTuple

from domain_payment.models import PixModel
from domain_payment.models.pix_model import CalendarModel, DebtorModel, ValueModel

from ..ports import ChargePixInputPort, ChargePixOutputPort
from ..services import AccountService, AdminService, PaymentService
from .interfaces import UseCase


class ChargePixServices(NamedTuple):
    payment_service: PaymentService
    admin_service: AdminService
    account_service: AccountService


class ChargePixUseCase(UseCase[ChargePixInputPort, ChargePixOutputPort]):
    def __init__(self, services: ChargePixServices) -> None:
        self.__payment_service = services.payment_service
        self.__admin_service = services.admin_service
        self.__account_service = services.account_service

    async def __call__(self, input_port: ChargePixInputPort) -> ChargePixOutputPort:
        account = await self.__account_service.retrieve_user(input_port)
        calendar_model = CalendarModel(expiracao=await self.__admin_service.pix_expiration_time)
        debtor_model = DebtorModel(cpf=account.cpf, nome=account.username)
        value_model = ValueModel(original=str(round(input_port.charge_value, ndigits=2)))
        pix_model = PixModel(
            calendario=calendar_model,
            devedor=debtor_model,
            valor=value_model,
            chave=await self.__admin_service.pix_key,
            solicitacaoPagador=await self.__admin_service.pix_request_type,
        )
        pix_charge_model = await self.__payment_service.generate_pix_qrcode(pix_model, input_port)
        return ChargePixOutputPort(msg="ok", **pix_charge_model.model_dump())
