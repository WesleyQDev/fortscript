# FortScript

A process supervisor with execution control based on system resource state.

[English](README.md) | [Português](README_ptBR.md)

**FortScript** is a Python Process Manager, based on RAM monitoring and OS process detection, that automatically starts, pauses, and terminates applications using reactive resource consumption policies.

---

## 1. The Library

FortScript can be integrated into any Python project as a library to manage child processes and monitor system health.

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
-   **Multi-Runtime**: Supports Python, Node.js (pnpm), and native Executables.

### Usage Examples

#### 1. Managing Independent Modules
You can use FortScript as a central controller for various scripts scattered across your system.

**config.yaml**:
```yaml
projects:
  - name: "Trading Bot"
    path: "C:/Users/Dev/Finance/bot.py"
  - name: "Server Monitor"
    path: "C:/Users/Dev/Server/monitor.js"
```

#### 2. Integration in Larger Projects
Import `FortScript` in your main application entry point to automatically handle background tasks.

```python
# main_controller.py
from fortscript import FortScript

def start_services():
    # Detects games/heavy apps and pauses these services automatically
    manager = FortScript(config_path="./services_config.yaml")
    manager.run()
```

---

## 2. CLI

The CLI is an interface designed for a broad audience, allowing for easy process management.

> **Note:** The CLI is currently in development. It will soon be available directly via `pip`.

- **Configuration**: The initialization file paths for your scripts are located in `cli/config.yaml`.
- **Future**: Soon, it will be possible to add the main initialization script to the CLI by running a single command inside the project folder.

### Usage
```bash
uv run cli/cli.py
```

---

## Roadmap & Features

The following list tracks the progress of our features and future implementations:

- [x] **Monitor Heavy Processes**: Detection of resource-intensive applications.
- [x] **RAM Usage Monitoring**: Automatic triggers based on memory percentage.
- [x] **Unified Script Runner**:
    - [x] Native Executables (`.exe`)
    - [x] Python Scripts (`.py`)
    - [x] JavaScript/TypeScript Projects (`package.json`)
- [ ] **System Integration**:
    - [ ] Auto-start with Windows/Linux.
    - [ ] System Tray (Icon) support for background operation.
- [x] **Smart Interruption**:
    - [x] Auto-stop when heavy processes are detected.
    - [x] Auto-resume when processes are closed.
    - [x] RAM-based stop/resume cycling.

---

## Contributing

Contributions are welcome! Please read our [Contribution Guide](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Developed with ❤️ by [WesleyyDev](https://github.com/WesleyQDev)
