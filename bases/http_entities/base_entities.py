from abc import abstractmethod, ABC


class BaseJsonHttp(ABC):
    @abstractmethod
    def json(self) -> str:
        pass

    @abstractmethod
    def from_json(self, data: str | bytes):
        pass


class BaseDictHttp(ABC):
    @abstractmethod
    def dict(self) -> dict:
        pass

    @abstractmethod
    def from_dict(self, data: dict):
        pass


class BaseListHttp(ABC):
    @abstractmethod
    def to_list(self) -> list:
        pass


class BaseASGIComp(ABC):
    @abstractmethod
    def to_asgi(self):
        pass
