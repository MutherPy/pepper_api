from abc import ABC, abstractmethod


class BaseExceptionResult(ABC):

    @classmethod
    @abstractmethod
    def from_exc(cls, e: Exception, **kwargs) -> "BaseExceptionResult":
        pass
