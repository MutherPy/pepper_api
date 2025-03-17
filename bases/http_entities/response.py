from abc import ABC, abstractmethod
from dataclasses import dataclass

from bases.http_entities.base_mixins import BaseDictHttp, BaseASGICompASGI, BaseASGISend
from bases.http_entities.headers import BaseHeaders


@dataclass
class BaseStartResponse(BaseDictHttp, BaseASGICompASGI, ABC):
    type: str
    status: int
    headers: BaseHeaders

    @classmethod
    @abstractmethod
    def build(cls, *args, **kwargs) -> "BaseStartResponse":
        pass


@dataclass
class BaseBodyResponse(BaseDictHttp, BaseASGICompASGI, ABC):
    type: str
    body: bytes
    more_body: bool

    @classmethod
    @abstractmethod
    def build(cls, *args, **kwargs) -> "BaseBodyResponse":
        pass


@dataclass
class BaseResponse(BaseASGISend, ABC):
    start: BaseStartResponse
    body: BaseBodyResponse

    @classmethod
    @abstractmethod
    def build(cls, *args, **kwargs) -> "BaseResponse":
        pass
