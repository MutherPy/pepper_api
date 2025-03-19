from functools import wraps
from dataclasses import dataclass, field
from typing import Optional, Any


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
