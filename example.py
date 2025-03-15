from app import PepperAPI
from routing.router import Router
from bases.handler import BaseHandler
from routing.router_tree import RadixTree


app = PepperAPI(routing_struct=RadixTree())


r = Router(app=app, root='/api/v1')


@r.route('/test')
class Test1(BaseHandler):
    async def get(self):
        return {'answer': 'hello'}


@r.route('/test/{id}')
class TestH2(BaseHandler):
    async def post(self, id):
        print(self, 'get', id)


if __name__ == '__main__':
    from uvicorn import run
    run(app=app)
