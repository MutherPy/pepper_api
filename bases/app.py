from abc import ABC, abstractmethod
from http_entities.request import Request
from typing import Callable, Type, Optional

from bases.routing_struct import BaseRoutingStructure
from bases.handler import BaseHandler

from typing import TypeAlias


TypeRouterFindResponse: TypeAlias = tuple[Optional[Type[BaseHandler]], Optional[dict]]


class BaseApp(ABC):
    def __init__(self, routing_struct: BaseRoutingStructure):
        self.routing_struct: BaseRoutingStructure = routing_struct

    def register_route(self, path: str, handler: Callable):
        self.routing_struct.add_route(path=path, handler=handler)

    def find_handler(self, path: str) -> TypeRouterFindResponse:
        return self.routing_struct.find_handler(path=path)

    async def build_request(self, scope: dict, receive: Callable) -> Request:
        r = Request.build(scope)
        await self.read_body(request=r, receive=receive)
        return r

    @abstractmethod
    async def read_body(self, request: Request, receive: Callable):
        raise NotImplementedError

    @abstractmethod
    async def request_handler(self, request: Request):
        raise NotImplementedError

    @abstractmethod
    async def __call__(self, scope, receive, send):
        raise NotImplementedError


