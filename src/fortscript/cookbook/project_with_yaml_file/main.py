import logging
import os

from fortscript import FortScript

# Basic logging configuration for the cookbook example
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Path to our English configuration file
base_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(base_dir, 'config.yaml')


def alert_system():
    print(
        '📢 [System Alert] Resource usage threshold reached! Pausing overlays.'
    )


def welcome_back():
    print('✅ [System Alert] Resources cleared. Overlays are live again!')


# Initialize FortScript using the external YAML file and events
app = FortScript(
    config_path=config_path, on_pause=alert_system, on_resume=welcome_back
)


def main():
    print('--- FortScript: Content Creator Case ---')
    print(f'Loading external configuration from: {config_path}')
    print(
        'Scenario: Managing streaming overlays with settings (and log level) defined in YAML.'
    )
    app.run()


if __name__ == '__main__':
    main()
