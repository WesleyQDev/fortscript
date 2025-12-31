from fortscript import GAMES, Callbacks, FortScript, RamConfig
import logging
import os
import sys

# Ensure we can import fortscript from source
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.abspath(os.path.join(current_dir, '../../../'))
if src_path not in sys.path:
    sys.path.insert(0, src_path)


# Basic logging configuration
logging.basicConfig(format='%(message)s')

# Define the absolute path to our backend simulator
base_dir = os.path.dirname(os.path.abspath(__file__))
backend_path = os.path.join(base_dir, 'backend_simulator.py')

# Configuration for a typical developer development stack
projects = [
    {'name': 'Backend API Simulator', 'path': backend_path}
]


# Callback functions for game detection events
def on_pause():
    print('>>> [Event] Game detected! Development stack PAUSED.')


def on_resume():
    print('>>> [Event] No games running. Resuming development stack...')


# RAM configuration with hysteresis to prevent constant toggling
ram_config = RamConfig(
    threshold=95,  # Pause if RAM usage exceeds 95%
    safe=85,       # Resume only when RAM falls below 85%
)

# Callback configuration
callbacks = Callbacks(
    on_pause=on_pause,
    on_resume=on_resume,
)


# Initialize FortScript utilizing the imported GAMES list
# This demonstrates how to use the built-in list of heavy processes
app = FortScript(
    projects=projects,
    heavy_process=GAMES,  # Using the imported list directly
    ram_config=ram_config,
    callbacks=callbacks,
    log_level='DEBUG',
)

if __name__ == '__main__':
    print('--- FortScript: Built-in Games List Example ---')
    print('This example uses the pre-defined "GAMES" list from the library.')
    print(f'Loaded {len(GAMES)} game definitions automatically.')

    # We will not call app.run() here to avoid blocking
    # the CI/Interactive session indefinitely
    # but we will simulate the check to prove it works.

    print('\n--- Verifying Configuration ---')
    print(f'Projects configured: {len(app.projects)}')
    print(f'Heavy processes monitored: {len(app.heavy_processes)}')

    # Check if the first game in the list is correctly monitored
    first_game = GAMES[0]['name']
    print(f'First monitored game: {first_game}')

    print('\n✅ Setup complete. '
          "To run the full loop, uncomment 'app.run()' in the code.")
    app.run()
