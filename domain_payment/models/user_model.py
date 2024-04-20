from pydantic import BaseModel, Field


class AuthenticatedUserModel(BaseModel):
    """Model that defines an authenticated user"""

    uid: str


class AccountModel(BaseModel):
    """Model that defines the user information"""

    cpf: str = Field(examples=["77777777777"])
    username: str = Field(examples=["Vinicius Abade"])
