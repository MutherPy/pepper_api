from abc import ABC
from dataclasses import dataclass
from bases.http_entities.base_entities import BaseJsonHttp, BaseDictHttp
from bases.http_entities.headers import BaseHeaders
from bases.http_entities.query import BaseQuery


@dataclass
class BaseRequest(ABC, BaseJsonHttp, BaseDictHttp):
    type: str
    method: str
    path: str
    headers: BaseHeaders
    query_string: BaseQuery
    body: bytes | None = None
