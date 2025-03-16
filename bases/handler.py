from abc import ABC
from typing import Callable, Optional

from exc.request_exc import MethodNotAllowed
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
            if param_type := param_annotations.get(k).annotation:
                if param_type is not sign.empty:
                    params[k] = param_type(params[k])

    async def process(self, method: str, params: dict):
        method = method.lower()
        try:
            controller_method = getattr(self, method)
            self._handle_callable_args(controller=controller_method, params=params)
            return await controller_method(**params)
        except AttributeError:
            raise MethodNotAllowed(method)
