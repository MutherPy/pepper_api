from abc import ABC
from dataclasses import dataclass
from bases.http_entities.base_mixins import BaseJsonHttp, BaseASGICompScope
from bases.http_entities.headers import BaseHeaders
from bases.http_entities.query import BaseQuery


@dataclass
class BaseRequest(BaseJsonHttp, BaseASGICompScope, ABC):
    type: str
    method: str
    path: str
    headers: BaseHeaders
    query_string: BaseQuery
    body: bytes | None = None
