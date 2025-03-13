from dataclasses import dataclass
from http import HTTPMethod
from urllib.parse import parse_qs

from src.core.entities.entities_util import BaseHTTPEntity
from src.core.exceptions.request_exc import IncorrectHTTPMethod
from src.core.entities.headers import Headers, make_headers


@dataclass
class Request(BaseHTTPEntity):
    type: str
    http_version: str
    method: str
    path: str
    query_string: dict
    headers: Headers
    client: tuple
    server: tuple
    state: dict
    body: str = ''

    def __post_init__(self):
        try:
            HTTPMethod[self.method]
        except KeyError as e:
            raise IncorrectHTTPMethod(f'No such method: {self.method}') from e
        if query_string := self.query_string.decode("UTF-8"):
            self.query_string = parse_qs(query_string)
        self.headers = make_headers(self.headers)
