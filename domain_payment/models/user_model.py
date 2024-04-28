from pydantic import BaseModel, Field


class AuthenticatedUserModel(BaseModel):
    uid: str


class AccountModel(BaseModel):
    cpf: str = Field(examples=["77777777777"])
    username: str = Field(examples=["Vinicius Abade"])
