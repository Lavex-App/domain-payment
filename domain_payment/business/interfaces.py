from abc import ABCMeta

import bson
from pydantic import BaseModel

from domain_payment.types.object_id import ObjectId


class Service(metaclass=ABCMeta):
    """Base representation of a service, it can be a pubsub, repository... or something else"""


class Port(BaseModel, metaclass=ABCMeta):
    """Base class for Port objects."""

    class Config:
        """Configuration class."""

        extra = "ignore"
        json_encoders = {bson.ObjectId: str, ObjectId: str}


class InputPort(Port, metaclass=ABCMeta):
    """Interface for routes input DTOs."""


class OutputPort(Port, metaclass=ABCMeta):
    """Interface for routes output DTOs."""
