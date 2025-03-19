from abc import ABC, abstractmethod
from bases.http_entities.response import BaseResponse


class BaseMiddleware(ABC):
    def __init__(self, app):
        self.app = app

    @abstractmethod
    async def __call__(self, scope, receive, send) -> BaseResponse:
        pass
