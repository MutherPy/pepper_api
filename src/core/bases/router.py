from abc import ABC

from src.core.exceptions.runtime_exc import IncorrectInheritance
from src.core.bases.app import BaseApp
from src.core.bases.handler import BaseHandler


class BaseRouter(ABC):
    __ROUTER_DEFAULT_COUNTER: int = 0

    def __init__(self, *, app: BaseApp, root: str, name=None):
        self.name = name if name else f'Router_#{self._router_counter}'
        self.app = app
        self.root = root

    def get_full_path(self, path: str) -> str:
        return f'{self.root}{path}'

    @property
    def _router_counter(self) -> int:
        self.__ROUTER_DEFAULT_COUNTER += 1
        return self.__ROUTER_DEFAULT_COUNTER

    def route(self, path: str):
        def inner(cls):
            if not issubclass(cls, BaseHandler):
                raise IncorrectInheritance(cls, BaseHandler)
            self.app.register_route(path=self.get_full_path(path), handler=cls)
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
