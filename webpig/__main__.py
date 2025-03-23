import logging

import typer
from rich.progress import track

from . import LoggingLevel, console
from .probe import ValidProbe, ProbeStatus, all_probes
from .source import ValidSource, all_sources

logger = logging.getLogger()


def collect_subdomains(domain: str, sources: list[ValidSource]) -> list[str]:
    subdomains: set[str] = set()
    logger.info(f"Enumerating subdomains for {domain}")

    for source_name in sources:
        source = all_sources[source_name]

        for subdomain in track(source.find(domain), description=f"Enumerating subdomains from {source.name()}", console=console):
            subdomains.add(subdomain)

    logger.info(f"Found {len(subdomains)} subdomains")
    logger.debug(f"Subdomains:\n\t{"\n\t".join(subdomains)}")

    return list(subdomains)


def probe_subdomains(domain: str, subdomains: list[str], probe_name: ValidProbe) -> list[ProbeStatus]:
    probe = all_probes[probe_name]
    results: list[ProbeStatus] = []

    logger.info(f"Probing subdomains with {probe.name()}")

    for subdomain in track(subdomains, description=f"Probing subdomains with {probe.name()}", console=console):
        results.append(probe.probe(subdomain))

    return results


def print_results(results: list[ProbeStatus]):
    print("\n".join([
        result.model_dump_json()
        for result in results
    ]))


def main(
    domain: str,
    verbosity: LoggingLevel = typer.Option(
        "info",
        "--verbosity",
        "-v",
        help="Logging verbosity"
    ),
    source: ValidSource = typer.Option(
        help="Sources to use for subdomain enumeration. If not provided, all sources will be used.",
    ),
    probe: ValidProbe = typer.Option(
        help="Probes to use for subdomain probing. If not provided, all probes will be used."
    ),
):
    logger.setLevel(verbosity.upper())

    subdomains = collect_subdomains(domain, [source])
    results = probe_subdomains(domain, subdomains, probe)
    print_results(results)


typer.run(main)
