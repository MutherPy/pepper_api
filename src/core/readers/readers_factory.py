from typing import Type

from src.core.bases.reader import BaseReader
from src.core.exceptions.runtime_exc import IncorrectRegistering, MissedRegistering


class ReaderFactory:
    __READERS: dict[str, Type[BaseReader]] = {}

    def register_reader(self, reader_type: str, reader_class: Type[BaseReader], force=False):
        if self.__READERS.get(reader_type) and not force:
            raise IncorrectRegistering(reader_class)
        self.__READERS[reader_type] = reader_class

    def get_reader(self, reader_type: str) -> BaseReader:
        try:
            return self.__READERS[reader_type]()
        except KeyError:
            raise MissedRegistering(reader_type)
