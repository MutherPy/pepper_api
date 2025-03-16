from abc import ABC
from typing import Callable, Optional

from exc.request_exc import MethodNotAllowed
from exc.runtime_exc import ServiceError
from http_entities.request import HTTPRequest
from inspect import signature


class BaseHandler(ABC):
    def __init__(self, request: HTTPRequest):
        self.r: HTTPRequest = request

    @staticmethod
    def _handle_callable_args(controller: Callable, params: dict):
        param_type: Optional[type]

        sign = signature(controller)
        param_annotations = sign.parameters
        for k in params.keys():
            # check if param from url presents in controller params
            if param := param_annotations.get(k):
                # if so - get it's annotated class
                param_type = param.annotation
                # if it was annotated, else - default class in <class: str>
                if param_type is not sign.empty:
                    params[k] = param_type(params[k])

    async def process(self, method: str, params: dict):
        method = method.lower()
        try:
            controller_method = getattr(self, method)
        except AttributeError:
            raise MethodNotAllowed(method)
        try:
            self._handle_callable_args(controller=controller_method, params=params)
        except AttributeError:
            raise ServiceError
        return await controller_method(**params)
