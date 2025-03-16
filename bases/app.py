from abc import ABC, abstractmethod

from bases.http_entities.headers import BaseHeaders
from http_entities.request import HTTPRequest
from http_entities.response import HTTPResponse, HTTPResponseStart, HTTPResponseBody
from http_entities.headers import Headers
from typing import Callable, Union, Optional, Any

from bases.routing_struct import BaseRoutingStructure, RSFindType
from http import HTTPStatus
from bases.http_types import SendEventTypes
from orjson import dumps


class BaseApp(ABC):
    def __init__(self, routing_struct: BaseRoutingStructure):
        self.routing_struct: BaseRoutingStructure = routing_struct

    def register_route(self, path: str, handler: Callable):
        self.routing_struct.add_route(path=path, handler=handler)

    def find_handler(self, path: str) -> RSFindType:
        return self.routing_struct.find_handler(path=path)

    async def build_request(self, scope: dict, receive: Callable) -> HTTPRequest:
        r = HTTPRequest.from_scope(scope)
        await self.read_body(request=r, receive=receive)
        return r

    async def build_response(
            self,
            status: int = HTTPStatus.OK,
            headers: Union[BaseHeaders, dict] = None,
            body: Optional[Any] = None,
            more_body: bool = False
    ) -> HTTPResponse:
        if not isinstance(headers, BaseHeaders):
            headers = Headers.from_dict(headers) if headers else {}
        start = HTTPResponseStart(type=SendEventTypes.START, status=status, headers=headers)
        body = HTTPResponseBody(type=SendEventTypes.BODY, body=body, more_body=more_body)
        return HTTPResponse(start=start, body=body)

    @abstractmethod
    async def read_body(self, request: HTTPRequest, receive: Callable):
        pass

    @abstractmethod
    async def request_handler(self, request: HTTPRequest):
        pass

    @abstractmethod
    async def __call__(self, scope, receive, send):
        pass
