import logging

from typing import Generator, cast

import requests

from .base import Source


logger = logging.getLogger()


class CrtSh(Source):
    """
    Scans crt.sh for subdomains of a given domain.
    """

    @staticmethod
    def name() -> str:
        return "crt.sh"

    @staticmethod
    def find(domain: str) -> Generator[str, None, None]:
        url = f"https://crt.sh/?q=%25.{domain}&output=json"

        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException as ce:
            logger.error(f"Failed to fetch crt.sh data for {domain}: {ce}")
            return

        for record in response.json():
            record = cast(dict[str, str], record)
            for name in record["name_value"].split('\n'):
                # skip wildcard subdomains since they're not reachable
                if not name.startswith("*"):
                    yield name
