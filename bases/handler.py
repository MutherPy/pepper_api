from abc import ABC

from exc.request_exc import MethodNotAllowed
from http_entities.request import HTTPRequest


class BaseHandler(ABC):

    def __init__(self, request: HTTPRequest):
        self.r: HTTPRequest = request

    async def process(self, method: str, params: dict):
        method = method.lower()
        try:
            controller_method = getattr(self, method)
            return await controller_method(**params)
        except AttributeError:
            raise MethodNotAllowed(method)
