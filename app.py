from http import HTTPStatus
from typing import Type, Any, Union

from bases import AsyncFunction
from bases.handler import BaseHandler
from bases.http_types import SendEventTypes
from core.exc_result import ExceptionResult
from http_entities.headers import Headers
from http_entities.response import HTTPResponse, HTTPResponseStart, HTTPResponseBody
from exc.request_exc import NotFound
from bases.app import BaseApp
from bases.reader import BaseReader
from http_entities.request import HTTPRequest

from core.readers import reader_provider


class PepperAPI(BaseApp):

    async def read_body(self, request: HTTPRequest, receive: AsyncFunction):
        reader: BaseReader = reader_provider.get_reader(request.type)
        await reader.read(request=request, receiver=receive)

    async def build_request(self, scope: dict, receive: AsyncFunction) -> HTTPRequest:
        r = HTTPRequest.from_scope(scope)
        await self.read_body(request=r, receive=receive)
        return r

    async def request_handler(self, request: HTTPRequest):
        handler: Type[BaseHandler]
        url_params: dict

        handler, url_params = self.find_handler(request.path)
        if not handler:
            raise NotFound(request.path)
        handler_inst = handler(request=request)
        result = await handler_inst.process(request.method, url_params)
        return result

    async def exceptions_handler(self, e: Exception) -> ExceptionResult:
        return ExceptionResult.from_exc(e)

    def build_headers(self) -> Headers:
        basic_headers = {
            'Content-Type': 'application/json',
        }
        h = Headers.from_dict(basic_headers)
        return h

    async def _build_bad_response(self, data: ExceptionResult) -> HTTPResponse:
        start = HTTPResponseStart(type=SendEventTypes.START, status=data.status)
        # TODO serialization in body as await
        body = HTTPResponseBody(type=SendEventTypes.BODY, body=data.msg, more_body=False)  # TODO streaming
        return HTTPResponse(start=start, body=body)

    async def _build_response(self, data: Any) -> HTTPResponse:
        start = HTTPResponseStart(type=SendEventTypes.START, status=HTTPStatus.OK)
        # TODO serialization in body as await
        body = HTTPResponseBody(type=SendEventTypes.BODY, body=data, more_body=False)  # TODO streaming
        return HTTPResponse(start=start, body=body)

    async def build_response(self, result: Union[Any, ExceptionResult], headers: Headers) -> HTTPResponse:
        response: HTTPResponse

        if not isinstance(result, ExceptionResult):
            response = await self._build_response(result)
        else:
            response = await self._build_bad_response(result)
        response.start.headers = headers
        return response
