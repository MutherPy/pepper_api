from abc import ABC, abstractmethod
from src.core.entities.request.objects import Request
from typing import Callable


class BaseApp(ABC):
    def __init__(self):
        self.routers: dict[str, "BaseRouter"] = {}

    def register_router(self, router: "BaseRouter"):
        if not self.routers.get(router.root):
            self.routers[router.root] = router

    def _scope_parser(self, scope: dict) -> Request:
        return Request.build(scope)

    @abstractmethod
    async def read_body(self, request: Request, receive: Callable):
        raise NotImplementedError

    @abstractmethod
    async def __call__(self, scope, receive, send):
        raise NotImplementedError


