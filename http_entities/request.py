from http_entities.headers import Headers
from http_entities.query import Query
from bases.http_entities.request import BaseRequest, BaseWSRequest
from mashumaro import DataClassDictMixin
from mashumaro.mixins.orjson import DataClassORJSONMixin
from dataclasses import dataclass
from mashumaro.config import BaseConfig
from io import FileIO

from core.requests.request_registry import register_request_type
from bases.http_types import RequestType


@register_request_type(RequestType.COMMON_HTTP)
@dataclass
class HTTPRequest(DataClassORJSONMixin, DataClassDictMixin, BaseRequest):
    headers: Headers
    query_string: Query

    class Config(BaseConfig):
        forbid_extra_keys = True
        serialization_strategy = {
            Headers: {
                "serialize": lambda x: x.to_dict()
            },
            Query: {
                "serialize": lambda x: x.to_dict()
            }
        }

    @classmethod
    def from_scope(cls, scope: dict) -> "HTTPRequest":
        return cls(
            type=scope['type'],
            method=scope['method'],
            path=scope['path'],
            headers=Headers.from_scope(scope),
            query_string=Query.from_scope(scope)
        )


@register_request_type(RequestType.FILE_HTTP)
@dataclass
class HTTPFileRequest(HTTPRequest):
    body: bytes | None = None


@register_request_type(RequestType.BIGFILE_HTTP)
@dataclass
class HTTPBigFileRequest(BaseRequest):
    body: FileIO | None = None

    def to_json(self) -> str:
        pass

    @classmethod
    def from_scope(cls, scope: dict):
        return cls(
            type=scope['type'],
            method=scope['method'],
            path=scope['path'],
            headers=Headers.from_scope(scope),
            query_string=Query.from_scope(scope)
        )


@register_request_type(RequestType.COMMON_WS)
@dataclass
class WSRequest(DataClassDictMixin, BaseWSRequest):
    @classmethod
    def from_scope(cls, scope: dict) -> "WSRequest":
        return cls(
            type=scope['type'],
            path=scope['path'],
            headers=Headers.from_scope(scope),
            query_string=Query.from_scope(scope),
        )
