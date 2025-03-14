from abc import ABC, abstractmethod
from http_entities.request import Request
from typing import Callable


class BaseReader(ABC):
    @abstractmethod
    async def read(self, request: Request, receiver: Callable):
        raise NotImplementedError
