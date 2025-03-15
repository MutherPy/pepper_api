from abc import ABC, abstractmethod
from typing import Callable, Type, Union
from bases.handler import BaseHandler
from typing import TypeAlias


RSFindType: TypeAlias = Union[tuple[Type[BaseHandler], dict], tuple[None, None]]


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
