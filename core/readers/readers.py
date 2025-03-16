from bases import AsyncFunction
from http_entities.request import HTTPRequest
from bases.reader import BaseReader


class HTTPReader(BaseReader):
    async def read(self, request: HTTPRequest, receiver: AsyncFunction):
        more_body = True
        body_parts = bytearray()
        while more_body:
            message = await receiver()
            body_parts.extend(message.get('body', b''))
            more_body = message.get('more_body', False)
        request.body = bytes(body_parts)
