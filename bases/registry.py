from abc import ABC, abstractmethod


class BaseRegistry(ABC):
    @classmethod
    @abstractmethod
    def register(cls, key, val):
        pass

    @classmethod
    @abstractmethod
    def retrieve(cls, key):
        pass
