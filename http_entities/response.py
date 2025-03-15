from mashumaro import DataClassDictMixin, pass_through
from mashumaro.mixins.orjson import DataClassORJSONMixin
from mashumaro.config import BaseConfig

from http_entities.headers import Headers

from bases.http_entities.response import BaseStartResponse, BaseBodyResponse, BaseResponse
from dataclasses import dataclass, field
from orjson import dumps


@dataclass
class HTTPResponseStart(DataClassDictMixin, BaseStartResponse):
    headers: Headers

    class Config(BaseConfig):
        serialization_strategy = {
            Headers: {
                "serialize": lambda x: x.to_asgi()
            }
        }

    def to_asgi(self):
        return self.to_dict()


@dataclass
class HTTPResponseBody(DataClassDictMixin, BaseBodyResponse):

    body: bytes = field(
        metadata={
            "serialization_strategy": pass_through,
        }
    )
    #
    # def __post_init__(self):
    #     self.body = dumps(self.body)
    #     print(self.body)

    def to_asgi(self):
        return self.to_dict()


@dataclass
class HTTPResponse(BaseResponse):
    start: HTTPResponseStart
    body: HTTPResponseBody
