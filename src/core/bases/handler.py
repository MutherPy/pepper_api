from abc import ABC

from src.core.exceptions.request_exc import MethodNotAllowed
from src.core.entities.request.objects import Request


class BaseHandler(ABC):

    def __init__(self, request: Request):
        self.r: Request = request

    async def process(self, method: str, params: dict):
        try:
            controller = getattr(self, method)
            await controller(**params)
        except AttributeError:
            raise MethodNotAllowed(method)



