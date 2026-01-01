import logging
import os
import subprocess
import sys
import time
from dataclasses import dataclass
from typing import Any, Callable, TypedDict

import psutil
import yaml

logger = logging.getLogger(__name__)


class ProjectConfig(TypedDict):
    name: str
    path: str


class HeavyProcessConfig(TypedDict):
    name: str
    process: str


class RamMonitoring:
    """Monitors RAM consumption."""

    def get_percent(self) -> float:
        """Returns the current RAM usage percentage."""
        return psutil.virtual_memory().percent


class AppsMonitoring:
    """Monitors the opening of resource-heavy applications."""

    def __init__(self, heavy_processes_list: list[HeavyProcessConfig]):
        """
        Initializes the application monitoring with a list of heavy processes.

        Args:
            heavy_processes_list (list[HeavyProcessConfig]): A list of
                dictionaries containing process info.
        """
        self.heavy_processes_list = heavy_processes_list

    def active_process_list(self) -> dict[str, bool]:
        """
        Check which heavy processes from the list are currently running.

        Returns:
            dict: A dictionary mapping process names to a boolean indicating if
             they are active.
        """
        status = {item['name']: False for item in self.heavy_processes_list}
        for proc in psutil.process_iter(['name']):
            try:
                proc_name = proc.info.get('name', '').lower()
                for item in self.heavy_processes_list:
                    if item['process'].lower() in proc_name:
                        status[item['name']] = True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return status


@dataclass
class RamConfig:
    threshold: int = 95
    safe: int = 85

    def __post_init__(self):
        if self.safe >= self.threshold:
            self.safe = max(0, self.threshold - 10)


@dataclass
class Callbacks:
    """Callback functions for script events."""

    on_pause: Callable | None = None
    on_resume: Callable | None = None


class FortScript:
    """Main class to manage scripts and monitor application status."""

    def __init__(
        self,
        config_path: str = 'fortscript.yaml',
        projects: list[ProjectConfig] | None = None,
        heavy_process: list[HeavyProcessConfig] | None = None,
        ram_config: RamConfig | None = None,
        callbacks: Callbacks | None = None,
        log_level: str | int | None = None,
        new_console: bool = True,
    ):
        """
        Initializes FortScript with the configuration file and monitoring parameters.

        Args:
            config_path (str): The path to the YAML configuration file.
            projects (list[ProjectConfig], optional): List of project
                definitions to be managed.
            heavy_process (list[HeavyProcessConfig], optional): List of
                processes that trigger resource saving.
            ram_config (RamConfig, optional): RAM usage configuration.
            callbacks (Callbacks, optional): Callback functions for events.
            log_level (str | int, optional): Severity level for logging.
            new_console (bool): If True, launches scripts in a separate console.
        """
        self.new_console = new_console
        self.file_config = self.load_config(config_path)

        self.active_processes: list[subprocess.Popen] = []

        self.projects: list[ProjectConfig] = (
            projects
            if projects is not None
            else self.file_config.get('projects', [])
        )
        self.heavy_processes: list[HeavyProcessConfig] = (
            heavy_process
            if heavy_process is not None
            else (self.file_config.get('heavy_processes') or [])
        )
        if ram_config is None:
            self.ram_config = RamConfig(
                threshold=self.file_config.get('ram_threshold', 95),
                safe=self.file_config.get('ram_safe', 85)
            )
        else:
            self.ram_config = ram_config

        self.callbacks = callbacks or Callbacks()

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

    def load_config(self, path: str) -> dict[str, Any]:
        """Loads the configuration from a YAML file. Returns empty dict if file fails."""
        try:
            if os.path.exists(path):
                with open(path, 'r') as file:
                    return yaml.safe_load(file) or {}
        except Exception as e:
            logger.warning(f'Could not load {path}: {e}')
        return {}

    def start_scripts(self) -> None:
        """Starts all projects defined in the configuration."""
        self.active_processes = []  # Clear the list before starting

        for project in self.projects:
            self._start_project(project)

        if self.callbacks.on_resume:
            try:
                self.callbacks.on_resume()
            except Exception as e:
                logger.error(f'Error in on_resume callback: {e}')

    def _start_project(self, project: ProjectConfig) -> None:
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

    def stop_scripts(self) -> None:
        """Terminates active scripts and their child processes."""
        logger.info('Closing active scripts and their child processes...')

        procs_to_kill = []

        # 1. Collect all processes (parents and children)
        for proc in self.active_processes:
            try:
                parent_process = psutil.Process(proc.pid)
                procs_to_kill.append(parent_process)
                procs_to_kill.extend(parent_process.children(recursive=True))
            except psutil.NoSuchProcess:
                pass

        # 2. Send terminate signal (SIGTERM / CTRL_C_EVENT equivalent attempt)
        for p in procs_to_kill:
            try:
                p.terminate()
            except psutil.NoSuchProcess:
                pass

        # 3. Wait for processes to exit (Graceful period)
        # We give them 3 seconds to close connections, save state, etc.
        gone, alive = psutil.wait_procs(procs_to_kill, timeout=3)

        # 4. Force kill if they are still alive
        for p in alive:
            try:
                logger.warning(
                    f'Process {p.name()} (PID: {p.pid}) did not exit. '
                    'Forcing kill.'
                )
                p.kill()
            except psutil.NoSuchProcess:
                pass

        self.active_processes = []
        logger.info('All processes have been terminated.')

        if self.callbacks.on_pause:
            try:
                self.callbacks.on_pause()
            except Exception as e:
                logger.error(f'Error in on_pause callback: {e}')

    def process_manager(self) -> None:
        """Manages scripts based on heavy process activity and RAM usage."""
        script_running = False
        first_check = True

        while True:
            status_dict = self.apps_monitoring.active_process_list()
            is_heavy_open = any(status_dict.values())

            current_ram = self.ram_monitoring.get_percent()
            is_ram_critical = current_ram > self.ram_config.safe

            # Initial feedback
            if first_check and (is_heavy_open or is_ram_critical):
                reason = 'heavy processes' if is_heavy_open else 'high RAM'
                logger.info(
                    f'System is busy ({reason}). Waiting for stabilization...'
                )
                first_check = False

            # Stop Condition
            if (is_heavy_open or is_ram_critical) and script_running:
                self._handle_stop_condition(
                    is_heavy_open, status_dict, current_ram
                )
                script_running = False

            # Start Condition
            elif (
                not is_heavy_open
                and not is_ram_critical
                and not script_running
                and current_ram < self.ram_config.safe
            ):
                self._handle_start_condition(current_ram)
                script_running = True
                first_check = False

            # Dead Process Handling
            if script_running and self.active_processes:
                script_running = self._check_dead_processes(script_running)

            time.sleep(5)

    def _handle_stop_condition(
        self,
        is_heavy_open: bool,
        status_dict: dict[str, bool],
        current_ram: float,
    ) -> None:
        if is_heavy_open:
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

    def _handle_start_condition(self, current_ram: float) -> None:
        logger.info(
            f'System stable (RAM: {current_ram}%). Starting scripts...'
        )
        self.start_scripts()

    def _check_dead_processes(self, script_running: bool) -> bool:
        alive_processes = []
        for proc in self.active_processes:
            ret_code = proc.poll()
            if ret_code is None:
                alive_processes.append(proc)
            elif ret_code == 0:
                logger.info(
                    f'Process (PID: {proc.pid}) finished successfully.'
                )
            else:
                logger.warning(
                    f'Process (PID: {proc.pid}) crashed/exited '
                    f'with code {ret_code}.'
                )

        self.active_processes = alive_processes

        if not self.active_processes:
            logger.info('All scripts finished. Waiting for system changes...')
            return False
        return script_running

    def run(self) -> None:
        """Runs the main application loop."""
        self.process_manager()
