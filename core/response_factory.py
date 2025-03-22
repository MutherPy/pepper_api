from typing import Type

from bases.http_entities.response import BaseResponse
from bases.http_types import ResponseType
from inspect import isasyncgenfunction, isasyncgen


class ResponseRegistry:
    _registry: dict[str, Type[BaseResponse]] = {}

    @classmethod
    def register(cls, key, creator):
        cls._registry[key] = creator

    @classmethod
    def retrieve(cls, key) -> Type[BaseResponse]:
        if key not in cls._registry:
            raise ValueError(f"Unknown response type: {key}")
        return cls._registry[key]


def register_response_type(key):
    def decorator(cls):
        ResponseRegistry.register(key, cls)
        return cls
    return decorator


class ResponseBuilder:
    @staticmethod
    def get_resp_type(input_data):
        resp_type = ResponseType.HTTP
        if isasyncgenfunction(input_data) or isasyncgen(input_data):
            resp_type = ResponseType.STREAM
        return resp_type

    @staticmethod
    def get_resp_content_type(response_type):
        c_type = 'application/json'
        if response_type == ResponseType.STREAM:
            c_type = 'application/octet-stream'
        return c_type

    @staticmethod
    async def build(status, body):
        response_type = ResponseBuilder.get_resp_type(body)
        content_type = ResponseBuilder.get_resp_content_type(response_type)
        resp_class = ResponseRegistry.retrieve(response_type)
        response = resp_class.build(status=status, body=body)
        response.start.headers.set('content-type', content_type)
        return response
