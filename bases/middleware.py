from abc import ABC, abstractmethod
from typing import Callable

from bases.http_entities.response import BaseResponse
from functools import wraps


class BaseMiddleware(ABC):
    def __init__(self, app: Callable):
        self.app = app

    @abstractmethod
    async def __call__(self, scope: dict, receive, send) -> BaseResponse:
        pass


class BaseHandlerMiddleware(ABC):
    def __new__(cls, decor_cls):
        def call_wrapper(f):
            @wraps(f)
            def wrapper(self, *args, **kwargs):
                # f == decor_cls.__init__
                f(self, *args, **kwargs)
                # to allow custom logic reach decorated instance
                cls.logic(self)
            return wrapper

        new = type(
            f'Decor_{decor_cls.__name__}',
            (decor_cls,),
            {'__init__': call_wrapper(decor_cls.__init__)}
        )
        new.__module__ = decor_cls.__module__
        return new

    @abstractmethod
    def logic(self):
        pass
