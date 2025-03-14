from typing import Callable

from src.core.exceptions.request_exc import NotFound
from src.core.bases.app import BaseApp
from src.core.bases.reader import BaseReader
from src.core.entities.request.objects import Request

from src.core.readers import reader_provider


class PepperAPI(BaseApp):

    async def request_handler(self, request: Request):
        handler, params = self.find_handler(request.path)
        if not handler:
            raise NotFound(path=request.path)
        h_inst = handler(request)
        return await h_inst.process(method=request.method.lower(), params=params)

    async def read_body(self, request: Request, receive: Callable):
        reader: BaseReader = reader_provider.get_reader(request.type)
        await reader.read(request=request, receiver=receive)

    async def __call__(self, scope, receive, send):
        request: Request = self._scope_parser(scope)
        await self.read_body(request=request, receive=receive)
        response = await self.request_handler(request=request)

        response = {
            "type": "http.response.start",
            "status": 200,
            "headers": [(b"content-type", b"text/plain")],
        }
        await send(response)
        await send({"type": "http.response.body", "body": b"Hello, ASGI!"})
