from enum import Enum


class ResponseTypes(str, Enum):
    START = "http.response.start"
    BODY = "http.response.body"
