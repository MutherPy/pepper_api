from abc import ABC, abstractmethod

from bases import AsyncFunction
from bases.http_entities.request import BaseRequest


class BaseReader(ABC):
    @abstractmethod
    async def read(self, request: BaseRequest, receiver: AsyncFunction):
        pass
