# FortScript

A process supervisor with execution control based on system resource state.

[English](README.md) | [Português](README_ptBR.md)


## 1. Python Library

FortScript can be integrated into any Python project as a library to manage child scripts.

You can use FortScript to start scripts and stop them when a certain amount of RAM is used. Or when a specific application/process is started.

A use case, for example, would be to use the library to create a Gaming Mode, where within your project you can define scripts that will be paused when specific games are started and resumed when the games are closed.

### Installation
FortScript was developed using UV. We recommend using UV to install the library.

```bash
uv add fortscript
```

If you are using standard Python, you can install the FortScript library with pip.

```bash
pip install fortscript
```

### Quick Start
```python
from fortscript import FortScript

# Initialize with a configuration file
app = FortScript(config_path="my_config.yaml")

# Run the management loop
app.run()
```

### Why use the library?
-   **Clean Lifecycle**: Safely start and stop child processes (including full process trees).
-   **Resource Monitoring**: Built-in hooks for RAM usage and process activity.
-   **Multi-Runtime**: Supports Python, Node.js (pnpm) and Native Executables.

#### 1. Managing Independent Modules
You can use FortScript as a central controller for various scripts scattered across your system.

**config.yaml**:
```yaml
# List of projects to be managed
projects:
  - name: "Trading Bot"
    path: "C:/Users/Dev/Finance/bot.py"
  - name: "Server Monitor"
    path: "C:/Users/Dev/Server/monitor.js"

# Processes that, when detected, will pause your projects
heavy_processes:
  - name: "Fortnite"
    process: "fortnite"
  - name: "Video Editor"
    process: "resolve"

# RAM usage percentage threshold to trigger safe shutdown
ram_threshold: 90
```

#### 2. Integration in larger projects
Import `FortScript` in your main application entry point to automatically handle background tasks.

```python
# main_controller.py
from fortscript import FortScript

def start_services():
    # Detects games/heavy apps and pauses these services automatically
    manager = FortScript(config_path="./services_config.yaml")
    manager.run()
```

### Configuration Options

The `config.yaml` file supports the following fields:

| Field | Description | Type | Default |
| :--- | :--- | :--- | :--- |
| `projects` | List of applications to manage. Each item needs a `name` and `path`. | List | `[]` |
| `heavy_processes` | List of processes that trigger a pause. Each item needs a `name` and `process` (part of the executable name). | List | `[]` |
| `ram_threshold` | Maximum RAM usage percentage allowed before stopping scripts. | Integer | `80` |

---

## 2. CLI

The CLI is an interface designed for a broad audience, allowing for easy process management.

### Usage
If you are developing locally:
```bash
uv run fort
```
After installation, simply run:
```bash
fort
```

- **Configuration**: The CLI looks for a `config.yaml` file in the same directory as the script.
- **Auto-detection**: Soon, it will be possible to add the main initialization script to the CLI by running a single command inside the project folder.

---

## Roadmap & Features

The following list tracks the progress of our features and future implementations:

- [x] **Monitor Heavy Processes**: Detection of applications that consume many resources.
- [x] **Monitor RAM Usage**: Automatic triggers based on memory percentage.
- [x] **Unified Script Executor**:
    - [ ] Native Executables (`.exe`)
    - [x] Python Scripts (`.py`)
    - [ ] JavaScript/TypeScript Projects (`package.json`)
- [ ] **System Integration**:
    - [ ] Auto-start with Windows/Linux.
    - [ ] System Tray (icon in the taskbar) for background operation.
- [x] **Smart Interruption**:
    - [x] Automatic stop when heavy processes are detected.
    - [x] Automatic resume when processes are closed.
    - [x] Stop/resume cycle based on RAM.

---

## Contributing

Contributions are welcome! Please read our [Contribution Guide](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Developed with ❤️ by [WesleyyDev](https://github.com/WesleyQDev)
