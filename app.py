from http import HTTPStatus
from typing import Type, Any, Union, Optional

from bases import AsyncFunction
from bases.handler import BaseHandler
from core.exc_result import ExceptionResult
from core.response_factory import ResponseBuilder
from core.method_meta import HandlerMethodResult
from exc.request_exc import NotFound
from bases.app import BaseApp
from bases.reader import BaseReader

from core.readers import reader_provider
from http_entities import (
    Headers,
    HTTPResponse,
    HTTPRequest, StreamingHTTPResponse
)


class PepperAPI(BaseApp):

    @staticmethod
    async def read_body(request: HTTPRequest, receive: AsyncFunction):
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

    def build_headers(self, headers: Optional[dict] = None) -> Headers:
        basic_headers = {
            'Powered-X': 'PepperAPI',
        }
        if headers:
            basic_headers.update(headers)
        return Headers.from_dict(basic_headers)

    async def build_response(
            self,
            result: Optional[Union[Any, HandlerMethodResult]] = None,
            exc_result: Optional[ExceptionResult] = None
    ) -> Union[HTTPResponse, StreamingHTTPResponse]:
        response: Union[HTTPResponse, StreamingHTTPResponse]

        headers_ext = None

        if result is not None:
            status = HTTPStatus.OK
            if not isinstance(result, HandlerMethodResult):
                body = result
            else:
                body = result.method_result
                headers_ext = result.method_meta
        else:
            status = exc_result.status
            body = exc_result.body

        response = await ResponseBuilder.build(status=status, body=body)
        h = self.build_headers(headers_ext)
        response.update_headers(headers=h)
        return response
