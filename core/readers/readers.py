from bases import AsyncFunction
from bases.http_types import RequestType
from http_entities.request import HTTPRequest
from bases.reader import BaseReader

from core.readers.readers_registry import register_request_reader_type


@register_request_reader_type(RequestType.COMMON_HTTP)
class HTTPReader(BaseReader):
    async def read(self, request: HTTPRequest, receiver: AsyncFunction):
        more_body = True
        body_parts = bytearray()
        while more_body:
            message = await receiver()
            body_parts.extend(message.get('body', b''))
            more_body = message.get('more_body', False)
        request.body = bytes(body_parts)
