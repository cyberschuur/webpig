from enum import Enum
import logging

from rich.logging import RichHandler
from rich.console import Console
from rich.progress import Progress

console = Console(stderr=True)
progress = Progress(console=console)

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(console=console, show_path=False)],
)


class LoggingLevel(str, Enum):
    debug = "debug"
    info = "info"
    warning = "warning"
    error = "error"
    critical = "critical"
