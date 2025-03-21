from abc import ABC, abstractmethod
from typing import Type, Union

from bases.handler import BaseHandler, BaseWSHandler
from bases import RSFindType


class BaseRoutingStructure(ABC):
    @abstractmethod
    def add_route(self, path: str, handler: Type[Union[BaseHandler, BaseWSHandler]]):
        pass

    @abstractmethod
    def find_handler(self, path: str) -> RSFindType:
        pass

    @abstractmethod
    def show_routes(self):
        pass
