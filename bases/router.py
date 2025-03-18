from abc import ABC, abstractmethod
from typing import Type, Optional

from bases.handler import BaseHandler
from exc.runtime_exc import IncorrectInheritance


class BaseRouter(ABC):
    def __init__(self, *, root: str):
        self.root = root
        self._handlers: dict[str, Type[BaseHandler]] = {}

    @property
    def handlers(self) -> dict[str, Type[BaseHandler]]:
        return self._handlers

    def get_full_path(self, path: str) -> str:
        return f'{self.root}{path}'

    def route(self, path: str):
        def inner(cls):
            if not issubclass(cls, BaseHandler):
                raise IncorrectInheritance(cls, BaseHandler)
            self._handlers[self.get_full_path(path)] = cls
            return cls
        return inner


# class BaseSubRouter(ABC, ReExtender):
#     __SUB_ROUTER_DEFAULT_COUNTER: int = 0
#
#     def __new__(cls, *args, **kwargs):
#         parent: BaseRouter = kwargs.get('parent')
#         if not isinstance(parent, BaseRouter):
#             raise TypeError('"parent" must be instance of BaseRouter')
#         new_router = super().__new__(cls)
#         cls.__SUB_ROUTER_DEFAULT_COUNTER += 1
#         new_router.__init__(**kwargs)
#         parent.register_sub_router(new_router)
#         return new_router
#
#     def __init__(self, *, parent: BaseRouter, root, name=None):
#         self.parent = parent
#         self.name = name if name else f'SubRouter_#{self._router_counter}_{self.parent.name}'
#         self.compiled_root = self._compile_path(root)
#
#     @property
#     def _router_counter(self) -> int:
#         return self.__SUB_ROUTER_DEFAULT_COUNTER
