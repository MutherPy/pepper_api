from abc import ABC, abstractmethod

from bases import AsyncFunction, RSFindType
from bases.http_entities.headers import BaseHeaders
from bases.http_entities.request import BaseRequest
from bases.http_entities.response import BaseResponse
from typing import Callable, Any, Union

from bases.routing_struct import BaseRoutingStructure
from core.exc_result import ExceptionResult


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
    async def build_response(self, result: Union[Any, ExceptionResult], headers: BaseHeaders) -> BaseResponse:
        pass

    async def __call__(self, scope: dict, receive, send):
        request: BaseRequest = await self.build_request(scope=scope, receive=receive)

        try:
            result: Any = await self.request_handler(request=request)
        except Exception as e:
            result: ExceptionResult = await self.exceptions_handler(e=e)
        headers: BaseHeaders = self.build_headers()
        response: BaseResponse = await self.build_response(result, headers)

        await send(response.start.to_asgi())
        await send(response.body.to_asgi())


