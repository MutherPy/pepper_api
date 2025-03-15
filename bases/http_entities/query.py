from abc import ABC, abstractmethod
from bases.http_entities.base_mixins import BaseDictHttp, BaseASGICompScope
from dataclasses import dataclass, field


@dataclass
class BaseQuery(BaseDictHttp, BaseASGICompScope, ABC):
    _query: dict = field(default_factory=dict)

    @abstractmethod
    def get(self, key: str) -> str:
        pass

