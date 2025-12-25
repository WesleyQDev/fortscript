import random
import time


# Minimalist simulator without external dependencies (rich) for stability in this test
def simulate_requests():
    """Simulates a developer backend logging API requests."""
    methods = ['GET', 'POST', 'PUT', 'DELETE']
    endpoints = [
        '/api/v1/users',
        '/api/v1/auth/login',
        '/api/v1/products',
        '/api/v1/orders',
    ]

    print('Backend Simulator Started. Press Ctrl+C to stop.')

    while True:
        method = random.choice(methods)
        endpoint = random.choice(endpoints)
        status = random.choice([200, 201, 400, 404, 500])
        latency = random.randint(10, 500)
        timestamp = time.strftime('%H:%M:%S')

        print(f'[{timestamp}] {method} {endpoint} -> {status} ({latency}ms)')
        time.sleep(random.uniform(0.5, 2.0))


if __name__ == '__main__':
    try:
        simulate_requests()
    except KeyboardInterrupt:
        print('\nShutting down Backend Simulator...')
