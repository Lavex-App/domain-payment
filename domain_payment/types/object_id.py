from typing import Any, Callable, Iterable

import bson


class ObjectId(bson.ObjectId):
    @classmethod
    def __get_validators__(cls) -> Iterable[Callable]:
        yield cls.validate

    @classmethod
    def validate(cls, value: Any) -> bson.ObjectId:
        if isinstance(value, bson.ObjectId):
            return value
        if ObjectId.is_valid(value):
            return ObjectId(value)
        raise ValueError("Invalid objectid.")

    @classmethod
    def __modify_schema__(cls, field_schema: dict) -> None:
        field_schema.update(type="string")
