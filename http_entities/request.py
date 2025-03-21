from http_entities.headers import Headers
from http_entities.query import Query
from bases.http_entities.request import BaseRequest, BaseWSRequest
from mashumaro import DataClassDictMixin
from mashumaro.mixins.orjson import DataClassORJSONMixin
from dataclasses import dataclass
from mashumaro.config import BaseConfig


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
