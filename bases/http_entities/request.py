from abc import ABC
from dataclasses import dataclass
from io import BytesIO, FileIO
from typing import Union

from bases.http_entities.base_mixins import BaseASGICompScope
from bases.http_entities.headers import BaseHeaders
from bases.http_entities.query import BaseQuery


@dataclass
class CommonASGIRequest(ABC):
    type: str
    path: str
    query_string: BaseQuery
    headers: BaseHeaders


@dataclass
class BaseRequest(BaseASGICompScope, CommonASGIRequest, ABC):
    method: str
    body: Union[bytes, BytesIO, FileIO]


@dataclass
class BaseBodyRequest(ABC):
    body: bytes | None = None


@dataclass
class BaseFileRequest(ABC):
    body: BytesIO | None = None


@dataclass
class BaseBigFileRequest(ABC):
    body: FileIO | None = None


@dataclass
class BaseWSRequest(BaseASGICompScope, CommonASGIRequest, ABC):
    pass
