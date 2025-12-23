import logging
import os
from importlib.metadata import version

from rich.console import Console
from rich.logging import RichHandler
from rich.text import Text

from fortscript import FortScript

try:
    __version__ = version('fortscript')
except Exception:
    __version__ = 'unknown'

console = Console()


def main():
    """Main entry point for the CLI."""
    # Configure logging with Rich
    logging.basicConfig(
        level="INFO",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True, show_path=False)]
    )

    # Minimalist and elegant header
    header = Text()
    header.append('', style='default')
    header.append('FORT', style='bold color(220)')
    header.append('SCRIPT', style='bold color(87)')
    header.append(f' v{__version__} by WesleyQDev', style='dim')
    console.print(header)

    # Path for the global config
    config_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'config.yaml'
    )

    app = FortScript(config_path=config_path)
    app.run()


if __name__ == '__main__':
    main()
