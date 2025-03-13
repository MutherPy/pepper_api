from .readers import HTTPReader
from .readers_factory import ReaderProvider


reader_provider = ReaderProvider()
reader_provider.register_reader('http', HTTPReader)

__all__ = [
    'reader_provider',
]