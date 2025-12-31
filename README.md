<div align="center">
  <a href="https://pypi.org/project/fortscript/">
    <img src="docs/logo.png" alt="FortScript" width="400">
  </a>
</div>

<p align="center">
  <a href="https://pypi.org/project/fortscript/">
    <img src="https://img.shields.io/pypi/v/fortscript?style=flat-square&color=blue" alt="PyPI">
  </a>
  <a href="https://pypi.org/project/fortscript/">
    <img src="https://img.shields.io/pypi/pyversions/fortscript?style=flat-square" alt="Python">
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="License">
  </a>
</p>

<p align="center">
  <a href="https://github.com/WesleyQDev/fortscript"><strong>English</strong></a>
  &nbsp;•&nbsp;
  <a href="https://github.com/WesleyQDev/fortscript/blob/main/README_ptBR.md">Português</a>
</p>

<br />

## What is FortScript?

Have you ever left a bot, an API, or a script running in the background while gaming, only to notice the game started lagging? Or forgot about processes silently consuming memory until your PC slowed down?

**FortScript solves this automatically.** It pauses your scripts when you open a game or resource-heavy application, and resumes them when you close it. Simple as that.

**Cross-platform:** FortScript was developed to work on any operating system, whether Windows, Linux, or MacOS.

### How it works

1. You define which scripts you want to manage (Python bots, Node.js projects, executables, etc.)
2. You define which applications are "heavy" (games, video editors, etc.)
3. FortScript monitors and does the rest: pauses when needed, resumes when possible.

**Callback Events (optional):** You can configure functions that will run automatically when scripts are paused or resumed:

- **`on_pause`**: Function executed when scripts are paused (e.g., send notification, save state).
- **`on_resume`**: Function executed when scripts are resumed (e.g., reconnect services, log return).

This is useful for integrating with notification systems, custom logs, or any action you want to perform at those moments.

## Installation

FortScript can be used in **two ways**: as a Python library or via command line (CLI). Both come in the same package.

### Installation as a project dependency

Use this option if you want to integrate FortScript into an existing Python project:

```bash
# UV (recommended)
uv add fortscript

# Poetry
poetry add fortscript

# pip
pip install fortscript
```

### Global installation (CLI)

Use this option if you want to use the `fort` command directly in the terminal, without writing code:

```bash
pipx install fortscript
```

### Prerequisites

- **Python 3.10+**
- **Node.js** (only if managing JavaScript/TypeScript projects)

---

## Configuration

FortScript can be configured in **two ways**: via a YAML file or directly through arguments in Python code.

### Option 1: YAML File

Create a file named `fortscript.yaml` in your project root:

```yaml
# ====================================
# FORTSCRIPT CONFIGURATION
# ====================================

# Scripts/projects that FortScript will manage
# FortScript starts these processes automatically
projects:
  - name: "My Discord Bot" # Friendly name (appears in logs)
    path: "./bot/main.py" # Python script (.py)

  - name: "Node API"
    path: "./api/package.json" # Node.js project (package.json)

  - name: "Local Server"
    path: "./server/app.exe" # Windows executable (.exe)

# Applications that will pause the scripts above
# When any of these processes are detected, scripts stop
heavy_processes:
  - name: "GTA V" # Friendly name
    process: "gta5" # Process name (without .exe)

  - name: "OBS Studio"
    process: "obs64"

  - name: "Cyberpunk 2077"
    process: "cyberpunk2077"

  - name: "Premiere Pro"
    process: "premiere"

# RAM threshold to pause scripts (%)
# If system RAM exceeds this value, scripts are paused
ram_threshold: 90

# Safe RAM limit to resume scripts (%)
# Scripts only return when RAM falls below this value
# This avoids constant toggling (hysteresis)
ram_safe: 80

# Log level (DEBUG, INFO, WARNING, ERROR)
# Use DEBUG to see detailed information during development
log_level: "INFO"
```

### Option 2: Code Arguments

You can pass all configurations directly in Python code without needing a YAML file:

```python
from fortscript import FortScript, RamConfig

app = FortScript(
    projects=[
        {"name": "My Bot", "path": "./bot/main.py"},
        {"name": "Node API", "path": "./api/package.json"},
    ],
    heavy_process=[
        {"name": "GTA V", "process": "gta5"},
        {"name": "OBS Studio", "process": "obs64"},
    ],
    ram_config=RamConfig(threshold=90, safe=80),
    log_level="INFO",
)

app.run()
```

> **Tip:** You can combine both! Arguments passed in code override values from the YAML file.

### Supported project types

| Type       | Extension/File   | Behavior                                            |
| ---------- | ---------------- | --------------------------------------------------- |
| Python     | `.py`            | Automatically detects `.venv` in the script's folder|
| Node.js    | `package.json`   | Runs `npm run start`                                |
| Executable | `.exe`           | Runs directly (Windows)                             |

---

## How to Use

### Option 1: Basic setup (YAML file only)

The simplest way to use FortScript:

```python
from fortscript import FortScript

# Loads settings from fortscript.yaml
app = FortScript()
app.run()
```

### Option 2: With event callbacks

Run custom functions when scripts are paused or resumed:

```python
from fortscript import FortScript, Callbacks

def when_paused():
    print("🎮 Gaming mode active! Scripts paused.")

def when_resumed():
    print("💻 Back to work! Scripts resumed.")

app = FortScript(
    config_path="fortscript.yaml",
    callbacks=Callbacks(
        on_pause=when_paused,
        on_resume=when_resumed,
    )
)

app.run()
```

### Option 3: Complete Configuration (Dynamic Python)

To keep your code organized, you can separate project and process lists into variables.

```python
from fortscript import FortScript, RamConfig, Callbacks

# 1. Define your callbacks
def notify_pause():
    print("⏸️ Scripts paused!")

def notify_resume():
    print("▶️ Scripts resumed!")

# 2. Define your projects
my_projects = [
    {"name": "Discord Bot", "path": "./bot/main.py"},
    {"name": "Express API", "path": "./api/package.json"},
    {"name": "Server", "path": "./server/app.exe"},
]

# 3. Define heavy processes
my_processes = [
    {"name": "GTA V", "process": "gta5"},
    {"name": "Cyberpunk 2077", "process": "cyberpunk2077"},
    {"name": "Chrome (Heavy)", "process": "chrome"},
]

# 4. Initialize FortScript
app = FortScript(
    projects=my_projects,
    heavy_process=my_processes,
    ram_config=RamConfig(threshold=90, safe=80),
    callbacks=Callbacks(
        on_pause=notify_pause,
        on_resume=notify_resume
    ),
    log_level="DEBUG",
)

app.run()
```

### Option 4: Via CLI (terminal)

Ideal for quick use or basic testing.

```bash
fort
```

> **Warning:** Currently, the CLI looks for settings in the package's internal file (`src/fortscript/cli/fortscript.yaml`), which limits local customization via CLI. For real projects, using a Python script (Options 1 to 3) is recommended until local CLI config support is implemented.

---

## Practical Example: Gaming Mode

Imagine you are a developer who runs work scripts (bots, APIs, automations) during the day but wants to play at night without the PC lagging.

In this example, we use FortScript's built-in game list (`GAMES`) so you don't have to configure each game manually.

### Project Structure

```text
my_project/
├── discord_bot/
│   ├── .venv/
│   └── main.py              # RAM-consuming bot
├── local_api/
│   ├── node_modules/
│   └── package.json         # Local Express API
└── gaming_mode.py           # Your manager script
```

### `gaming_mode.py` file

```python
import os
from fortscript import FortScript, GAMES

# Project paths
base_dir = os.path.dirname(os.path.abspath(__file__))
bot_path = os.path.join(base_dir, "discord_bot", "main.py")
api_path = os.path.join(base_dir, "local_api", "package.json")

# Projects to manage
my_projects = [
    {"name": "Discord Bot", "path": bot_path},
    {"name": "Local API", "path": api_path},
]

# Combining the default game list with custom processes
# GAMES already includes GTA, Valorant, CS2, LOL, Fortnite, etc.
my_heavy_processes = GAMES + [
    {"name": "Video Editor", "process": "premiere"},
    {"name": "C++ Compiler", "process": "cl"}
]

def on_pause():
    print("=" * 50)
    print("🎮 GAMING MODE ACTIVE! Scripts paused to free up resources.")
    print("=" * 50)

def on_resume():
    print("=" * 50)
    print("💻 WORK MODE - Resuming your scripts...")
    print("=" * 50)

# Initialize FortScript
app = FortScript(
    projects=my_projects,
    heavy_process=my_heavy_processes,
    ram_config=RamConfig(threshold=85, safe=75),
    callbacks=Callbacks(
        on_pause=on_pause,
        on_resume=on_resume,
    ),
)

if __name__ == "__main__":
    print("🎯 FortScript: Gaming Mode Started")
    app.run()
```

---

## Roadmap
> If you have an idea, feel free to suggest new features by creating an `issue`.

### Library

- [ ] **Custom Functions**: Manage Python functions by creating separate threads.
- [ ] **Per-Project Conditions**: Allow a specific project to pause only if a specific app opens.
- [ ] **Graceful Shutdown**: Try a graceful shutdown (SIGINT/CTRL+C) before forcing process termination.
- [ ] **Dead Process Handling**: Periodically check if started processes are still alive.
- [ ] **Project Abstraction**: Refactor into classes (`PythonProject`, `NodeProject`) to easily add new languages.
- [x] **Type Hinting**: Improve typing across all methods for better IDE support.

### CLI

- [ ] **System Tray**: Run minimized in the system tray.
- [ ] **Additional commands**:
  - `fort add <path>` - Add project to config
  - `fort list` - List configured projects
  - `fort remove <name>` - Remove project

---

## Current Features

- [x] Automatic pause when detecting heavy applications
- [x] Automatic pause by RAM limit
- [x] Built-in list with 150+ games and apps (`from fortscript import GAMES`)
- [x] Resuming with hysteresis (ram_safe vs ram_threshold)
- [x] Python script support with `.venv` detection
- [x] Node.js project support via `npm run start`
- [x] Windows executable support (`.exe`)
- [x] Configuration via YAML file (`fortscript.yaml`)
- [x] Configuration via code arguments
- [x] Event callbacks (`on_pause` and `on_resume`)
- [x] Configurable log levels (DEBUG, INFO, WARNING, ERROR)
- [x] Safe process termination (tree-kill)

---

## Contributing

Contributions are welcome! See the [Contributing Guide](CONTRIBUTING.md) to get started.

## License

MIT - See [LICENSE](LICENSE) for details.

---

<div align="center">
  Made with ❤️ by <a href="https://github.com/WesleyQDev">WesleyQDev</a>
</div>