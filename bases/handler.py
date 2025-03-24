from abc import ABC, abstractmethod
from asyncio import Queue, Task, create_task, gather, CancelledError
from collections import defaultdict
from http import HTTPMethod
from types import MappingProxyType
from typing import Callable, Union, AsyncIterable, Any, Type

from bases.body import BaseBodyEntity
from bases.http_entities.request import BaseRequest, BaseWSRequest

from exc.request_exc import MethodNotAllowed, UnprocessableEntity
from exc.runtime_exc import ServiceError, EmptyArgumentAnnotation

from bases.http_types import WSReceiveEventTypes, WSSendEventTypes

from inspect import isasyncgenfunction, signature


class HandlerMethodsPreCompiler:
    @staticmethod
    def _get_handler_methods(handler: Type["BaseHandler"]) -> dict:
        user_defined_attrs = {}
        for k, v in handler.__dict__.items():
            if k.upper() not in HTTPMethod.__members__:
                continue
            user_defined_attrs[k] = v
        return user_defined_attrs

    @staticmethod
    def inspect_handler_methods(handler: Type["BaseHandler"]) -> defaultdict[Callable, dict[str, type]]:
        user_methods: dict = HandlerMethodsPreCompiler._get_handler_methods(handler)
        method_ann_types = defaultdict(dict)
        for method in user_methods.values():
            sign = signature(method)
            for annotated_parameter in sign.parameters.values():
                param_name = annotated_parameter.name
                if param_name == 'self':
                    continue
                param_type = annotated_parameter.annotation

                if param_type is sign.empty:
                    raise EmptyArgumentAnnotation(method, handler, param_name)

                method_ann_types[method][param_name] = param_type
        return method_ann_types


class BaseHandler(ABC):
    # using to speed up type casting while runtime
    # set to each Class-Handler registered for any http defined method
    # NOTE method_ann_types -> mapping <function Handler.get> not <bound method Handler.get>
    __methods_precompile__: MappingProxyType[Callable, MappingProxyType[str, type]]

    def __init_subclass__(cls, **kwargs):
        method_ann_types = HandlerMethodsPreCompiler.inspect_handler_methods(cls)
        cls.__methods_precompile__ = MappingProxyType({k: MappingProxyType(v) for k, v in method_ann_types.items()})

    def __init__(self, request: BaseRequest):
        self.r: BaseRequest = request

    def _handle_callable_args(self, method: Callable, url_params: dict[str, str]) -> dict:
        # method - bound method to handler instance. mapping - has class functions
        method_annotations: MappingProxyType[str, type] = self.__methods_precompile__.get(method.__func__)
        if not method_annotations:
            raise RuntimeError(f'No mapping key: {method.__func__}')
        args_to_return: dict = {}
        for param_name, type_obj in method_annotations.items():
            if issubclass(type_obj, BaseBodyEntity):
                try:
                    args_to_return[param_name] = type_obj.from_json(self.r.body)
                except Exception as e:
                    raise UnprocessableEntity(str(e)) from e
            else:
                args_to_return[param_name] = type_obj(url_params[param_name])
        return args_to_return

    async def process(self, method: str, url_params: dict) -> Any:
        method = method.lower()
        try:
            controller_method: Callable = getattr(self, method)
        except AttributeError:
            raise MethodNotAllowed(method)
        try:
            args_to_pass: dict = self._handle_callable_args(method=controller_method, url_params=url_params)
        except AttributeError:  # TODO why?
            raise ServiceError
        return await controller_method(**args_to_pass)


class BaseWSHandler(ABC):
    def __init__(self, request: BaseWSRequest, url_params: dict = None):
        self.r = request
        self.url_params = url_params

        self.q = Queue()

        self.is_connected = False

        self.__tasks: tuple[Task, Task] = None

    async def __tasks_cancel(self):
        for t in self.__tasks:
            if not t.cancelled():
                t.cancel()

    async def __reader(self, receive):
        while True:
            event = await receive()
            if event["type"] == WSReceiveEventTypes.RECEIVE:
                message = event["text"]
                await self.reader(message=message)
            elif event["type"] == WSReceiveEventTypes.CONNECT:
                self.is_connected = True
            elif event["type"] == WSReceiveEventTypes.DISCONNECT:
                break
        await self.__tasks_cancel()

    @abstractmethod
    async def reader(self, message):
        ...

    async def __gen_writer(self, send):
        async for msg in self.writer():
            await send({"type": WSSendEventTypes.SEND, "text": msg})

    async def __simple_writer(self, send):
        while True:
            result = await self.writer()
            await send({"type": WSSendEventTypes.SEND, "text": result})

    async def __writer(self, send):
        if isasyncgenfunction(self.writer):
            await self.__gen_writer(send)
        else:
            await self.__simple_writer(send)

    @abstractmethod
    async def writer(self) -> Union[str, AsyncIterable]:
        ...

    async def process(self, receive, send):
        self.__tasks = (
            create_task(self.__reader(receive)),
            create_task(self.__writer(send))
        )
        await send({"type": WSSendEventTypes.ACCEPT})
        try:
            await gather(*self.__tasks)
        except CancelledError:
            pass
