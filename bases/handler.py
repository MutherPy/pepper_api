from abc import ABC

from exc.request_exc import MethodNotAllowed
from http_entities.request import Request


class BaseHandler(ABC):

    def __init__(self, request: Request):
        self.r: Request = request

    async def process(self, method: str, params: dict):
        method = method.lower()
        try:
            controller_method = getattr(self, method)
            return await controller_method(**params)
        except AttributeError:
            raise MethodNotAllowed(method)
