from bases.router import BaseRouter
from bases.handler import BaseHandler

from exc.runtime_exc import IncorrectInheritance


class Router(BaseRouter):
    def route(self, path: str):
        def inner(cls):
            if not issubclass(cls, BaseHandler):
                raise IncorrectInheritance(cls, BaseHandler)
            self.app.register_route(path=self.get_full_path(path), handler=cls)
            return cls
        return inner

