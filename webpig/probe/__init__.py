

from enum import Enum

from .base import ProbeStatus, Probe
from .http import HttpProbe


class ValidProbe(str, Enum):
    HTTP = HttpProbe.name()


all_probes: dict[ValidProbe, type[Probe]] = {
    ValidProbe.HTTP: HttpProbe,
}


def get_probe_help():
    return "\n\n".join([
        f" - {probe_name.value}:{probe.__doc__}" if probe.__doc__ else ""
        for probe_name, probe in all_probes.items()]).replace(" "*4, " ")


__all__ = ["ValidProbe", "ProbeStatus", "all_probes"]
