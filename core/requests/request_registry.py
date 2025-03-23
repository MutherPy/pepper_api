from typing import Type

from bases.registry import BaseRegistry
from exc.runtime_exc import MissedRegistering

from bases.http_entities.request import BaseRequest
from bases.http_types import RequestType
from exc.runtime_exc import IncorrectRegistering


class RequestRegistry(BaseRegistry):
    _registry: dict[str, Type[BaseRequest]] = {}

    @classmethod
    def register(cls, request_type, request_class):
        if request_type not in RequestType:
            raise IncorrectRegistering(request_type)
        cls._registry[request_type] = request_class

    @classmethod
    def retrieve(cls, request_type) -> Type[BaseRequest]:
        if request_type not in cls._registry:
            raise MissedRegistering(f"Unknown request type: {request_type}")
        return cls._registry[request_type]


def register_request_type(key):
    def decorator(cls):
        RequestRegistry.register(key, cls)
        return cls
    return decorator

