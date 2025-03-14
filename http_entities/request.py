from http import HTTPMethod
from urllib.parse import parse_qs

from bases.http_entities.base_entities import BaseHTTPEntity
from exc.request_exc import IncorrectHTTPMethod
from http_entities.headers import Headers
from msgspec import Struct


class Request(Struct, BaseHTTPEntity):
    type: str
    method: str
    path: str
    headers: Headers
    query_string: dict[str, str] = {}
    body: bytes | None = None

    @classmethod
    def build(cls, scope: dict) -> "Request":
        try:
            HTTPMethod[scope["method"]]
        except KeyError:
            raise IncorrectHTTPMethod(f'No such method: {scope["method"]}')
        if query_string := scope["query_string"].decode("UTF-8"):
            query_string = parse_qs(query_string)
        headers = Headers.build(scope["headers"])
        return cls(
            type=scope["type"],
            method=scope["method"],
            path=scope["path"],
            query_string=query_string,
            headers=headers,
            body=None
        )
