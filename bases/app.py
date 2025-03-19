from abc import ABC, abstractmethod

from bases import AsyncFunction, RSFindType
from bases.http_entities.headers import BaseHeaders
from bases.http_entities.request import BaseRequest
from bases.http_entities.response import BaseResponse
from bases.handler import BaseHandler
from typing import Any, Optional, Type, Union

from bases.http_types import RequestType
from bases.middleware import BaseMiddleware
from bases.routing_struct import BaseRoutingStructure
from core.exc_result import ExceptionResult
from typing import TYPE_CHECKING

from core.method_meta import HandlerMethodResult

if TYPE_CHECKING:
    from bases.router import BaseRouter


class BaseApp(ABC):
    def __init__(self, routing_struct: BaseRoutingStructure):
        self.routing_struct: BaseRoutingStructure = routing_struct

        self.__app = self.app

    def _register_route(self, path: str, handler: Type[BaseHandler]):
        self.routing_struct.add_route(path=path, handler=handler)

    def include_router(self, router: "BaseRouter"):
        for path, handler in router.handlers.items():
            self._register_route(path, handler=handler)

    def add_middleware(self, middleware: Type[BaseMiddleware]):
        self.__app = middleware(self.__app)

    def find_handler(self, path: str) -> RSFindType:
        return self.routing_struct.find_handler(path=path)

    @abstractmethod
    async def build_request(self, scope: dict, receive: AsyncFunction) -> BaseRequest:
        pass

    @abstractmethod
    async def request_handler(self, request: BaseRequest) -> Any:
        pass

    @abstractmethod
    async def exceptions_handler(self, e: Exception) -> ExceptionResult:
        pass

    @abstractmethod
    def build_headers(self, headers: Optional[dict] = None) -> BaseHeaders:
        pass

    @abstractmethod
    async def build_response(self, result: Optional[Any] = None, exc_result: Optional[ExceptionResult] = None) -> BaseResponse:
        pass

    async def app(self, scope: dict, receive, send) -> BaseResponse:
        request: BaseRequest = await self.build_request(scope=scope, receive=receive)
        result: Optional[Any] = None
        exc_result: Optional[ExceptionResult] = None
        try:
            result: Union[Any, HandlerMethodResult] = await self.request_handler(request=request)
        except Exception as e:
            exc_result: ExceptionResult = await self.exceptions_handler(e=e)
        response: BaseResponse = await self.build_response(result=result, exc_result=exc_result)
        return response

    async def __call__(self, scope: dict, receive, send):
        if scope['type'] == RequestType.HTTP:
            try:
                response = await self.__app(scope, receive, send)
            except Exception as e:
                exc_result: ExceptionResult = await self.exceptions_handler(e=e)
                response: BaseResponse = await self.build_response(result=None, exc_result=exc_result)
            await response.send_to_asgi(send)
        elif scope['type'] == RequestType.LIFE:
            print('lifespan')
