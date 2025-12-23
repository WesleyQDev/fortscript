import random
import time

from rich.console import Console
from rich.live import Live
from rich.table import Table

console = Console()


def simulate_requests():
    """Simulates a developer backend logging API requests."""
    methods = ['GET', 'POST', 'PUT', 'DELETE']
    endpoints = [
        '/api/v1/users',
        '/api/v1/auth/login',
        '/api/v1/products',
        '/api/v1/orders',
    ]

    logs = []

    with Live(refresh_per_second=2) as live:
        while True:
            # Generate a new random request
            method = random.choice(methods)
            endpoint = random.choice(endpoints)
            status = random.choice([200, 201, 400, 404, 500])
            latency = random.randint(10, 500)

            log_entry = {
                'time': time.strftime('%H:%M:%S'),
                'method': method,
                'endpoint': endpoint,
                'status': status,
                'latency': f'{latency}ms',
            }

            logs.append(log_entry)
            if len(logs) > 10:
                logs.pop(0)

            # Create a nice UI table
            table = Table(
                title='[bold blue]Developer Backend Simulator - Service A[/bold blue]'
            )
            table.add_column('Time', style='dim')
            table.add_column('Method', style='bold')
            table.add_column('Endpoint', style='cyan')
            table.add_column(
                'Status', style='green' if status < 400 else 'red'
            )
            table.add_column('Latency', style='magenta')

            for log in logs:
                table.add_row(
                    log['time'],
                    log['method'],
                    log['endpoint'],
                    str(log['status']),
                    log['latency'],
                )

            live.update(table)
            time.sleep(random.uniform(0.5, 2.0))


if __name__ == '__main__':
    try:
        simulate_requests()
    except KeyboardInterrupt:
        console.print('\n[yellow]Shutting down Backend Simulator...[/yellow]')
