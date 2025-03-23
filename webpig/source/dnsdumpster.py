import os
import logging

from typing import Generator, Optional
from rich.prompt import Prompt

import requests

from .. import console, progress
from .base import Source


logger = logging.getLogger()


class DnsDumpster(Source):
    """
    Uses the DNSDumpster API to find subdomains of a given domain. Requires an
    API key to be set using the DNSDUMPSTER_API_KEY environment variable or
    provided via prompt.
    """

    @staticmethod
    def _get_api_key() -> Optional[str]:
        api_key = os.getenv("DNSDUMPSTER_API_KEY")

        if not api_key:
            progress.stop()
            api_key = Prompt.ask(
                prompt="Please provide your DNSDUMPSTER_API_KEY",
                password=True,
                default=None,
                console=console
            )
            progress.start()

        return api_key

    @staticmethod
    def name() -> str:
        return "dnsdumpster"

    @staticmethod
    def find(domain: str) -> Generator[str, None, None]:
        api_key = DnsDumpster._get_api_key()

        if not api_key:
            logger.error(
                "DNSDUMPSTER_API_KEY not set and prompt not provided. Skipping dnsdumpster source.")
            return

        try:
            url = f"https://api.dnsdumpster.com/domain/{domain}"
            response = requests.get(url, headers={"X-Api-Key": api_key})
            response.raise_for_status()
        except requests.RequestException as ce:
            logger.error(
                f"Failed to fetch dnsdumpster data for {domain}: {ce}")
            return

        # for now, just return the domain names from the A records
        for record in response.json()["a"]:
            yield record["host"]

        yield url
