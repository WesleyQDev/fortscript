# FortScript

<<<<<<< HEAD
**Gerenciador inteligente de scripts que pausa automaticamente quando processos pesados estão em execução.**

## 📋 Descrição

FortScript é uma ferramenta que monitora continuamente processos em execução no seu computador. Quando um processo configurado é detectado (como jogos), todos os scripts são automaticamente pausados para liberar recursos do sistema. Assim que o processo é fechado, os scripts são reiniciados automaticamente.

**Ideal para:**

- 🎮 Jogos que exigem máximo desempenho (Fortnite, Valorant, CS2, etc.)
- 🖥️ Aplicações de edição de vídeo/imagem
- 🔧 Qualquer software que demande muitos recursos

## ⚙️ Funcionalidades

- 🔍 **Detecção automática** de processos em execução
- ⏸️ **Pausa automática** de todos os scripts quando o processo inicia
- ▶️ **Reinício automático** dos scripts quando o processo fecha
- 📁 Suporte a scripts `.bat`, `.py` e `.exe`
- 🔄 Verificação periódica configurável
- 🎯 Lista personalizável de processos a monitorar
- 🖥️ **CLI interativa** com interface rica para gerenciar configurações
- 💾 Configuração persistente em JSON

## 📦 Requisitos

- Python 3.12 ou superior
- [UV](https://github.com/astral-sh/uv) (gerenciador de pacotes)

## 🚀 Instalação

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/fortscript.git
cd fortscript
```

2. Instale as dependências com UV:

```bash
uv sync
```

3. (Opcional) Instale globalmente para usar o comando `fort` de qualquer lugar:

```bash
uv tool install -e .
```

## 📖 Como Usar

### CLI - Gerenciador de Processos

O FortScript possui uma CLI interativa para gerenciar os processos monitorados:

```bash
# Se instalado globalmente
fort

# Ou usando uv run
uv run fort
```

#### Comandos Disponíveis

| Comando                      | Descrição                            | Exemplo                  |
| ---------------------------- | ------------------------------------ | ------------------------ |
| `fort list`                  | Lista todos os processos monitorados | `fort list`              |
| `fort add <nome>`            | Adiciona um novo processo            | `fort add "cs2.exe"`     |
| `fort remove <id/nome>`      | Remove um processo (por ID ou nome)  | `fort remove 1`          |
| `fort edit <id/nome> <novo>` | Edita o nome de um processo          | `fort edit 1 "novo.exe"` |
| `fort interval <segundos>`   | Define o intervalo de verificação    | `fort interval 10`       |
| `fort clear`                 | Remove todos os processos            | `fort clear`             |

#### Exemplos de Uso

```bash
# Listar processos configurados
fort list

# Adicionar um novo processo para monitorar
fort add "VALORANT-Win64-Shipping.exe"

# Remover pelo ID
fort remove 2

# Alterar intervalo de verificação para 10 segundos
fort interval 10

# Modo interativo (sem argumentos, pergunta o que fazer)
fort add
fort remove
```

### Iniciar o Monitoramento

Execute o arquivo `start.bat` ou rode diretamente:

```bash
uv run main.py
```

### Adicionar Scripts

Coloque seus scripts na pasta `scripts/`. Os seguintes formatos são suportados:

- `.bat` - Arquivos batch do Windows
- `.py` - Scripts Python
- `.exe` - Executáveis

Todos os scripts nesta pasta serão executados automaticamente quando o FortScript iniciar e pausados quando um processo monitorado for detectado.

## 📂 Estrutura do Projeto

```
fortscript/
├── main.py          # Script principal de monitoramento
├── cli.py           # CLI interativa (Typer + Rich)
├── config.json      # Configuração de processos e intervalo
├── pyproject.toml   # Configuração do projeto e dependências
├── start.bat        # Inicializador rápido
├── scripts/         # Pasta para seus scripts
│   ├── bot.bat
│   └── rewards.bat
└── README.md        # Este arquivo
```

## ⚙️ Configuração

A configuração é gerenciada pelo arquivo `config.json`:

```json
{
  "processes": ["FortniteClient-Win64-Shipping.exe"],
  "poll_interval": 5
}
```

Use a CLI `fort` para editar a configuração de forma interativa, ou edite o arquivo diretamente.

### Exemplos de Processos Populares

| Jogo/Aplicação    | Nome do Processo                    |
| ----------------- | ----------------------------------- |
| Fortnite          | `FortniteClient-Win64-Shipping.exe` |
| Valorant          | `VALORANT-Win64-Shipping.exe`       |
| CS2               | `cs2.exe`                           |
| League of Legends | `League of Legends.exe`             |
| GTA V             | `GTA5.exe`                          |
| Apex Legends      | `r5apex.exe`                        |
| Adobe Premiere    | `Adobe Premiere Pro.exe`            |
| DaVinci Resolve   | `Resolve.exe`                       |

## 💡 Casos de Uso

1. **Gamers**: Pause bots, downloaders ou scripts de automação enquanto joga
2. **Criadores de Conteúdo**: Libere recursos durante edição de vídeo
3. **Desenvolvedores**: Pause processos de build/watch durante testes pesados

## 🛠️ Dependências

- [psutil](https://github.com/giampaolo/psutil) - Monitoramento de processos
- [typer](https://typer.tiangolo.com/) - CLI moderna
- [rich](https://rich.readthedocs.io/) - Interface rica no terminal

## 📄 Licença

MIT
---

Feito com ❤️ para quem precisa de automação inteligente e gerenciamento eficiente de recursos.
=======
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
>>>>>>> v02
