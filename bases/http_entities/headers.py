from abc import ABC, abstractmethod
from bases.http_entities.base_mixins import BaseDictHttp, BaseASGIComp, BaseJsonHttp
from dataclasses import dataclass, field


@dataclass
class BaseHeaders(BaseJsonHttp, BaseDictHttp, BaseASGIComp, ABC):
    _headers: dict = field(default_factory=dict)

    @abstractmethod
    def set(self, key: str, val):
        pass

    @abstractmethod
    def get(self, key: str) -> str:
        pass
