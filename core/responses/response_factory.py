from bases.http_types import ResponseType
from inspect import isasyncgenfunction, isasyncgen

from core.responses.response_registry import ResponseRegistry


class ResponseFactory:
    @staticmethod
    def find_http_resp_type(body_type):
        resp_type = ResponseType.HTTP
        if isasyncgenfunction(body_type) or isasyncgen(body_type):
            resp_type = ResponseType.STREAM
        return resp_type

    @staticmethod
    def get_resp_content_type(response_type):
        c_type = 'application/json'
        if response_type == ResponseType.STREAM:
            c_type = 'application/octet-stream'
        return c_type

    @staticmethod
    async def create(status, body):
        response_type = ResponseFactory.find_http_resp_type(body)
        content_type = ResponseFactory.get_resp_content_type(response_type)
        resp_class = ResponseRegistry.retrieve(response_type)
        response = resp_class.build(status=status, body=body)
        response.start.headers.set('content-type', content_type)
        return response
