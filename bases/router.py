from abc import ABC
from typing import Type, Callable

from bases.handler import BaseHandler, BaseWSHandler
from exc.runtime_exc import IncorrectInheritance, NotEnoughUrlParams, TooMuchUrlParams

from re import compile
from bases.body import BaseBodyEntity


class RoutedHandlerCheck:
    regexp = compile(r"\{([\w\d]+)}")

    @staticmethod
    def _get_path_params(path: str) -> list:
        return RoutedHandlerCheck.regexp.findall(path)

    @staticmethod
    def inspect_handler_methods(path: str, handler: Type["BaseHandler"]):
        url_params: list = RoutedHandlerCheck._get_path_params(path)
        user_methods = handler.__methods_precompile__.items()
        method: Callable
        args_data: dict[str, type]
        for method, args_data in user_methods:
            error_params: list[str] = []
            checked_params: set[str] = set()
            for param_name, param_type in args_data.items():
                if issubclass(param_type, BaseBodyEntity):
                    continue
                if param_name not in url_params:
                    error_params.append(param_name)
                else:
                    checked_params.add(param_name)
            if error_params:
                raise NotEnoughUrlParams(method, handler, error_params)
            if left := set(url_params) - checked_params:
                raise TooMuchUrlParams(method, handler, left)


class BaseRouter(ABC):
    def __init__(self, *, root: str):
        self.root = root
        self._handlers: dict[str, Type[BaseHandler]] = {}
        self._ws_handlers: dict[str, Type[BaseWSHandler]] = {}

    @property
    def handlers(self) -> dict[str, Type[BaseHandler]]:
        return self._handlers

    @property
    def ws_handlers(self) -> dict[str, Type[BaseWSHandler]]:
        return self._ws_handlers

    def get_full_path(self, path: str) -> str:
        return f'{self.root}{path}'

    def route(self, path: str):
        def inner(cls):
            if not issubclass(cls, BaseHandler):
                raise IncorrectInheritance(cls, BaseHandler)
            full_path = self.get_full_path(path)
            RoutedHandlerCheck.inspect_handler_methods(full_path, cls)
            self._handlers[full_path] = cls
            return cls
        return inner

    def ws_route(self, path: str):
        def inner(cls):
            if not issubclass(cls, BaseWSHandler):
                raise IncorrectInheritance(cls, BaseWSHandler)
            self._ws_handlers[self.get_full_path(path)] = cls
            return cls
        return inner
