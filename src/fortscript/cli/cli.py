import os
import sys
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich import box
from rich.console import Console


def print_banner():
    """Prints a styled banner for the FortScript system."""
    title = Text()
    title.append("FORT", style="bold color(220)")
    title.append("SCRIPT", style="bold color(87)")

    credit = Text("\nby WesleyyDev", style="italic color(245)")

    content = Text.assemble(title, credit, justify="center")

    banner = Panel(
        Align.center(content, vertical="middle"),
        box=box.DOUBLE,
        border_style="bright_blue",
        padding=(1, 10),
        title="[bold white]🚀 System Loaded[/]",
        subtitle="[dim]v0.2[/]"
    )
    Console().print(banner)


def main():
    """Main entry point for the CLI."""
    # Import the main class relative to this package or absolute
    from fortscript.main import FortScript

    print_banner()
    # Use config from the same directory as cli.py
    config_path = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), "config.yaml")

    # Ensure config exists or handle it?
    # For now, keeping original behavior but user might want robustness later.

    app = FortScript(config_path=config_path)
    app.run()


if __name__ == "__main__":
    main()
