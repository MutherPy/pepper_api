from typing import Union

from msgspec import Struct
from src.core.entities.base_entities import BaseHTTPEntity
from src.core.entities.response.types import ResponseTypes
from src.core.entities.headers import Headers


class ResponseStart(Struct, BaseHTTPEntity):
    type: str
    status: int
    headers: Headers

    @classmethod
    def build(cls, scope: Union[dict, list]) -> "ResponseStart":
        return cls(
            type=ResponseTypes.START,
            status=scope['status'],
            headers=Headers.build(scope.get('headers')).to_list()
        )


class ResponseBody(Struct, BaseHTTPEntity):
    type: str
    body: bytes
    more_body: bool

    @classmethod
    def build(cls, scope: Union[dict, list]) -> "ResponseBody":
        return cls(
            type=ResponseTypes.BODY,
            body=scope['body'],
            more_body=scope.get('more_body', False)
        )


class Response(Struct, BaseHTTPEntity):
    start: ResponseStart
    body: ResponseBody

    @classmethod
    def build(cls, scope: Union[dict, list]) -> "Response":
        return cls(
            start=ResponseStart.build(scope),
            body=ResponseBody.build(scope)
        )



