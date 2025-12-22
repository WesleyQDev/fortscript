<div align="center" id="top">
  <a href="https://pypi.org/project/fortscript/">
    <picture>
      <img src="docs/logo.png" alt="FortScript">
    </picture>
  </a>

  <br />

  <a href="https://pypi.org/project/fortscript/">
    <img src="https://img.shields.io/pypi/v/fortscript?style=flat-square&color=blue" alt="PyPI">
  </a>
  <a href="https://pypi.org/project/fortscript/">
    <img src="https://img.shields.io/pypi/pyversions/fortscript?style=flat-square" alt="Python">
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="License">
  </a>
</div>

<div align="center">
  <a href="https://github.com/WesleyQDev/fortscript">English</a>
  <span>&nbsp;&nbsp;•&nbsp;&nbsp;</span>
  <a href="https://github.com/WesleyQDev/fortscript/blob/main/README_ptBR.md">Português</a>
  <br />
</div>

<br />

## What is FortScript?

Have you ever left a bot, an API, or a script running in the background while gaming, only to notice the game started lagging? Or forgot about processes silently consuming memory until your PC slowed down?

**FortScript solves this automatically.** It pauses your scripts when you open a game or resource-heavy application, and resumes them when you close it. Simple as that.

### How it works

1. You define which scripts you want to manage (Python bots, Node.js projects, etc.)
2. You define which applications are "heavy" (games, video editors, etc.)
3. FortScript monitors and does the rest: pauses when needed, resumes when possible.

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

- **Python 3.12+**
- **Node.js** (only if managing JavaScript/TypeScript projects)

---

## Configuration

Regardless of how you use FortScript (code or CLI), configuration is done through a `config.yaml` file:

```yaml
# Scripts that FortScript will manage
projects:
  - name: "My Discord Bot"
    path: "./bot/main.py"
  - name: "Node API"
    path: "./api/package.json"

# Applications that will pause the scripts above
heavy_processes:
  - name: "GTA V"
    process: "gta5"
  - name: "OBS Studio"
    process: "obs64"

# Pause scripts if RAM exceeds this limit (%)
ram_threshold: 85
```

**Explanation:**
- `projects`: List of scripts/projects that FortScript will start and manage.
- `heavy_processes`: When any of these applications open, scripts are paused.
- `ram_threshold`: If system RAM exceeds this value, scripts are also paused.

### Supported project types

| Type | Extension | Behavior |
|------|-----------|----------|
| Python | `.py` | Automatically detects `.venv` in the script's folder |
| Node.js | `package.json` | Runs `npm run start` |

---

## How to Use

### Option 1: Via Python code

Ideal for integrating FortScript into an existing project or having programmatic control:

```python
from fortscript import FortScript

app = FortScript(config_path="config.yaml")
app.run()
```

### Option 2: Via CLI (terminal)

Ideal for quick use without writing code:

```bash
# Navigate to the folder with your config.yaml
cd my_project

# Run
fort
```

> **Note:** The CLI currently runs FortScript from the `config.yaml`. Additional commands like `fort add` are planned for future versions.

---

## Practical Example

Imagine you have the following project structure:

```text
my_project/
├── discord_bot/
│   ├── .venv/
│   └── main.py
├── express_api/
│   ├── node_modules/
│   └── package.json
├── config.yaml
└── manager.py
```

The `manager.py` would be:

```python
from fortscript import FortScript

app = FortScript(config_path="config.yaml")
app.run()
```

When you open GTA V, FortScript automatically:
1. Pauses the Discord bot
2. Pauses the Express API
3. Displays the pause reason in the terminal

When you close GTA V, everything resumes automatically.

---

## Roadmap

### Library

- [ ] **`.exe` support**: Manage executables directly.
- [ ] **Configuration via arguments**: Pass `projects`, `heavy_processes`, and `ram_threshold` directly in code, without needing a YAML file.
- [ ] **Custom functions**: Manage Python functions beyond external files.
- [ ] **Games module**: Pre-defined list of popular games.

**Games module preview:**

```python
from fortscript import FortScript
from fortscript.games import GAMES

# GAMES contains dozens of popular games
app = FortScript(heavy_processes=GAMES)
app.run()
```

| Included games | |
|----------------|---|
| Minecraft, GTA V, Fortnite | Counter-Strike 2, Valorant, League of Legends |
| Roblox, Apex Legends | ...and many more |

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
- [x] Python script support with `.venv` detection
- [x] Node.js project support via `npm run start`
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
