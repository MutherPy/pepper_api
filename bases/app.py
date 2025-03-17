from abc import ABC, abstractmethod

from bases import AsyncFunction, RSFindType
from bases.http_entities.headers import BaseHeaders
from bases.http_entities.request import BaseRequest
from bases.http_entities.response import BaseResponse
from typing import Callable, Any, Union, Optional

from bases.routing_struct import BaseRoutingStructure
from core.exc_result import ExceptionResult
from core.response_factory import ResponseFactory


class BaseApp(ABC):
    def __init__(self, routing_struct: BaseRoutingStructure):
        self.routing_struct: BaseRoutingStructure = routing_struct

    def register_route(self, path: str, handler: Callable):
        self.routing_struct.add_route(path=path, handler=handler)

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
    def build_headers(self, **kwargs) -> BaseHeaders:
        pass

    @abstractmethod
    async def build_response(self, result: Optional[Any] = None, exc_result: Optional[ExceptionResult] = None) -> BaseResponse:
        pass

    async def __call__(self, scope: dict, receive, send):
        request: BaseRequest = await self.build_request(scope=scope, receive=receive)
        result: Optional[Any] = None
        exc_result: Optional[ExceptionResult] = None
        try:
            result: Any = await self.request_handler(request=request)
        except Exception as e:
            exc_result: ExceptionResult = await self.exceptions_handler(e=e)

        response: BaseResponse = await self.build_response(result=result, exc_result=exc_result)

        await response.send_to_asgi(send)
