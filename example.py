from dataclasses import dataclass

from mashumaro.mixins.orjson import DataClassORJSONMixin

from app import PepperAPI
from bases.body import BaseBodyEntity, BaseBodyResponseEntity
from bases.middleware import BaseMiddleware, BaseHandlerMiddleware
from exc.request_exc import AuthAccessDenied, PermAccessDenied, QueryParamExpected
from http_entities import Headers
from routing.router import Router
from bases.handler import BaseHandler
from routing.router_tree import RadixTree
from core.method_meta import meta
from asyncio import sleep


@dataclass
class Place:
    city: str
    country: str


@dataclass
class UserFromRequest(DataClassORJSONMixin, BaseBodyEntity):
    name: str
    age: int
    place:  Place


# User json example:
# {
#   "name": "Alex",
#   "age": 10,
#   "place": {
#       "city": "Lviv",
#       "country": "Ukraine"
#   }
# }

@dataclass
class UserAnswer:
    agree: bool


@dataclass
class UserToResponse(DataClassORJSONMixin, BaseBodyResponseEntity):
    name: str
    age: int
    answer: UserAnswer


app = PepperAPI(routing_struct=RadixTree())


# THIS MIDDLEWARES ARE GLOBAL
class AuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        headers = Headers.from_scope(scope)
        if not headers.get('Authorize'):
            raise AuthAccessDenied
        resp = await self.app(scope, receive, send)
        resp.start.headers.update(Authorized='true')
        return resp


class Permissions(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        headers = Headers.from_scope(scope)
        if not headers.get('Permissions'):
            raise PermAccessDenied
        return await self.app(scope, receive, send)


# LIFO like middlewares processing
app.add_middleware(Permissions)
app.add_middleware(AuthMiddleware)

r = Router(root='/api/v1')


# EXAMPLE OF REGULAR REQUEST WITH BODY DATA AND RESPONSE
@r.route('/test')
class Test1(BaseHandler):
    async def get(self, user: UserFromRequest) -> UserToResponse:
        # serialized User object
        agree = True if user.age > 18 else False
        return UserToResponse(name=user.name, age=user.age, answer=UserAnswer(agree=agree))


# EXAMPLE OF REGULAR REQUEST WITH HANDLER DECORATOR

class DecorTestQuery(BaseHandlerMiddleware):
    def logic(self):
        if not self.r.query_string.get('qt'):
            raise QueryParamExpected('qt')


@r.route('/test/query')
# it is important to decorate class, after routing
@DecorTestQuery
class TestQuery(BaseHandler):
    async def get(self):
        return self.r.query_string.get('qt')


# EXAMPLE OF STREAMING RESPONSE
@r.route('/test/{id}')
class TestH2(BaseHandler):
    @meta(content_type='image/png')
    async def get(self, id: int):
        print(id)

        async def file_getter():
            # use smth like IOfiles
            with open('example_img.png', 'rb') as f:
                for line in f:
                    yield line
                    await sleep(0)

        return file_getter  # or file_getter()


app.include_router(router=r)


if __name__ == '__main__':
    from uvicorn import run
    run(app=app)
