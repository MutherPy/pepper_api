from typing import Callable

from src.core.entities.request.objects import Request
from src.core.bases.reader import BaseReader


class HTTPReader(BaseReader):
    async def read(self, request: Request, receiver: Callable):
        more_body = True
        body_parts = []
        while more_body:
            message = await receiver()
            body_parts.append(message.get('body', b'').decode("utf-8"))
            more_body = message.get('more_body', False)
        request.body = ''.join(body_parts)
