from typing import Callable

from src.core.entities.response.objects import Response
from src.core.exceptions.request_exc import NotFound
from src.core.bases.app import BaseApp
from src.core.bases.reader import BaseReader
from src.core.entities.request.objects import Request

from src.core.readers import reader_provider

from http import HTTPStatus


class PepperAPI(BaseApp):

    async def request_handler(self, request: Request) -> Response:
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

    async def read_body(self, request: Request, receive: Callable):
        reader: BaseReader = reader_provider.get_reader(request.type)
        await reader.read(request=request, receiver=receive)

    async def __call__(self, scope, receive, send):
        request: Request = self._scope_parser(scope)
        await self.read_body(request=request, receive=receive)

        response: Response = await self.request_handler(request=request)

        await send(response.start.to_dict())
        await send(response.body.to_dict())
