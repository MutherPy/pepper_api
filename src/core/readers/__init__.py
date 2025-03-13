from .readers import HTTPReader
from .readers_factory import ReaderFactory


reader_provider = ReaderFactory()
reader_provider.register_reader('http', HTTPReader)

__all__ = [
    'reader_provider',
]