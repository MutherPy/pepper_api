from abc import ABC
from dataclasses import dataclass
from bases.http_entities.base_mixins import BaseJsonHttp, BaseASGICompScope
from bases.http_entities.headers import BaseHeaders
from bases.http_entities.query import BaseQuery


@dataclass
class CommonASGIRequest(ABC):
    type: str
    path: str
    query_string: BaseQuery
    headers: BaseHeaders


@dataclass
class BaseRequest(BaseJsonHttp, BaseASGICompScope, CommonASGIRequest, ABC):
    method: str
    body: bytes | None = None


@dataclass
class BaseWSRequest(BaseASGICompScope, CommonASGIRequest, ABC):
    ...
