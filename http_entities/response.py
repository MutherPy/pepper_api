from mashumaro import DataClassDictMixin
from mashumaro.config import BaseConfig

from http_entities.headers import Headers

from bases.http_entities.response import BaseStartResponse, BaseBodyResponse, BaseResponse
from dataclasses import dataclass


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
    def to_asgi(self):
        return self.to_dict()


@dataclass
class HTTPResponse(BaseResponse):
    start: HTTPResponseStart
    body: HTTPResponseBody
