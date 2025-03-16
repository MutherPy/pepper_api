from abc import ABC, abstractmethod
from dataclasses import dataclass

from bases.http_entities.base_mixins import BaseDictHttp, BaseASGICompASGI
from bases.http_entities.headers import BaseHeaders


@dataclass
class BaseStartResponse(BaseDictHttp, BaseASGICompASGI, ABC):
    type: str
    status: int
    headers: BaseHeaders


@dataclass
class BaseBodyResponse(BaseDictHttp, BaseASGICompASGI, ABC):
    type: str
    body: bytes
    more_body: bool = False


@dataclass
class BaseResponse(ABC):
    start: BaseStartResponse
    body: BaseBodyResponse
