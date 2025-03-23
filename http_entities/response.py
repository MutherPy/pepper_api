from inspect import isasyncgenfunction

from mashumaro import DataClassDictMixin, pass_through
from mashumaro.config import BaseConfig

from bases.http_types import ResponseType, HTTPSendEventTypes
from core.responses.response_registry import register_response_type
from http_entities.headers import Headers

from bases.http_entities.response import BaseStartResponse, BaseBodyResponse, BaseResponse
from dataclasses import dataclass, field, fields
from orjson import dumps
from bases.body import BaseBodyResponseEntity
from typing import AsyncGenerator


@dataclass
class HTTPResponseStart(DataClassDictMixin, BaseStartResponse):
    headers: Headers = field(default_factory=Headers)

    class Config(BaseConfig):
        serialization_strategy = {
            Headers: {
                "serialize": lambda x: x.to_asgi()
            }
        }

    @classmethod
    def build(cls, status) -> "HTTPResponseStart":
        return cls(
            type=HTTPSendEventTypes.START,
            status=status
        )

    async def to_asgi(self):
        return self.to_dict()


class ResponseBodyManager:
    @staticmethod
    def process(body_data) -> bytes:
        t = type(body_data)
        if issubclass(t, BaseBodyResponseEntity):
            return body_data.to_jsonb()
        else:
            return dumps(body_data)


@dataclass
class HTTPResponseBody(DataClassDictMixin, BaseBodyResponse):
    body: bytes = field(
        default=b'',
        metadata={
            "serialization_strategy": pass_through,
        }
    )
    more_body: bool = False

    @classmethod
    def build(cls, body) -> "HTTPResponseBody":
        return cls(
            type=HTTPSendEventTypes.BODY,
            body=body
        )

    async def to_asgi(self):
        self.body = ResponseBodyManager.process(self.body)
        return self.to_dict()


@register_response_type(ResponseType.HTTP)
@dataclass
class HTTPResponse(BaseResponse):
    start: HTTPResponseStart
    body: HTTPResponseBody

    @classmethod
    def build(cls, status, body) -> "HTTPResponse":
        return cls(
            start=HTTPResponseStart.build(status=status),
            body=HTTPResponseBody.build(body=body)
        )

    def update_headers(self, headers: Headers):
        self.start.headers.update(**headers.to_dict())

    async def send_to_asgi(self, sender):
        await sender(await self.start.to_asgi())
        await sender(await self.body.to_asgi())


@dataclass
class StreamingHTTPResponseBody(BaseBodyResponse):
    body: AsyncGenerator = field(
        metadata={
            "serialize": False
        }
    )
    more_body: bool = True

    def to_dict(self) -> dict:
        # mashumaro not ignoring <body> due to unserializable data type <AsyncGenerator>
        r = {i.name: getattr(self, i.name) for i in fields(self) if i.metadata.get('serialize', True)}
        return r

    @classmethod
    def build(cls, body) -> "StreamingHTTPResponseBody":
        return cls(
            type=HTTPSendEventTypes.BODY,
            body=body
        )

    async def to_asgi(self):
        tmp_data = self.to_dict()
        if isasyncgenfunction(self.body):
            self.body = self.body()
        async for i in self.body:
            tmp_data['body'] = dumps(i) if not isinstance(i, bytes) else i
            yield tmp_data
        tmp_data['body'] = b''
        tmp_data['more_body'] = False
        yield tmp_data


@register_response_type(ResponseType.STREAM)
@dataclass
class StreamingHTTPResponse(HTTPResponse):
    body: StreamingHTTPResponseBody

    @classmethod
    def build(cls, status, body) -> "StreamingHTTPResponse":
        return cls(
            start=HTTPResponseStart.build(status=status),
            body=StreamingHTTPResponseBody.build(body=body)
        )

    async def send_to_asgi(self, sender):
        await sender(await self.start.to_asgi())
        async for part in self.body.to_asgi():
            await sender(part)
