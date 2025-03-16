from typing import TypeAlias, Callable, Awaitable, Any, Union, Type

from bases.handler import BaseHandler


AsyncFunction: TypeAlias = Callable[[], Awaitable[Any]]

RSFindType: TypeAlias = Union[tuple[Type[BaseHandler], dict], tuple[None, None]]


