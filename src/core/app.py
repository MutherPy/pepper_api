from typing import Callable

from src.core.bases.app import BaseApp
from src.core.bases.reader import BaseReader
from src.core.entities.request.objects import Request

from src.core.readers import reader_provider


class PepperAPI(BaseApp):

    async def read_body(self, request: Request, receive: Callable):
        reader: BaseReader = reader_provider.get_reader(request.type)
        await reader.read(request=request, receiver=receive)

    async def __call__(self, scope, receive, send):
        request: Request = self._scope_parser(scope)
        await self.read_body(request=request, receive=receive)


        response = {
            "type": "http.response.start",
            "status": 200,
            "headers": [(b"content-type", b"text/plain")],
        }
        await send(response)
        await send({"type": "http.response.body", "body": b"Hello, ASGI!"})
