from dataclasses import dataclass

from mashumaro.mixins.orjson import DataClassORJSONMixin

from app import PepperAPI
from bases.body import BaseBodyEntity
from routing.router import Router
from bases.handler import BaseHandler
from routing.router_tree import RadixTree


app = PepperAPI(routing_struct=RadixTree())
r = Router(app=app, root='/api/v1')


@dataclass
class Place(DataClassORJSONMixin, BaseBodyEntity):
    city: str
    country: str


@dataclass
class User(DataClassORJSONMixin, BaseBodyEntity):
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


@r.route('/test')
class Test1(BaseHandler):
    async def get(self, user: User):
        # serialized User object
        return {'answer': f'Hello {user.name} from {user.place.city}'}


@r.route('/test/{id}')
class TestH2(BaseHandler):
    async def post(self, id):
        print(self, 'get', id)


if __name__ == '__main__':
    from uvicorn import run
    run(app=app)
