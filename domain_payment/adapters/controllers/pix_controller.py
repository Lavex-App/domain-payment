import logging
from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from pydantic_core import ValidationError

from domain_payment.adapters.controllers.__dependencies__ import RegisterControllerDependencies
from domain_payment.business.ports import ChargePixInputPort

from .dtos import ChargePixInputDTO, ChargePixOutputDTO

account_controller = APIRouter()


@account_controller.post(
    "/charge-pix",
    response_model=ChargePixOutputDTO,
    status_code=status.HTTP_201_CREATED,
)
async def charge_pix(
    dto: ChargePixInputDTO,
    dependencies: Annotated[RegisterControllerDependencies, Depends()],
) -> JSONResponse | ChargePixOutputDTO:
    try:
        charge_pix_input_port = ChargePixInputPort(**dto.model_dump(), uid=dependencies.uid)
        output_port = await dependencies.charge_pix_use_case(charge_pix_input_port)
        return ChargePixOutputDTO(**output_port.model_dump())
    except ValidationError as errors:
        output_errors = {}
        for error in errors.errors():
            output_errors[error["type"]] = error["msg"]
            logging.info(f"Warning [Register Account] | {error['type']} - {error['msg']}")
        content = {"msg": "error", "errors": output_errors}
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content)
