import time

import psutil
from rich.console import Console
from rich.live import Live
from rich.panel import Panel

console = Console()


def streaming_overlay():
    """Simulates a background streaming helper/overlay controller."""
    with Live(refresh_per_second=4) as live:
        start_time = time.time()

        while True:
            elapsed = time.strftime(
                '%H:%M:%S', time.gmtime(time.time() - start_time)
            )
            cpu_usage = psutil.cpu_percent()

            # Simulated Twitch/YouTube events
            status_text = (
                f'[bold cyan]Overlay Active[/bold cyan]\n'
                f'Uptime: {elapsed}\n'
                f'Heartbeat: [green]Stable[/green]\n'
                f'CPU Load: [yellow]{cpu_usage}%[/yellow]\n\n'
                f'[dim]Listening for stream events...[/dim]'
            )

            panel = Panel(
                status_text,
                title='[bold magenta]StreamTools Helper[/bold magenta]',
                subtitle='Managed by FortScript',
                border_style='magenta',
            )

            live.update(panel)
            time.sleep(0.25)


if __name__ == '__main__':
    try:
        streaming_overlay()
    except KeyboardInterrupt:
        console.print('\n[magenta]StreamTools Helper Closed.[/magenta]')
