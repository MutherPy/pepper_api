from bases.http_entities.headers import BaseHeaders
from dataclasses import dataclass
from orjson import dumps


@dataclass
class Headers(BaseHeaders):
    def to_json(self):
        return dumps(self._headers).decode()

    @classmethod
    def from_scope(cls, scope: dict) -> "Headers":
        raw_headers = scope.get('headers')
        if not raw_headers:
            return cls()
        return cls({k.decode("utf-8"): v.decode("utf-8") for k, v in raw_headers})

    def to_dict(self):
        return self._headers

    @classmethod
    def from_dict(cls, data: dict):
        return cls(_headers=data)

    def get(self, key: str, default: str = None) -> str | None:
        return self._headers.get(key.lower(), default)

    def set(self, key: str, val):
        self._headers[key.lower()] = val

    def to_asgi(self) -> list[tuple]:
        return [(k.encode("utf-8"), v.encode("utf-8")) for k, v in self._headers.items()]
