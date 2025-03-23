from enum import Enum

from .import crtsh
from .base import Source


class ValidSource(str, Enum):
    CRTSH = crtsh.CrtSh.name()


all_sources: dict[ValidSource, type[Source]] = {
    ValidSource.CRTSH: crtsh.CrtSh,
}

__all__ = ["ValidSource", "all_sources"]
