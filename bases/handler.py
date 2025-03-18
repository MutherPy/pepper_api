from abc import ABC
from typing import Callable, Optional, Any

from bases.body import BaseBodyEntity

from exc.request_exc import MethodNotAllowed, UnprocessableEntity
from exc.runtime_exc import ServiceError, EmptyArgumentAnnotation, TooMuchUrlParams, NotEnoughUrlParams
from http_entities.request import HTTPRequest
from inspect import signature, Parameter
from functools import wraps
from dataclasses import dataclass, field


@dataclass
class HandlerMethodResult:
    method_meta: dict = field(default_factory=dict)
    method_result: Any = field(default=None)


def meta(content_type: Optional[str] = None):
    """ Better for streaming. Slowing response. """
    def wrapper(f):
        @wraps(f)
        async def inner(*args, **kwargs):
            result = await f(*args, **kwargs)
            h_meta = HandlerMethodResult(
                method_meta=dict(
                    content_type=content_type
                ),
                method_result=result
            )
            return h_meta
        return inner
    return wrapper


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
                try:
                    args_to_return[param_name] = param_type.from_json(self.r.body)
                except Exception as e:
                    raise UnprocessableEntity(str(e)) from e
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
