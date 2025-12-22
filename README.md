<div align="center" id="top">
  <a href="https://pypi.org/project/fortscript/">
    <picture>
      <img src="docs\logo.png" alt="FortScript">
    </picture>
  </a>
</div>

<div align="center">
  <a href="https://github.com/WesleyQDev/fortscript">English</a>
  <span>&nbsp;&nbsp;•&nbsp;&nbsp;</span>
  <a href="https://github.com/WesleyQDev/fortscript/blob/main/README_ptBR.md">Português</a>
  <br />
</div>

## What is Fortscript?

Fortscript is a process supervisor with intelligent execution control based on system resource status and application activity.

## Python Library

FortScript acts as an intelligent control layer for your project's scripts and services. It allows automating the pausing and resuming of processes based on environmental triggers, such as RAM usage or the execution of specific applications.

The main focus is **development convenience**: ensuring that your support modules (bots, local APIs, workers) run only when the system has available resources or when you are not in a task that requires full hardware focus (such as games or video editing).

### Prerequisites

Before installing, make sure you meet the following requirements:

- **Python**: Version 3.12 or higher.
- **Node.js**: (Optional) Only required if you are managing JavaScript/TypeScript projects.
- **Package Manager**: We recommend [uv](https://github.com/astral-sh/uv) for a faster experience, although it is not mandatory.

### Installation

You can install FortScript using your preferred package manager:

**Using UV (Recommended):**

```bash
uv add fortscript
```

**Using Poetry:**

```bash
poetry add fortscript
```

**Virtual Environment (Manual):**

```bash
python -m venv .venv

# On Windows:
.venv\Scripts\activate

# On Linux/macOS:
source .venv/bin/activate

# After activating, install:
pip install fortscript
```

### Quick Start

```python
from fortscript import FortScript

# Initialize with a configuration file
app = FortScript(config_path="fort_config.yaml")

# Run the management loop
app.run()
```

### Main Features

- **Intelligent Orchestration**: Automatically pauses scripts when detecting configured "heavy" processes.
- **Resource Management**: Protects system stability by terminating linked processes if RAM hits the defined limit.
- **Native Compatibility**: Automatically detects and utilizes `.venv` environments within Python script folders.
- **Full-Stack Support**: Manages Node.js projects through the detection of `package.json` files.

#### 1. Managing Project Modules

FortScript shines when managing various components of the same ecosystem. Instead of manually running each script, you centralize control.

**Example of supported structure:**

```text
my_project/
├── bot_service/
│   ├── .venv/
│   └── main.py
├── api_node/
│   ├── node_modules/
│   └── package.json
└── dashboard.py (FortScript Manager)
```

**config.yaml**:

```yaml
# Internal project modules
projects:
  - name: "Python Worker"
    path: "./bot_service/main.py"
  - name: "Node Server"
    path: "./api_node/package.json"

# Processes that will pause the above scripts
heavy_processes:
  - name: "GTA V"
    process: "gta5"
  - name: "Obs Studio"
    process: "obs64"

# Security limit (RAM %)
ram_threshold: 85
```

---

## 2. CLI

The CLI allows you to use the full power of FortScript directly through the terminal, without needing to write additional Python code, using only the configuration file.

> **⚠️ Note:** The CLI is under **development**. Although project auto-detection is still being refined, the base command to run the `config.yaml` file is already operational.

### Global CLI Installation (Recommended)

To use the `fort` command anywhere on the system, we recommend installing via **pipx**:

```bash
pipx install fortscript
```

### How to use

Navigate to your project folder (where `config.yaml` is) and run:

```bash
fort
```

---

## Roadmap & Features

- [x] **Monitor Heavy Processes**: Detection of resource-intensive apps.
- [x] **Monitor RAM Usage**: Automatic triggers based on percentage.
- [x] **Unified Executor**:
  - [x] Python Scripts (`.py`) with automatic `.venv` support.
  - [x] Node.js Projects (`package.json`) via `npm`.
  - [ ] Native executables (`.exe`).
- [x] **Tree-kill**: Correctly terminates the entire process tree (avoids orphan processes).
- [ ] **System Tray Interface**: Silent background operation.

---

## Contribution

Contributions are vital! See our [Contribution Guide](CONTRIBUTING.md) to find out how to help.

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

---

Developed with ❤️ by [WesleyyDev](https://github.com/WesleyQDev)
