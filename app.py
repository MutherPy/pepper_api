from http import HTTPStatus
from typing import Type, Any, Union, Optional

from bases.app import BaseApp

from bases.handler import BaseHandler, BaseWSHandler
from core.exc_result import ExceptionResult, WSExceptionResult
from core.requests.request_factory import RequestFactory
from core.readers.readers_registry import ReaderRegistry
from core.response_factory import ResponseBuilder
from core.method_meta import HandlerMethodResult
from exc.request_exc import NotFound

from exc.runtime_exc import WrongRouting

from http_entities import *
from core.readers import *


class PepperAPI(BaseApp):
    async def build_request(self, scope: dict, receive: AsyncFunction = None) -> Union[HTTPRequest, StreamingHTTPResponse, WSRequest]:
        req_obj = await RequestFactory.create(scope)
        reader = ReaderRegistry.retrieve(request_type=req_obj.type)
        if reader:
            await reader.read(req_obj, receive)
        return req_obj

    async def request_handler(self, request: HTTPRequest):
        handler: Type[BaseHandler]
        url_params: dict

        handler, url_params = self.find_handler(request.path)
        if not handler:
            raise NotFound(request.path)
        elif not issubclass(handler, BaseHandler):
            raise WrongRouting(request.path, handler, BaseHandler)
        handler_inst = handler(request=request)
        result = await handler_inst.process(request.method, url_params)
        return result

    async def ws_request_handler(self, request: WSRequest, receive, send):
        handler: Type[BaseWSHandler]
        url_params: dict

        handler, url_params = self.find_ws_handler(request.path)
        if not handler:
            raise NotFound(request.path)
        elif not issubclass(handler, BaseWSHandler):
            raise WrongRouting(request.path, handler, BaseWSHandler)
        handler_inst = handler(request=request, url_params=url_params)
        e = None
        try:
            await handler_inst.process(receive, send)
        except Exception as _e:
            e = _e
        finally:
            return handler_inst.is_connected, e

    async def exceptions_handler(self, e: Exception) -> ExceptionResult:
        return ExceptionResult.from_exc(e)

    async def ws_exceptions_handler(self, e: Exception) -> WSExceptionResult:
        return WSExceptionResult.from_exc(e)

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
