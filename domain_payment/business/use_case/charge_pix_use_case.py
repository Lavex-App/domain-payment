from typing import NamedTuple

from domain_payment.models import PixModel
from domain_payment.models.pix_model import CalendarModel, DebtorModel, ValueModel

from ..ports import ChargePixInputPort, ChargePixOutputPort
from ..services import AccountService, AdminService, PixService
from .interfaces import UseCase


class Services(NamedTuple):
    pix_service: PixService
    admin_service: AdminService
    account_service: AccountService


class ChargePixUseCase(UseCase[ChargePixInputPort, ChargePixOutputPort]):
    """Use case for updating user CPF.

    This use case handles the updating of user CPF. It receives input data via an UpdateCpfInputPort,
    updates the CPF via the provided AccountService, and returns an UpdateCpfOutputPort indicating
    the success of the CPF update process.

    Args:
        services (Services): An instance of AccountService providing business logic for account-related operations.
    """

    def __init__(self, services: Services) -> None:
        """Initialize the UpdateCpfUseCase with the provided AccountService."""
        self.__pix_service = services.pix_service
        self.__admin_service = services.admin_service
        self.__account_service = services.account_service

    async def __call__(self, input_port: ChargePixInputPort) -> ChargePixOutputPort:
        """Execute the update CPF use case.

        Updates the user CPF with the provided information via the AccountService.

        Args:
            input_port (UpdateCpfInputPort): The input port containing user UID and CPF.

        Returns:
            UpdateCpfOutputPort: An output port containing a message indicating the success of the CPF update process.
        """  # noqa: E501
        admin_pix_key = await self.__admin_service.pix_key()
        admin_pix_expiration_time = await self.__admin_service.pix_expiration_time()
        admin_pix_request_type = await self.__admin_service.pix_request_type()
        account = await self.__account_service.retrieve_user(input_port)

        calendar_model = CalendarModel(expiracao=admin_pix_expiration_time)
        debtor_model = DebtorModel(cpf=account.cpf, nome=account.username)
        value_model = ValueModel(original=input_port.charge_value)
        pix_model = PixModel(
            calendario=calendar_model,
            devedor=debtor_model,
            valor=value_model,
            chave=admin_pix_key,
            solicitacaoPagador=admin_pix_request_type,
        )

        self.__pix_service.generate_pix_qrcode(pix_model)
        return ChargePixOutputPort(msg="ok")
