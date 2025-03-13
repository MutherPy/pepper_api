
from src.core.entities.base_entities import BaseHTTPEntity
from msgspec import Struct


class Headers(Struct, BaseHTTPEntity):
    """Клас для обробки заголовків HTTP-запиту."""
    __headers: dict[str, str]

    @classmethod
    def build(cls, raw_headers: list[tuple[bytes, bytes]]) -> "Headers":
        return cls({k.decode("utf-8"): v.decode("utf-8") for k, v in raw_headers})

    def _get(self, key: str, default: str = None) -> str | None:
        return self.__headers.get(key.lower(), default)

    def __getitem__(self, key):
        self.__headers.get(key.lower(), None)
