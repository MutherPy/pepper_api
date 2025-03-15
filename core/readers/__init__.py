from .readers import HTTPReader
from .readers_factory import ReaderProvider
from bases.http_types import RequestType


reader_provider = ReaderProvider()
reader_provider.register_reader(RequestType.HTTP, HTTPReader)

__all__ = [
    'reader_provider',
]