from abc import ABC, abstractmethod
from src.core.entities.request.objects import Request
from typing import Callable, Type, Optional

from src.core.bases.routing_struct import BaseRoutingStructure
from src.core.bases.handler import BaseHandler


class BaseApp(ABC):
    def __init__(self, routing_struct: BaseRoutingStructure):
        self.routing_struct: BaseRoutingStructure = routing_struct

    def register_route(self, path: str, handler: Callable):
        self.routing_struct.add_route(path=path, handler=handler)

    def find_handler(self, path: str) -> tuple[Optional[Type[BaseHandler]], Optional[dict]]:
        return self.routing_struct.find_handler(path=path)

    def _scope_parser(self, scope: dict) -> Request:
        return Request.build(scope)

    @abstractmethod
    async def request_handler(self, request: Request):
        raise NotImplementedError

    @abstractmethod
    async def read_body(self, request: Request, receive: Callable):
        raise NotImplementedError

    @abstractmethod
    async def __call__(self, scope, receive, send):
        raise NotImplementedError


from src.core.bases.router import BaseRouter
