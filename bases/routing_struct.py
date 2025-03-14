from abc import ABC, abstractmethod
from typing import Callable, Type, Optional
from bases.handler import BaseHandler


class BaseRoutingStructure(ABC):
    @abstractmethod
    def add_route(self, path: str, handler: Callable):
        raise NotImplementedError

    @abstractmethod
    def find_handler(self, path: str) -> tuple[Optional[Type[BaseHandler]], Optional[dict]]:
        raise NotImplementedError

    @abstractmethod
    def show_routes(self):
        raise NotImplementedError
