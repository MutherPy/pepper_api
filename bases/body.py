from abc import ABC, abstractmethod


class BaseBodyEntity(ABC):

    @classmethod
    @abstractmethod
    def from_json(cls, data: bytes):
        pass
