from abc import abstractmethod
from typing import Union


class BaseHTTPEntity:
    @classmethod
    @abstractmethod
    def build(cls, scope: Union[dict, list]) -> "BaseHTTPEntity":
        raise NotImplementedError
