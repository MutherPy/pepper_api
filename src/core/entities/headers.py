from dataclasses import dataclass

from src.core.entities.entities_util import BaseHTTPEntity


@dataclass
class Headers(BaseHTTPEntity):
    host: str
    connection: str
    accept: str
    content_type: str


def make_headers(value: list[tuple[bytes, bytes]]) -> Headers:
    d = {}
    for k, v in value:
        key = k.decode("utf-8")
        val = v.decode("utf-8")
        if '-' in key:
            key = key.replace('-', '_')
        d[key] = val
    return Headers.from_dict(d)
