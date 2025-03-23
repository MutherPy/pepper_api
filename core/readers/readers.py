from bases import AsyncFunction
from bases.http_entities.request import BaseRequest
from bases.http_types import RequestType
from http_entities.request import HTTPRequest
from bases.reader import BaseReader

from core.readers.readers_registry import register_request_reader_type
from io import BytesIO
from tempfile import TemporaryFile


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


@register_request_reader_type(RequestType.FILE_HTTP)
class HTTPFileReader(BaseReader):
    async def read(self, request: BaseRequest, receiver: AsyncFunction):
        body = BytesIO()
        more_body = True
        while more_body:
            message = await receiver()
            body.write(message.get('body', b''))
            more_body = message.get('more_body', False)
        body.seek(0)
        request.body = body


@register_request_reader_type(RequestType.BIGFILE_HTTP)
class HTTPBigFileReader(BaseReader):
    async def read(self, request: BaseRequest, receiver: AsyncFunction):
        body = TemporaryFile()
        more_body = True
        while more_body:
            message = await receiver()
            body.write(message.get('body', b''))
            more_body = message.get('more_body', False)
        body.seek(0)
        request.body = body
