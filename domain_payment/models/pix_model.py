from pydantic import BaseModel, Field


class CalendarModel(BaseModel):
    """Model that defines debtor information"""

    expiracao: int = Field(examples=["3600"])


class DebtorModel(BaseModel):
    """Model that defines debtor information"""

    cpf: str = Field(examples=["00000000000"])
    nome: str = Field(examples=["Fulano de Tal"])


class ValueModel(BaseModel):
    """Model that defines the value of the pix transaction"""

    original: str = Field(examples=["123.45"])


class PixModel(BaseModel):
    """Model that defines pix base information"""

    calendario: CalendarModel
    devedor: DebtorModel
    valor: ValueModel
    chave: str
    solicitacaoPagador: str
