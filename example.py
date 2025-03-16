from dataclasses import dataclass

from mashumaro.mixins.orjson import DataClassORJSONMixin

from app import PepperAPI
from bases.body import BaseBodyEntity, BaseBodyResponseEntity
from routing.router import Router
from bases.handler import BaseHandler
from routing.router_tree import RadixTree


app = PepperAPI(routing_struct=RadixTree())
r = Router(app=app, root='/api/v1')


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


@r.route('/test')
class Test1(BaseHandler):
    async def get(self, user: UserFromRequest) -> UserToResponse:
        # serialized User object
        agree = True if user.age > 18 else False
        return UserToResponse(name=user.name, age=user.age, answer=UserAnswer(agree=agree))


@r.route('/test/{id}')
class TestH2(BaseHandler):
    async def post(self, id):
        print(self, 'get', id)


if __name__ == '__main__':
    from uvicorn import run
    run(app=app)
