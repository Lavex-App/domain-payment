from abc import ABCMeta

import bson
from pydantic import BaseModel

from domain_payment.types.object_id import ObjectId


class DTO(BaseModel, metaclass=ABCMeta):
    """Base class for DTO objects."""

    class Config:
        """Configuration class."""

        extra = "ignore"
        json_encoders = {bson.ObjectId: str, ObjectId: str}


class InputDTO(DTO, metaclass=ABCMeta):
    """Interface for routes input DTOs."""


class OutputDTO(DTO, metaclass=ABCMeta):
    """Interface for routes output DTOs."""
