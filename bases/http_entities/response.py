from abc import ABC
from dataclasses import dataclass

from bases.http_entities.base_entities import BaseASGIComp
from bases.http_entities.headers import BaseHeaders


@dataclass
class BaseStartResponse(ABC, BaseASGIComp):
    type: str
    status: int
    headers: BaseHeaders


@dataclass
class BaseBodyResponse(ABC, BaseASGIComp):
    type: str
    body: bytes
    more_body: bool


@dataclass
class BaseResponse(ABC):
    start: BaseStartResponse
    body: BaseBodyResponse
