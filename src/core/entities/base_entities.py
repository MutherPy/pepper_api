from abc import abstractmethod
from typing import Union


class BaseHTTPEntity:
    @classmethod
    @abstractmethod
    def build(cls, scope: Union[dict, list]) -> "BaseHTTPEntity":
        raise NotImplementedError

    def to_dict(self) -> dict:
        return {f: getattr(self, f) for f in self.__struct_fields__}
