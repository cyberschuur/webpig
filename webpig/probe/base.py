import abc

from typing import Any, Literal, Optional
from pydantic import BaseModel, field_serializer


AllowedMethod = Literal["GET", "POST", "PUT",
                        "DELETE", "PATCH", "HEAD", "OPTIONS", "TRACE"]


class ProbeStatus(BaseModel):
    probe: type["Probe"]
    url: str
    reachable: bool
    status: Optional[int] = None
    message: Optional[str] = None
    response_time: Optional[float] = None

    @field_serializer("probe", when_used="json")
    def probe_to_string(self, v: "Probe") -> str:
        return v.name()


class Probe(metaclass=abc.ABCMeta):
    @staticmethod
    @abc.abstractmethod
    def name() -> str:
        raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
    def probe(
        domain: str,
        timeout: int = 0,
        method: AllowedMethod = "GET",
        headers: dict[str, str] = {},
        data: dict[str, Any] = {},
    ) -> ProbeStatus:
        raise NotImplementedError
