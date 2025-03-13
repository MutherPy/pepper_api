from abc import ABC, abstractmethod
from src.core.bases import BaseApp
from typing import Optional


class BaseRouter(ABC):
    __ROUTER_DEFAULT_COUNTER: int = 0

    @property
    def router_counter(self) -> int:
        return self.__ROUTER_DEFAULT_COUNTER

    def __new__(cls, *args, **kwargs):
        app: Optional[BaseApp] = kwargs.get('app')
        if not isinstance(app, BaseApp):
            raise TypeError('"app" must be instance of BaseApp')
        new_router = super().__new__(cls)
        cls.__ROUTER_DEFAULT_COUNTER += 1
        app.register_router(new_router)
        return new_router

    def __init__(self, *, app: BaseApp, name=None, root='/'):
        self.name = name if name else f'Router_#{self.router_counter}'
        self.root = root
