from typing import TypeAlias, Callable, Awaitable, Union, Type

from bases.handler import BaseHandler, BaseWSHandler

AsyncFunction: TypeAlias = Callable[[], Awaitable[bytes]]

RSFindType: TypeAlias = Union[tuple[Type[Union[BaseHandler, BaseWSHandler]], dict], tuple[None, None]]
