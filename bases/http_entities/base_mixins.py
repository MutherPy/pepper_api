from abc import abstractmethod, ABC
from functools import singledispatch


class BaseJsonHttp(ABC):
    @abstractmethod
    def to_json(self) -> str:
        pass

    @classmethod
    def from_json(cls, data: str | bytes):
        raise NotImplementedError


class BaseDictHttp(ABC):
    @abstractmethod
    def to_dict(self) -> dict:
        pass

    @classmethod
    def from_dict(cls, data: dict):
        raise NotImplementedError


class BaseListHttp(ABC):
    @abstractmethod
    def to_list(self) -> list:
        pass


class BaseASGICompScope(ABC):
    @classmethod
    @abstractmethod
    def from_scope(cls, scope: dict):
        pass


class BaseASGICompASGI(ABC):
    @abstractmethod
    async def to_asgi(self):
        pass


class BaseASGISend(ABC):
    @abstractmethod
    async def send_to_asgi(self, sender):
        pass


class BaseASGIComp(BaseASGICompScope, BaseASGICompASGI, ABC):
    pass
