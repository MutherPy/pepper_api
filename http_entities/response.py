from mashumaro import DataClassDictMixin, pass_through
from mashumaro.config import BaseConfig

from exc.response_exc import UnprocessableEntity
from http_entities.headers import Headers

from bases.http_entities.response import BaseStartResponse, BaseBodyResponse, BaseResponse
from dataclasses import dataclass, field
from orjson import dumps
from bases.body import BaseBodyResponseEntity


@dataclass
class HTTPResponseStart(DataClassDictMixin, BaseStartResponse):
    headers: Headers = None

    class Config(BaseConfig):
        serialization_strategy = {
            Headers: {
                "serialize": lambda x: x.to_asgi()
            }
        }

    def to_asgi(self):
        return self.to_dict()


class ResponseBodyManager:
    _serializers_strategies = {
        str: lambda x: bytes(x, 'utf-8'),
        dict: dumps,
        int: lambda x: bytes(str(x), 'utf-8'),
        type(None): dumps,
    }

    @classmethod
    def process(cls, body_data) -> bytes:
        t = type(body_data)
        if issubclass(t, BaseBodyResponseEntity):
            return body_data.to_jsonb()
        elif strat := cls._serializers_strategies.get(t):
            return strat(body_data)
        else:
            raise UnprocessableEntity(body_data)


@dataclass
class HTTPResponseBody(DataClassDictMixin, BaseBodyResponse):

    body: bytes = field(
        metadata={
            "serialization_strategy": pass_through,
        }
    )

    def to_asgi(self):
        self.body = ResponseBodyManager.process(self.body)
        return self.to_dict()


@dataclass
class HTTPResponse(BaseResponse):
    start: HTTPResponseStart
    body: HTTPResponseBody
