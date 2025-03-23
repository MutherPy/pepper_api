from typing import Type, Optional, Union

from bases.http_entities.request import BaseRequest, BaseWSRequest
from bases.http_types import RequestType, ScopeType
from mimetypes import guess_extension

from core.requests.request_registry import RequestRegistry
from exc.request_exc import IncorrectRequestType
from http_entities import Headers


class ContentTypeDetector:
    @staticmethod
    def is_c_type_file(content_type: str) -> bool:
        content_type = content_type.lower()
        if content_type.startswith('application/json'):
            return False
        return (
                guess_extension(content_type) is not None  # FIXME multipart completely incorrect
                # or
                # content_type.startswith("multipart/form-data")
        )

    @staticmethod
    def is_file(content_type: Optional[str]):
        c_t_file = False

        if content_type:
            c_t_file = ContentTypeDetector.is_c_type_file(content_type)

        return c_t_file


class ContentLengthDetector:
    @staticmethod
    def is_big(content_length: Optional[str]) -> bool:
        if content_length:
            if int(content_length) > 4_000_000:  # TODO to configs
                return True
        return False


class RequestFactory:
    @staticmethod
    def find_http_req_type(headers: Headers) -> str:
        c_t = headers.get('content-type')
        c_l = headers.get('content-length')
        potential_req_type = RequestType.COMMON_HTTP
        if ContentTypeDetector.is_file(c_t):
            potential_req_type = RequestType.FILE_HTTP
            if ContentLengthDetector.is_big(c_l):
                potential_req_type = RequestType.BIGFILE_HTTP
        return potential_req_type

    @staticmethod
    def find_ws_req_type(headers: Headers):
        potential_req_type = None
        upg = headers.get('upgrade')
        if upg and upg == 'websocket':
            potential_req_type = RequestType.COMMON_WS
        return potential_req_type

    @staticmethod
    async def create(scope: dict) -> Union[BaseRequest, BaseWSRequest]:
        req_obj: Union[BaseRequest, BaseWSRequest]

        scope_type = scope["type"]
        headers = Headers.from_scope(scope)  # FIXME headers creation
        if scope_type == ScopeType.HTTP:
            req_class_type: str = RequestFactory.find_http_req_type(headers=headers)
        elif scope_type == ScopeType.WS:
            req_class_type: str = RequestFactory.find_ws_req_type(headers=headers)
        else:
            raise IncorrectRequestType(scope_type)

        req_class: Type[BaseRequest] = RequestRegistry.retrieve(req_class_type)
        req_obj = req_class.from_scope(scope=scope)
        req_obj.type = req_class_type
        return req_obj
