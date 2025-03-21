from typing import TypeAlias, Callable, Awaitable, Any, Union, Type

from bases.handler import BaseHandler, BaseWSHandler

AsyncFunction: TypeAlias = Callable[[], Awaitable[Any]]

RSFindType: TypeAlias = Union[tuple[Type[Union[BaseHandler, BaseWSHandler]], dict], tuple[None, None]]


