import logging
import os

from fortscript import Callbacks, FortScript, RamConfig

# Basic logging configuration for the cookbook example
logging.basicConfig(format='%(message)s')

# Define the absolute path to our backend simulator
base_dir = os.path.dirname(os.path.abspath(__file__))
backend_path = os.path.join(base_dir, 'backend_simulator.py')

# Configuration for a typical developer development stack
# These projects will be started automatically when system resources are stable
development_projects = [
    {'name': 'API Gateway Simulator', 'path': backend_path}
]

# Define heavy applications that should pause our dev stack
# (e.g., when you want to play a game or render a video)
productivity_blockers = [
    {'name': 'Chrome (Heavy Usage)', 'process': 'chrome.exe'},
    {'name': 'High-End Game', 'process': 'cyberpunk2077.exe'},
    {'name': 'Video Editor', 'process': 'premiere.exe'},
]


def on_pause():
    print('>>> [Event] Development stack PAUSED. Enjoy your game!')


def on_resume():
    print('>>> [Event] System stable. Returning to development mode...')


ram = RamConfig(
    threshold=90,  # Pause if RAM usage exceeds 90%
    safe=80,  # Resume only when RAM falls below 80% (Hysteresis)
)

# Initialize FortScript with our custom configuration and events
app = FortScript(
    projects=development_projects,
    heavy_process=productivity_blockers,
    ram_config=ram,
    callbacks=Callbacks(
        on_pause=on_pause,
        on_resume=on_resume,
    ),
    log_level='DEBUG',  # Show detailed logs for debugging
)

if __name__ == '__main__':
    print('--- FortScript: Developer Productivity Case ---')
    print(
        'Scenario: Managing a local backend stack that pauses during heavy tasks.'
    )
    app.run()
