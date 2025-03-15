from typing import Callable, Type

from bases.handler import BaseHandler
from http_entities.response import HTTPResponse
from exc.request_exc import NotFound
from bases.app import BaseApp
from bases.reader import BaseReader
from http_entities.request import HTTPRequest

from core.readers import reader_provider


class PepperAPI(BaseApp):

    async def request_handler(self, request: HTTPRequest) -> HTTPResponse:
        handler: Type[BaseHandler]
        url_params: dict

        handler, url_params = self.find_handler(request.path)
        if not handler:
            raise NotFound(request.path)
        handler_inst = handler(request=request)
        result = await handler_inst.process(request.method, url_params)
        response = await self.build_response(
            headers={'code': '100'},
            body=result
        )
        return response

    async def read_body(self, request: HTTPRequest, receive: Callable):
        reader: BaseReader = reader_provider.get_reader(request.type)
        await reader.read(request=request, receiver=receive)

    async def __call__(self, scope, receive, send):
        request = await self.build_request(scope, receive=receive)
        response: HTTPResponse = await self.request_handler(request=request)
        await send(response.start.to_asgi())
        await send(response.body.to_asgi())
