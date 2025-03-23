from typing import Type

from bases.http_entities.response import BaseResponse
from bases.registry import BaseRegistry
from bases.http_types import ResponseType
from exc.runtime_exc import IncorrectRegistering


class ResponseRegistry(BaseRegistry):
    _registry: dict[str, Type[BaseResponse]] = {}

    @classmethod
    def register(cls, response_type, response_class):
        if response_type not in ResponseType:
            raise IncorrectRegistering(response_type)
        cls._registry[response_type] = response_class

    @classmethod
    def retrieve(cls, response_type) -> Type[BaseResponse]:
        if response_type not in cls._registry:
            raise ValueError(f"Unknown response type: {response_type}")
        return cls._registry[response_type]


def register_response_type(key):
    def decorator(cls):
        ResponseRegistry.register(key, cls)
        return cls
    return decorator
