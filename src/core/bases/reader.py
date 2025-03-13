from abc import ABC, abstractmethod
from src.core.entities.request.objects import Request
from typing import Callable


class BaseReader(ABC):
    @abstractmethod
    async def read(self, request: Request, receiver: Callable):
        raise NotImplementedError
