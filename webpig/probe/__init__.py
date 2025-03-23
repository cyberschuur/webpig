

from enum import Enum

from .base import ProbeStatus, Probe
from .http import HttpProbe


class ValidProbe(str, Enum):
    HTTP = HttpProbe.name()


all_probes: dict[ValidProbe, type[Probe]] = {
    ValidProbe.HTTP: HttpProbe,
}


__all__ = ["ValidProbe", "ProbeStatus", "all_probes"]
