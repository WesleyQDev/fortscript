import logging
import os
import subprocess
import sys
import time
from typing import Callable

import psutil
import yaml

logger = logging.getLogger(__name__)


class RamMonitoring:
    """Monitors RAM consumption."""

    def get_percent(self):
        """Returns the current RAM usage percentage."""
        return psutil.virtual_memory().percent


class AppsMonitoring:
    """Monitors the opening of resource-heavy applications."""

    def __init__(self, heavy_processes_list: list):
        """
        Initializes the application monitoring with a list of heavy processes.

        Args:
            heavy_processes_list (list): A list of dictionaries containing
                process info.
        """
        self.heavy_processes_list = heavy_processes_list

    def active_process_list(self):
        """
        Check which heavy processes from the list are currently running.

        Returns:
            dict: A dictionary mapping process names to a boolean indicating if
             they are active.
        """
        status = {item['name']: False for item in self.heavy_processes_list}
        for proc in psutil.process_iter(['name']):
            try:
                proc_name = proc.info['name'].lower()
                for item in self.heavy_processes_list:
                    if item['process'].lower() in proc_name:
                        status[item['name']] = True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return status


class FortScript:
    """Main class to manage scripts and monitor application status."""

    def __init__(
        self,
        config_path: str = 'fortscript.yaml',
        projects: list[dict[str, str]] | None = None,
        heavy_process: list[dict[str, str]] | None = None,
        ram_threshold: int | None = None,
        ram_safe: int | None = None,
        on_pause: Callable | None = None,
        on_resume: Callable | None = None,
        log_level: str | int | None = None,
        new_console: bool = True,
    ):
        """
        Initializes FortScript with the configuration file and monitoring parameters.

        Args:
            config_path (str): The path to the YAML configuration file.
            projects (list[dict[str, str]], optional): List of project definitions to be managed.
            heavy_process (list[dict[str, str]], optional): List of processes that trigger resource saving.
            ram_threshold (int, optional): RAM usage percentage that triggers a pause in scripts.
            ram_safe (int, optional): RAM usage percentage considered safe to resume execution.
            on_pause (Callable, optional): Callback function to execute when scripts are paused.
            on_resume (Callable, optional): Callback function to execute when scripts are resumed.
            log_level (str | int, optional): Severity level for logging (e.g., 'INFO', 'DEBUG').
            new_console (bool): If True, launches scripts in a separate console window.
        """
        self.new_console = new_console
        self.file_config = self.load_config(config_path)

        self.active_processes = []

        self.projects = (
            projects
            if projects is not None
            else (self.file_config.get('projects') or [])
        )
        self.heavy_processes = (
            heavy_process
            if heavy_process is not None
            else (self.file_config.get('heavy_processes') or [])
        )
        self.ram_threshold = (
            ram_threshold
            if ram_threshold is not None
            else (self.file_config.get('ram_threshold', 95))
        )
        self.ram_safe = (
            ram_safe
            if ram_safe is not None
            else (self.file_config.get('ram_safe', 85))
        )

        self.on_pause = on_pause
        self.on_resume = on_resume

        # Set log level (Argument > Config > Default INFO)
        level = (
            log_level
            if log_level is not None
            else (self.file_config.get('log_level', 'INFO'))
        )
        logger.setLevel(level)

        self.is_windows = os.name == 'nt'

        self.apps_monitoring = AppsMonitoring(self.heavy_processes)
        self.ram_monitoring = RamMonitoring()

    def load_config(self, path):
        """Loads the configuration from a YAML file. Returns empty dict if file fails."""
        try:
            if os.path.exists(path):
                with open(path, 'r') as file:
                    return yaml.safe_load(file) or {}
        except Exception as e:
            logger.warning(f'Could not load {path}: {e}')
        return {}

    def start_scripts(self):
        """Starts all projects defined in the configuration."""
        self.active_processes = []  # Clear the list before starting

        for project in self.projects:
            self._start_project(project)

        if self.on_resume:
            try:
                self.on_resume()
            except Exception as e:
                logger.error(f'Error in on_resume callback: {e}')

    def _start_project(self, project):
        """Starts a single project based on its configuration."""
        project_name = project.get('name', 'Unknown Project')
        script_path = project.get('path')

        if not script_path:
            logger.warning(
                f'Project {project_name} '
                f"skipped because it has no 'path' defined."
            )
            return

        project_dir = os.path.dirname(script_path)
        creation_flags = 0
        if self.is_windows and self.new_console:
            creation_flags = subprocess.CREATE_NEW_CONSOLE

        # Check if the script is Python
        if script_path.endswith('.py'):
            try:
                if self.is_windows:
                    venv_python = os.path.join(
                        project_dir, '.venv', 'Scripts', 'python.exe'
                    )
                else:
                    venv_python = os.path.join(
                        project_dir, '.venv', 'bin', 'python'
                    )

                python_exe = (
                    venv_python
                    if os.path.exists(venv_python)
                    else sys.executable
                )

                proc = subprocess.Popen(
                    [python_exe, script_path],
                    creationflags=creation_flags,
                )
                self.active_processes.append(proc)
                logger.info(f'Project started: {project_name} ({script_path})')

            except Exception as e:
                logger.error(f'Error executing {project_name}: {e}')

        elif script_path.endswith('package.json'):
            try:
                command = ['npm', 'run', 'start']
                if os.name == 'nt':
                    command[0] = 'npm.cmd'

                proc = subprocess.Popen(
                    command,
                    cwd=project_dir,
                    creationflags=creation_flags,
                )
                self.active_processes.append(proc)
                logger.info(f'Project: {project_name} started successfully!')

            except Exception as e:
                logger.error(f'Error executing {project_name}: {e}')

        # Invalid extension handling
        elif script_path.endswith('.exe') and self.is_windows:
            try:
                command = ['cmd.exe', '/c', str(script_path)]

                proc = subprocess.Popen(
                    command,
                    cwd=str(project_dir),
                    creationflags=creation_flags,
                )
                self.active_processes.append(proc)

            except Exception as e:
                logger.error(f'Error executing {project_name}: {e}')
        else:
            logger.warning(
                f'The project {project_name} was skipped (invalid extension). '
                'Try again with a script: [.py, .exe] or a Node.js project.'
            )

    def stop_scripts(self):
        """Terminates active scripts and their child processes."""
        logger.info('Closing active scripts and their child processes...')
        for proc in self.active_processes:
            try:
                # 1. Get the process by PID using psutil
                parent_process = psutil.Process(proc.pid)

                # 2. List all children (the python script, etc.)
                for child_process in parent_process.children(recursive=True):
                    child_process.terminate()  # Close the child

                # 3. Close the parent (the uv/pnpm command)
                parent_process.terminate()

            except (psutil.NoSuchProcess, Exception):
                pass

        self.active_processes = []
        logger.info('All processes have been terminated.')

        if self.on_pause:
            try:
                self.on_pause()
            except Exception as e:
                logger.error(f'Error in on_pause callback: {e}')

    def process_manager(self):
        """Manages scripts based on heavy process activity and RAM usage."""
        script_running = False
        first_check = True

        while True:
            status_dict = self.apps_monitoring.active_process_list()
            is_heavy_process_open = any(status_dict.values())

            current_ram = self.ram_monitoring.get_percent()
            is_ram_critical = current_ram > self.ram_threshold

            # Initial feedback if system is already heavy
            if first_check and (is_heavy_process_open or is_ram_critical):
                reason = (
                    'heavy processes' if is_heavy_process_open else 'high RAM'
                )
                logger.info(
                    f'System is busy ({reason}). Waiting for stabilization...'
                )
                first_check = False

            if (is_heavy_process_open or is_ram_critical) and script_running:
                if is_heavy_process_open:
                    detected = [k for k, v in status_dict.items() if v]
                    logger.warning(
                        f'Closing scripts due to heavy processes: {detected}'
                    )
                else:
                    logger.warning(
                        f'Closing scripts due to high RAM usage: {current_ram}%'
                    )

                self.stop_scripts()
                logger.info('Scripts stopped.')
                script_running = False
            elif (
                not is_heavy_process_open
                and not is_ram_critical
                and not script_running
                and current_ram < self.ram_safe
            ):
                logger.info(
                    f'System stable (RAM: {current_ram}%). Starting scripts...'
                )
                self.start_scripts()
                script_running = True
                first_check = False
            elif not is_heavy_process_open:
                # Optional: showing status even when already running,
                # or just pass
                pass

            if not self.active_processes and script_running:
                logger.error(
                    'No valid scripts found to start. '
                    'FortScript is shutting down.'
                )
                break
            time.sleep(5)

    def run(self):
        """Runs the main application loop."""
        self.process_manager()
