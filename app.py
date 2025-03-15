from typing import Callable

from http_entities.response import Response
from exc.request_exc import NotFound
from bases.app import BaseApp
from bases.reader import BaseReader
from http_entities.request import HTTPRequest

from core.readers import reader_provider

from http import HTTPStatus


class PepperAPI(BaseApp):

    async def request_handler(self, request: HTTPRequest) -> Response:
        handler, params = self.find_handler(request.path)
        if not handler:
            raise NotFound(path=request.path)
        result = await (
            handler(request).process(
                method=request.method.lower(),
                params=params
            )
        )
        return Response.build(
            dict(
                status=HTTPStatus.OK,
                headers=[(b'content-type', b'text/plain')],
                body=result.encode('utf-8'),
            )
        )

    async def read_body(self, request: HTTPRequest, receive: Callable):
        reader: BaseReader = reader_provider.get_reader(request.type)
        await reader.read(request=request, receiver=receive)

    async def __call__(self, scope, receive, send):
        request = await self.build_request(scope, receive=receive)
        response: Response = await self.request_handler(request=request)
        await send(response.start.to_dict())
        await send(response.body.to_dict())
