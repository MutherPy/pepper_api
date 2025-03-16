from abc import ABC, abstractmethod
from typing import Callable

from bases import RSFindType


class BaseRoutingStructure(ABC):
    @abstractmethod
    def add_route(self, path: str, handler: Callable):
        pass

    @abstractmethod
    def find_handler(self, path: str) -> RSFindType:
        pass

    @abstractmethod
    def show_routes(self):
        pass
