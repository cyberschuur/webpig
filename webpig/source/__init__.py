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


def get_source_help():
    return "\n\n".join([
        f" - {source_name.value}:{source.__doc__}" if source.__doc__ else ""
        for source_name, source in all_sources.items()]).replace(" "*4, " ")


__all__ = ["ValidSource", "all_sources"]
