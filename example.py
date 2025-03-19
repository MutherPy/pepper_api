from dataclasses import dataclass

from mashumaro.mixins.orjson import DataClassORJSONMixin

from app import PepperAPI
from bases.body import BaseBodyEntity, BaseBodyResponseEntity
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

r = Router(root='/api/v1')


# EXAMPLE OF REGULAR REQUEST WITH BODY DATA AND RESPONSE
@r.route('/test')
class Test1(BaseHandler):
    async def get(self, user: UserFromRequest) -> UserToResponse:
        # serialized User object
        agree = True if user.age > 18 else False
        return UserToResponse(name=user.name, age=user.age, answer=UserAnswer(agree=agree))


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
