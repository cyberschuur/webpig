import logging

import typer

from webpig import LoggingLevel, console, progress
from webpig.probe import ValidProbe, ProbeStatus, all_probes, get_probe_help
from webpig.source import ValidSource, all_sources, get_source_help

logger = logging.getLogger()


def collect_subdomains(domain: str, sources: list[ValidSource]) -> list[str]:
    subdomains: set[str] = set([domain])
    logger.info(f"Enumerating subdomains for {domain}")

    for source_name in sources:
        source = all_sources[source_name]

        task = progress.add_task(
            f"Enumerating subdomains from {source.name()}",
            console=console,
            total=None
        )

        for subdomain in source.find(domain):
            subdomains.add(subdomain)
            progress.advance(task)

        progress.remove_task(task)

    logger.info(f"Found {len(subdomains)} subdomains")
    logger.debug(f"Subdomains:\n\t{"\n\t".join(subdomains)}")

    return list(subdomains)


def probe_subdomains(subdomains: list[str], probes: list[ValidProbe]) -> list[ProbeStatus]:
    if not subdomains:
        logger.warning("No subdomains to probe")
        return []

    results: list[ProbeStatus] = []
    logger.info(f"Probing subdomains")

    for probe_name in probes:
        probe = all_probes[probe_name]
        task = progress.add_task(
            f"Probing subdomains with {probe.name()}", total=len(subdomains))

        for subdomain in subdomains:
            results.append(probe.probe(subdomain))
            progress.advance(task)

        progress.remove_task

    logger.info(f"Probing complete: collected {len(results)} results")
    logger.debug(
        f"Results:\n\t{"\n\t".join([result.model_dump_json() for result in results])}")

    return results


def print_results(results: list[ProbeStatus]):
    print("\n".join([
        result.model_dump_json()
        for result in results
    ]))


def main(
    domain: str,
    verbosity: LoggingLevel = typer.Option(
        "info", "--verbosity", "-v",
        help="Logging verbosity"
    ),
    source: list[ValidSource] = typer.Option(
        [], help=f"Sources to use for subdomain enumeration. If not provided, all sources will be used.\n\n{get_source_help()}",
    ),
    probes: list[ValidProbe] = typer.Option(
        [], help=f"Probes to use for host probing. If not provided, all probes will be used.\n\n{get_probe_help()}"
    ),
):
    progress.start()
    logger.setLevel(verbosity.upper())

    if not source:
        source = list(all_sources.keys())
    if not probes:
        probes = list(all_probes.keys())

    try:
        subdomains = collect_subdomains(domain, source)
        results = probe_subdomains(subdomains, probes)
        print_results(results)
    except KeyboardInterrupt:
        logger.error("User interrupted")
    finally:
        progress.stop()
