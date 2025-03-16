from abc import ABC
from typing import Callable

from bases.body import BaseBodyEntity

from exc.request_exc import MethodNotAllowed
from exc.runtime_exc import ServiceError, EmptyArgumentAnnotation, TooMuchUrlParams, NotEnoughUrlParams
from http_entities.request import HTTPRequest
from inspect import signature, Parameter


class BaseHandler(ABC):
    def __init__(self, request: HTTPRequest):
        self.r: HTTPRequest = request

    def _handle_callable_args(self, controller: Callable, url_params: dict) -> dict:
        annotated_parameter: Parameter

        param_name: str
        param_type: type

        args_to_return: dict = {}

        error_params = []

        sign = signature(controller)
        for annotated_parameter in sign.parameters.values():
            param_name = annotated_parameter.name
            param_type = annotated_parameter.annotation

            if param_type is sign.empty:
                raise EmptyArgumentAnnotation(param_name)

            if issubclass(param_type, BaseBodyEntity):
                args_to_return[param_name] = param_type.from_json(self.r.body)
                continue

            if url_param_value := url_params.pop(param_name, None):
                args_to_return[param_name] = param_type(url_param_value)
            else:
                error_params.append(param_name)

        if error_params:
            raise NotEnoughUrlParams(error_params)
        if url_params:
            raise TooMuchUrlParams(url_params.keys())
        return args_to_return

    async def process(self, method: str, url_params: dict):
        method = method.lower()
        try:
            controller_method: Callable = getattr(self, method)
        except AttributeError:
            raise MethodNotAllowed(method)
        try:
            args_to_pass: dict = self._handle_callable_args(controller=controller_method, url_params=url_params)
        except AttributeError:
            raise ServiceError
        return await controller_method(**args_to_pass)
