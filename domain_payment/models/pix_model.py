from decimal import Decimal

from pydantic import BaseModel, Field, field_validator, validator


class CalendarModel(BaseModel):
    expiracao: int = Field(examples=[3600])


class DebtorModel(BaseModel):
    cpf: str = Field(examples=["00000000000"])
    nome: str = Field(examples=["Fulano de Tal"])


class ValueModel(BaseModel):
    original: str = Field(examples=["123.45"])

    @field_validator("original")
    @classmethod
    def validate_decimal_places(cls, value: str) -> str:
        decimal_value = Decimal(value)
        formatted_value = f"{decimal_value:.2f}"
        return formatted_value


class PixModel(BaseModel):
    calendario: CalendarModel
    devedor: DebtorModel
    valor: ValueModel
    chave: str
    solicitacaoPagador: str


class PixChargeModel(BaseModel):
    pix_qrcode_path: str
    pix_copy_paste: str
