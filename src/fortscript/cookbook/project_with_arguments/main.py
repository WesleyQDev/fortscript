import os

from fortscript import FortScript

# Define the absolute path to our backend simulator
base_dir = os.path.dirname(os.path.abspath(__file__))
backend_path = os.path.join(base_dir, "backend_simulator.py")

# Configuration for a typical developer development stack
# These projects will be started automatically when system resources are stable
development_projects = [
    {
        'name': 'API Gateway Simulator',
        'path': backend_path
    }
]

# Define heavy applications that should pause our dev stack
# (e.g., when you want to play a game or render a video)
productivity_blockers = [
    {'name': 'Chrome (Heavy Usage)', 'process': 'chrome.exe'},
    {'name': 'High-End Game', 'process': 'cyberpunk2077.exe'},
    {'name': 'Video Editor', 'process': 'premiere.exe'}
]

# Initialize FortScript with our custom configuration
app = FortScript(
    projects=development_projects,
    heavy_process=productivity_blockers,
    ram_threashold=85  # Pause if RAM usage exceeds 85%
)

if __name__ == "__main__":
    print("--- [bold green]FortScript: Developer Productivity Case[/bold green] ---")
    print("Scenario: Managing a local backend stack that pauses during heavy tasks.")
    app.run()
