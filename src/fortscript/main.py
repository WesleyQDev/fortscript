import os
import subprocess
import time

import psutil
import yaml
from rich import print


class RamMonitoring:
    """Monitors RAM consumption."""

    def get_percent(self):
        """Returns the current RAM usage percentage."""
        return psutil.virtual_memory().percent


class AppsMonitoring:
    """Monitors the opening of resource-heavy applications."""

    def __init__(self, heavy_processes_list):
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

    def __init__(self, config_path='config.yaml'):
        """
        Initializes FortScript with the configuration file.

        Args:
            config_path (str): The path to the YAML configuration file.
        """
        self.config = self.load_config(config_path)
        self.projects = self.config.get('projects') or []

        self.ram_monitoring = RamMonitoring()

        self.heavy_processes = self.config.get('heavy_processes') or []
        self.apps_monitoring = AppsMonitoring(self.heavy_processes)
        self.active_processes = []

        self.ram_threshold = self.config.get('ram_threshold', 80)
        

        self.is_windows = os.name == 'nt'

    def load_config(self, path):
        """
        Loads the configuration from a YAML file.

        Args:
            path (str): Path to the configuration file.

        Returns:
            dict: The loaded configuration.
        """
        with open(path, 'r') as file:
            config = yaml.safe_load(file)
        return config

    def start_scripts(self):
        """Starts all projects defined in the configuration."""
        self.active_processes = []  # Clear the list before starting
        
        for project in self.projects:
            project_name = project.get('name')
            script_path = project.get('path')
            project_dir = os.path.dirname(script_path)

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
                        venv_python if os.path.exists(
                            venv_python) else 'python'
                    )

                    proc = subprocess.Popen(
                        [python_exe, script_path],
                        creationflags=subprocess.CREATE_NEW_CONSOLE,
                    )
                    self.active_processes.append(proc)
                    print(
                        f'Name: [bold blue]{project_name}[/bold blue]\n'
                        f'Path: [red]{script_path}[/red] '
                    )

                except Exception as e:
                    print(
                        f'[bold red]Error executing {project_name}:[/bold red]'
                        f'{e}'
                    )
            elif script_path.endswith('package.json'):
                try:
                    command = ['npm', 'run', 'start']
                    if os.name == 'nt':
                        command[0] = 'npm.cmd'

                    proc = subprocess.Popen(
                        command,
                        cwd=project_dir,
                        creationflags=subprocess.CREATE_NEW_CONSOLE,
                    )
                    self.active_processes.append(proc)

                    print(
                        f'Project: [bold blue]{project_name}[/bold blue] '
                        'started successfully!'
                    )

                except Exception as e:
                    print(
                        f'[bold red]Error executing {project_name}:[/bold red]'
                        f'{e}'
                    )

            # Invalid extension handling
            elif script_path.endswith('.exe') and self.is_windows:
                try:
                    command = ['cmd.exe', '/c', str(script_path)]

                    proc = subprocess.Popen(
                        command,
                        cwd=str(project_dir),
                        creationflags=subprocess.CREATE_NEW_CONSOLE,
                    )
                    self.active_processes.append(proc)

                except Exception as e:
                    print(
                        f'[bold red]Error executing {project_name}:[/bold red]'
                        f'{e}'
                    )
            else:
                print(
                    f"\n[yellow]Warning:[/yellow] The project [bold]{project_name}[/bold] was skipped (invalid extension).\n"
                    f"Try again with a script: [red][.py, .exe][/red] or a Node.js project with a [red]package.json[/red] in the folder."
                )
    def stop_scripts(self):
        """Terminates active scripts and their child processes."""
        print(
            '[yellow]Closing active scripts and'
            'their child processes...[/yellow]'
        )
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
        print('[green]All processes have been terminated.[/green]')

    def process_manager(self):
        """Manages scripts based on heavy process activity and RAM usage."""
        script_running = ""
        while True:
            status_dict = self.apps_monitoring.active_process_list()
            is_heavy_process_open = any(status_dict.values())

            current_ram = self.ram_monitoring.get_percent()
            is_ram_critical = current_ram > self.ram_threshold


            if (is_heavy_process_open or is_ram_critical) and script_running:
                if is_heavy_process_open:
                    detected = [k for k, v in status_dict.items() if v]
                    print(
                        f'\n[bold red]Closing scripts due to heavy processes:'
                        '[/bold red]{detected}'
                    )
                else:
                    print(
                        f'\n[bold red]Closing scripts due to high RAM usage:'
                        '[/bold red] {current_ram}%'
                    )

                self.stop_scripts()
                print('[yellow]Scripts stopped.[/yellow]')
                script_running = False
            elif (
                not is_heavy_process_open
                and not is_ram_critical
                and not script_running
            ):
                print(
                    f'\n[bold green]System stable (RAM: {current_ram}%).'
                    'Starting scripts...[/bold green]'
                )
                self.start_scripts()
                script_running = True
            elif not is_heavy_process_open:
                # Optional: showing status even when already running,
                # or just pass
                pass

            if not self.active_processes and script_running:
                print("[bold red]No valid scripts found to start. FortScript is shutting down.[/bold red]")
                break
            time.sleep(5)

    def run(self):
        """Runs the main application loop."""
        self.process_manager()
