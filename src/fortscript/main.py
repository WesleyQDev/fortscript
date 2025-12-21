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
            heavy_processes_list (list): A list of dictionaries containing process info.
        """
        self.heavy_processes_list = heavy_processes_list

    def active_process_list(self):
        """
        Check which heavy processes from the list are currently running.

        Returns:
            dict: A dictionary mapping process names to a boolean indicating if they are active.
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

    def __init__(self, config_path="config.yaml"):
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

    def load_config(self, path):
        """
        Loads the configuration from a YAML file.

        Args:
            path (str): Path to the configuration file.

        Returns:
            dict: The loaded configuration.
        """
        with open(path, "r") as file:
            config = yaml.safe_load(file)
        return config

    def start_scripts(self):
        """Starts all projects defined in the configuration."""
        self.active_processes = []  # Clear the list before starting
        for project in self.projects:
            project_name = project.get('name')
            script_path = project.get('path')

            # Check if the script is Python
            if script_path.endswith(".py"):
                try:
                    proc = subprocess.Popen(['uv', "run", script_path],
                                            creationflags=subprocess.CREATE_NEW_CONSOLE)
                    self.active_processes.append(proc)
                    print(
                        f"Project: [bold blue]{project_name}[/bold blue] \n Script: [red]{script_path}[/red] started successfully!\n")

                except Exception as e:
                    print(
                        f"[bold red]Error executing {project_name}:[/bold red] {e}")
            # Check if the script is JS or TS
            elif script_path.endswith(".js") or script_path.endswith(".ts"):
                try:
                    subprocess.Popen(['pnpm', "run", "start"],
                                     cwd=project_dir,
                                     creationflags=subprocess.CREATE_NEW_CONSOLE)

                    print(
                        f"Project: [bold blue]{project_name}[/bold blue] \n Script: [red]{script_path}[/red] started successfully!\n")

                except Exception as e:
                    print(
                        f"[bold red]Error executing {project_name}:[/bold red] {e}")

            # Invalid extension handling
            else:
                print(
                    f"""[yellow]Warning:[/yellow] The project {project_name} was skipped (invalid extension). \n Try again with a script:[red] [.py, .js, .ts or .exe]""")

    def stop_scripts(self):
        """Terminates active scripts and their child processes."""
        print("[yellow]Closing active scripts and their child processes...[/yellow]")
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
        print("[green]All processes have been terminated.[/green]")

    def process_manager(self):
        """Manages scripts based on heavy process activity and RAM usage."""
        script_running = False
        while True:
            status_dict = self.apps_monitoring.active_process_list()
            is_heavy_process_open = any(status_dict.values())

            current_ram = self.ram_monitoring.get_percent()
            is_ram_critical = current_ram > self.ram_threshold

            if (is_heavy_process_open or is_ram_critical) and script_running:
                if is_heavy_process_open:
                    detected = [k for k, v in status_dict.items() if v]
                    print(
                        f"[bold red]Closing scripts due to heavy processes:[/bold red] {detected}")
                else:
                    print(
                        f"[bold red]Closing scripts due to high RAM usage:[/bold red] {current_ram}%")

                self.stop_scripts()
                print("[yellow]Scripts stopped.[/yellow]")
                script_running = False
            elif not is_heavy_process_open and not is_ram_critical and not script_running:
                print(
                    f"[bold green]System stable (RAM: {current_ram}%). Restarting scripts...[/bold green]")
                self.start_scripts()
                script_running = True
            elif not is_heavy_process_open:
                # Optional: showing status even when already running, or just pass
                pass

            time.sleep(5)

    def run(self):
        """Runs the main application loop."""
        print("Running...")
        self.process_manager()
