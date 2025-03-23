from typing import Any

from requests import request, RequestException

from webpig.probe.base import ProbeStatus, AllowedMethod, Probe


class HttpProbe(Probe):
    """
    Probes a domain using simple, unsecured HTTP.
    """

    @staticmethod
    def name() -> str:
        return "http"

    @staticmethod
    def probe(
        domain: str,
        timeout: int = 5,
        method: AllowedMethod = "GET",
        headers: dict[str, str] = {},
        data: dict[str, Any] = {}
    ) -> ProbeStatus:
        url = f"http://{domain}/"

        try:
            response = request(
                method, url, headers=headers, data=data, timeout=timeout)
        except RequestException as ce:
            # get the root cause of the exception
            while (ce.__context__):
                ce = ce.__context__

            return ProbeStatus(
                probe=HttpProbe,
                url=url,
                reachable=False,
                message=str(ce)
            )

        return ProbeStatus(
            probe=HttpProbe,
            url=url,
            reachable=response.ok,
            status=response.status_code,
            message=response.reason,
            response_time=response.elapsed.total_seconds()
        )
