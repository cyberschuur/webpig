from enum import Enum

from webpig.source import dnsdumpster

from .import crtsh
from .base import Source


class ValidSource(str, Enum):
    CRTSH = crtsh.CrtSh.name()
    DNSDUMPSTER = dnsdumpster.DnsDumpster.name()


all_sources: dict[ValidSource, type[Source]] = {
    ValidSource.CRTSH: crtsh.CrtSh,
    ValidSource.DNSDUMPSTER: dnsdumpster.DnsDumpster,
}

__all__ = ["ValidSource", "all_sources"]
