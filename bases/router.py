from abc import ABC, abstractmethod
from typing import Type, Optional, Union, Callable

from bases.handler import BaseHandler, BaseWSHandler
from exc.runtime_exc import IncorrectInheritance, EmptyArgumentAnnotation, NotEnoughUrlParams, TooMuchUrlParams

from re import compile
from inspect import signature, Parameter
from bases.body import BaseBodyEntity
from collections import defaultdict
from http import HTTPMethod
from types import MappingProxyType


class RoutedHandlerCheck:
    regexp = compile(r"\{([\w\d]+)}")

    @staticmethod
    def _get_path_params(path: str) -> list:
        return RoutedHandlerCheck.regexp.findall(path)

    @staticmethod
    def _get_handler_methods(handler: BaseHandler) -> dict:
        user_defined_attrs = {}
        for k, v in handler.__dict__.items():
            if k.upper() not in HTTPMethod.__members__:
                continue
            user_defined_attrs[k] = v
        return user_defined_attrs

    @staticmethod
    def inspect_handler_methods(path, handler) -> defaultdict[Callable, dict[str, type]]:
        url_params: list = RoutedHandlerCheck._get_path_params(path)
        user_methods: dict = RoutedHandlerCheck._get_handler_methods(handler)
        method_ann_types = defaultdict(dict)
        for method in user_methods.values():
            sign = signature(method)
            error_params = []
            checked_params = set()
            for annotated_parameter in sign.parameters.values():
                param_name = annotated_parameter.name
                if param_name == 'self':
                    continue
                param_type = annotated_parameter.annotation

                if param_type is sign.empty:
                    raise EmptyArgumentAnnotation(method, handler, param_name)
                if issubclass(param_type, BaseBodyEntity):
                    method_ann_types[method][param_name] = param_type
                    continue

                if param_name not in url_params:
                    error_params.append(param_name)
                else:
                    checked_params.add(param_name)

                method_ann_types[method][param_name] = param_type

            if error_params:
                raise NotEnoughUrlParams(method, handler, error_params)
            if left := set(url_params) - checked_params:
                raise TooMuchUrlParams(method, handler, left)
        return method_ann_types

    @staticmethod
    def set_precompiled_type_casting(handler: Type[BaseHandler], methods_meta: dict):
        handler.__methods_precompile__ = MappingProxyType({k: MappingProxyType(v) for k, v in methods_meta.items()})


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
            print(cls)  # FIXME do not work with class decorators
            methods_meta: defaultdict = RoutedHandlerCheck.inspect_handler_methods(full_path, cls)
            print(methods_meta)
            # NOTE methods_meta -> mapping <function Handler.get> not <bound method Handler.get>
            RoutedHandlerCheck.set_precompiled_type_casting(cls, methods_meta)
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
