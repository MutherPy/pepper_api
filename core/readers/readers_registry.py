from typing import Type, Optional

from bases.reader import BaseReader
from bases.registry import BaseRegistry


class ReaderRegistry(BaseRegistry):
    _registry: dict[str, Type[BaseReader]] = {}

    @classmethod
    def register(cls, request_type: str, reader_class: Type[BaseReader]):
        cls._registry[request_type] = reader_class

    @classmethod
    def retrieve(cls, request_type: str) -> Optional[BaseReader]:
        if request_type not in cls._registry:
            return None
        return cls._registry[request_type]()


def register_request_reader_type(key):
    def decorator(cls):
        ReaderRegistry.register(key, cls)
        return cls
    return decorator

