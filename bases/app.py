from abc import ABC, abstractmethod
from http_entities.request import HTTPRequest
from typing import Callable

from bases.routing_struct import BaseRoutingStructure, TypeRouterFindResponse


class BaseApp(ABC):
    def __init__(self, routing_struct: BaseRoutingStructure):
        self.routing_struct: BaseRoutingStructure = routing_struct

    def register_route(self, path: str, handler: Callable):
        self.routing_struct.add_route(path=path, handler=handler)

    def find_handler(self, path: str) -> TypeRouterFindResponse:
        return self.routing_struct.find_handler(path=path)

    async def build_request(self, scope: dict, receive: Callable) -> HTTPRequest:
        r = HTTPRequest.build(scope)
        await self.read_body(request=r, receive=receive)
        return r

    @abstractmethod
    async def read_body(self, request: HTTPRequest, receive: Callable):
        raise NotImplementedError

    @abstractmethod
    async def request_handler(self, request: HTTPRequest):
        raise NotImplementedError

    @abstractmethod
    async def __call__(self, scope, receive, send):
        raise NotImplementedError


