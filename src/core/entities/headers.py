
from src.core.entities.base_entities import BaseHTTPEntity
from msgspec import Struct


class Headers(Struct, BaseHTTPEntity):
    _headers: dict[str, str]

    @classmethod
    def build(cls, raw_headers: list[tuple[bytes, bytes]]) -> "Headers":
        return cls({k.decode("utf-8"): v.decode("utf-8") for k, v in raw_headers})

    def get(self, key: str, default: str = None) -> str | None:
        return self._headers.get(key.lower(), default)

    def to_list(self) -> list[tuple]:
        return [(k.encode("utf-8"), v.encode("utf-8")) for k,v in self._headers.items()]
