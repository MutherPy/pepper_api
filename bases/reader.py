from abc import ABC, abstractmethod

from bases import AsyncFunction
from http_entities.request import HTTPRequest


class BaseReader(ABC):
    @abstractmethod
    async def read(self, request: HTTPRequest, receiver: AsyncFunction):
        pass
