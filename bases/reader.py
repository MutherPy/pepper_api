from abc import ABC, abstractmethod
from http_entities.request import HTTPRequest
from typing import Callable


class BaseReader(ABC):
    @abstractmethod
    async def read(self, request: HTTPRequest, receiver: Callable):
        pass
