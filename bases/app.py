from abc import ABC, abstractmethod

from bases import AsyncFunction, RSFindType
from bases.http_entities.headers import BaseHeaders
from bases.http_entities.request import BaseRequest, BaseWSRequest
from bases.http_entities.response import BaseResponse
from bases.handler import BaseHandler, BaseWSHandler
from typing import Any, Optional, Type, Union

from bases.http_types import ScopeType, WSSendEventTypes
from bases.middleware import BaseMiddleware
from bases.routing_struct import BaseRoutingStructure
from core.exc_result import ExceptionResult, WSExceptionResult
from typing import TYPE_CHECKING

from core.method_meta import HandlerMethodResult

from contextvars import ContextVar

if TYPE_CHECKING:
    from bases.router import BaseRouter


class BaseApp(ABC):
    def __init__(self, http_routing_struct: BaseRoutingStructure, ws_routing_struct: BaseRoutingStructure = None):
        self.http_routing_struct: BaseRoutingStructure = http_routing_struct
        self.ws_routing_struct: Optional[BaseRoutingStructure] = ws_routing_struct if ws_routing_struct else http_routing_struct

        self.http_app = self.main_http_app

        self.ws_app = self.main_ws_app

        self.ws_connection: ContextVar = ContextVar('ws_connection', default=False)

    def _register_route(self, path: str, handler: Type[BaseHandler]):
        self.http_routing_struct.add_route(path=path, handler=handler)

    def _register_ws_route(self, path: str, handler: Type[BaseWSHandler]):
        self.ws_routing_struct.add_route(path, handler)

    def include_router(self, router: "BaseRouter"):
        for path, handler in router.handlers.items():
            self._register_route(path, handler=handler)
        for path, handler in router.ws_handlers.items():
            self._register_ws_route(path, handler)

    def add_middleware(self, middleware: Type[BaseMiddleware]):
        self.http_app = middleware(self.http_app)

    def add_ws_middleware(self, middleware):  # TODO add ws middlewares interface
        self.ws_app = middleware(self.ws_app)

    def find_handler(self, path: str) -> RSFindType:
        return self.http_routing_struct.find_handler(path=path)

    def find_ws_handler(self, path: str) -> RSFindType:
        return self.ws_routing_struct.find_handler(path=path)

    @abstractmethod
    async def build_request(self, scope: dict, receive: AsyncFunction = None) -> Union[BaseRequest, BaseWSRequest]:
        pass

    @abstractmethod
    async def request_handler(self, request: BaseRequest) -> Any:
        pass

    @abstractmethod
    async def ws_request_handler(self, request: BaseWSRequest, receive: AsyncFunction, send: AsyncFunction):
        pass

    @abstractmethod
    async def exceptions_handler(self, e: Exception) -> ExceptionResult:
        pass

    @abstractmethod
    async def ws_exceptions_handler(self, e: Exception) -> WSExceptionResult:
        pass

    @abstractmethod
    def build_headers(self, headers: Optional[dict] = None) -> BaseHeaders:
        pass

    @abstractmethod
    async def build_response(self, result: Optional[Any] = None, exc_result: Optional[ExceptionResult] = None) -> BaseResponse:
        pass

    async def main_http_app(self, scope: dict, receive, send) -> BaseResponse:
        request: BaseRequest = await self.build_request(scope=scope, receive=receive)
        result: Optional[Any] = None
        exc_result: Optional[ExceptionResult] = None
        try:
            result: Union[Any, HandlerMethodResult] = await self.request_handler(request=request)
        except Exception as e:
            exc_result: ExceptionResult = await self.exceptions_handler(e=e)
        response: BaseResponse = await self.build_response(result=result, exc_result=exc_result)
        return response

    async def main_ws_app(self, scope: dict, receive, send):
        request: BaseWSRequest = await self.build_request(scope=scope)
        await self.ws_request_handler(request, receive, send)

    async def __call__(self, scope: dict, receive, send):
        scope_type = scope['type']
        if scope_type == ScopeType.HTTP:
            try:
                response = await self.http_app(scope, receive, send)
            except Exception as e:
                exc_result: ExceptionResult = await self.exceptions_handler(e=e)
                response: BaseResponse = await self.build_response(result=None, exc_result=exc_result)
            await response.send_to_asgi(send)
        elif scope_type == ScopeType.WS:
            try:
                await self.ws_app(scope, receive, send)
            except Exception as e:
                exc_result: WSExceptionResult = await self.ws_exceptions_handler(e)
                # let client connect, and then close connection to share info while closing
                if not self.ws_connection.get():
                    await send({"type": WSSendEventTypes.ACCEPT})
                await send({"type": WSSendEventTypes.CLOSE, "code": exc_result.code, "reason": exc_result.reason})
        elif scope_type == ScopeType.LIFE:
            print('lifespan')
