from abc import ABC, abstractmethod
from bases.http_entities.base_entities import BaseListHttp, BaseDictHttp


class BaseHeaders(ABC, BaseListHttp, BaseDictHttp):
    @abstractmethod
    def get(self, key: str) -> str:
        pass
