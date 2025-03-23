import abc
from typing import Generator


class Source(metaclass=abc.ABCMeta):
    @staticmethod
    @abc.abstractmethod
    def name() -> str:
        raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
    def find(domain: str) -> Generator[str, None, None]:
        raise NotImplementedError
