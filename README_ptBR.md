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
  <a href="https://github.com/WesleyQDev/fortscript">English</a>
  &nbsp;•&nbsp;
  <a href="https://github.com/WesleyQDev/fortscript/blob/main/README_ptBR.md"><strong>Português</strong></a>
</p>

<br />

## O que é FortScript?

Você já deixou um bot, uma API ou um script rodando em segundo plano enquanto jogava, e o jogo começou a travar? Ou esqueceu processos consumindo memória até o PC ficar lento?

**FortScript resolve isso automaticamente.** Ele pausa seus scripts quando você abre um jogo ou aplicativo pesado, e retoma quando você fecha. Simples assim.

**Multiplaforma** FortScript foi desenvolvido para funcionar em qualquer plataforma seja Windows, Linux ou MacOS.

### Como funciona

1. Você define quais scripts quer gerenciar (bots Python, projetos Node.js, executáveis, etc.)
2. Você define quais aplicativos são "pesados" (jogos, editores de vídeo, etc.)
3. O FortScript monitora e faz o resto: pausa quando necessário, retoma quando possível.

**Eventos de Callback (opcional):** Você pode configurar funções que serão executadas automaticamente quando os scripts forem pausados ou retomados:

- **`on_pause`**: Função executada quando os scripts são pausados (ex: enviar notificação, salvar estado)
- **`on_resume`**: Função executada quando os scripts são retomados (ex: reconectar serviços, logar retorno)

Isso é útil para integrar com sistemas de notificação, logs personalizados ou qualquer ação que você queira executar nesses momentos.

## Instalação

O FortScript pode ser usado de **duas formas**: como biblioteca Python ou via linha de comando (CLI). Ambas vêm no mesmo pacote.

### Instalação como dependência do projeto

Use esta opção se você quer integrar o FortScript em um projeto Python existente:

```bash
# UV (recomendado)
uv add fortscript

# Poetry
poetry add fortscript

# pip
pip install fortscript
```

### Instalação global (CLI)

Use esta opção se você quer usar o comando `fort` diretamente no terminal, sem escrever código:

```bash
pipx install fortscript
```

### Pré-requisitos

- **Python 3.10+**
- **Node.js** (apenas se for gerenciar projetos JavaScript/TypeScript)

---

## Configuração

O FortScript pode ser configurado de **duas formas**: através de um arquivo YAML ou diretamente via argumentos no código Python.

### Opção 1: Arquivo YAML

Crie um arquivo chamado `fortscript.yaml` na raiz do seu projeto:

```yaml
# ====================================
# CONFIGURAÇÃO FORTSCRIPT
# ====================================

# Scripts/projetos que o FortScript vai gerenciar
# O FortScript inicia esses processos automaticamente
projects:
  - name: "Meu Bot Discord" # Nome amigável (aparece nos logs)
    path: "./bot/main.py" # Script Python (.py)

  - name: "API Node"
    path: "./api/package.json" # Projeto Node.js (package.json)

  - name: "Servidor Local"
    path: "./server/app.exe" # Executável Windows (.exe)

# Aplicativos que vão pausar os scripts acima
# Quando qualquer um desses processos for detectado, os scripts param
heavy_processes:
  - name: "GTA V" # Nome amigável
    process: "gta5" # Nome do processo (sem .exe)

  - name: "OBS Studio"
    process: "obs64"

  - name: "Cyberpunk 2077"
    process: "cyberpunk2077"

  - name: "Premiere Pro"
    process: "premiere"

# Limite de RAM para pausar os scripts (%)
# Se a RAM do sistema ultrapassar esse valor, os scripts são pausados
ram_threshold: 90

# Limite de RAM seguro para retomar os scripts (%)
# Os scripts só voltam quando a RAM cair abaixo desse valor
# Isso evita que fiquem ligando/desligando constantemente (histerese)
ram_safe: 80

# Nível de log (DEBUG, INFO, WARNING, ERROR)
# Use DEBUG para ver informações detalhadas durante desenvolvimento
log_level: "INFO"
```

**Explicação dos campos:**

| Campo                       | Tipo   | Descrição                                          |
| --------------------------- | ------ | -------------------------------------------------- |
| `projects`                  | Lista  | Scripts/projetos que serão iniciados e gerenciados |
| `projects[].name`           | Texto  | Nome amigável que aparece nos logs                 |
| `projects[].path`           | Texto  | Caminho para o arquivo do projeto                  |
| `heavy_processes`           | Lista  | Aplicativos que pausam os scripts quando abertos   |
| `heavy_processes[].name`    | Texto  | Nome amigável do aplicativo                        |
| `heavy_processes[].process` | Texto  | Nome do processo (sem extensão .exe)               |
| `ram_threshold`             | Número | % de RAM para pausar os scripts (padrão: 95)       |
| `ram_safe`                  | Número | % de RAM para retomar os scripts (padrão: 85)      |
| `log_level`                 | Texto  | Nível de log: DEBUG, INFO, WARNING, ERROR          |

### Opção 2: Argumentos no Código

Você pode passar todas as configurações diretamente no código Python, sem precisar de arquivo YAML:

```python
from fortscript import FortScript

app = FortScript(
    projects=[
        {"name": "Meu Bot", "path": "./bot/main.py"},
        {"name": "API Node", "path": "./api/package.json"},
    ],
    heavy_process=[
        {"name": "GTA V", "process": "gta5"},
        {"name": "OBS Studio", "process": "obs64"},
    ],
    ram_threshold=90,
    ram_safe=80,
    log_level="INFO",
)

app.run()
```

> **Dica:** Você pode combinar as duas formas! Argumentos passados no código sobrescrevem os valores do arquivo YAML.

Fortscript está em constante evolução, em próximas versões sera possivel executar projetos de outras linguagens, assim como poder escolher a forma de como o projeto sera iniciado como qual gerenciador de pacotes usar para iniciar o script/projeto.

### Tipos de projeto/script atualmente suportados

| Tipo       | Extensão/Arquivo | Comportamento                                      |
| ---------- | ---------------- | -------------------------------------------------- |
| Python     | `.py`            | Detecta automaticamente `.venv` na pasta do script |
| Node.js    | `package.json`   | Executa `npm run start`                            |
| Executável | `.exe`           | Executa diretamente (Windows)                      |

---

## Como Usar

### Opção 1: Configuração básica (só arquivo YAML)

A forma mais simples de usar o FortScript:

```python
from fortscript import FortScript

# Carrega configurações do fortscript.yaml
app = FortScript()
app.run()
```

### Opção 2: Configuração via argumentos (sem arquivo YAML)

Passe todas as configurações diretamente no código:

```python
from fortscript import FortScript

app = FortScript(
    projects=[
        {"name": "Meu Bot Discord", "path": "./bot/main.py"},
    ],
    heavy_process=[
        {"name": "Valorant", "process": "valorant"},
        {"name": "League of Legends", "process": "leagueclient"},
    ],
    ram_threshold=90,
    ram_safe=80,
    log_level="INFO",
)

app.run()
```

### Opção 3: Com callbacks de eventos

Execute funções personalizadas quando os scripts são pausados ou retomados:

```python
from fortscript import FortScript

def quando_pausar():
    print("🎮 Modo gaming ativado! Scripts pausados.")
    # Você pode: enviar notificação, salvar estado, etc.

def quando_retomar():
    print("💻 Voltando ao trabalho! Scripts retomados.")
    # Você pode: reconectar serviços, logar retorno, etc.

app = FortScript(
    config_path="fortscript.yaml",
    on_pause=quando_pausar,    # Função executada ao pausar
    on_resume=quando_retomar,  # Função executada ao retomar
)

app.run()
```

### Opção 4: Configuração completa (todos os argumentos)

Exemplo com todos os parâmetros disponíveis:

```python
from fortscript import FortScript

def notificar_pausa():
    print("⏸️ Scripts pausados!")

def notificar_retomada():
    print("▶️ Scripts retomados!")

app = FortScript(
    config_path="fortscript.yaml",           # Arquivo de configuração (opcional)
    projects=[                                # Lista de projetos
        {"name": "Bot Discord", "path": "./bot/main.py"},
        {"name": "API Express", "path": "./api/package.json"},
        {"name": "Servidor", "path": "./server/app.exe"},
    ],
    heavy_process=[                           # Processos pesados
        {"name": "GTA V", "process": "gta5"},
        {"name": "Cyberpunk 2077", "process": "cyberpunk2077"},
    ],
    ram_threshold=90,                         # Pausar se RAM > 90%
    ram_safe=80,                              # Retomar se RAM < 80%
    on_pause=notificar_pausa,                 # Callback ao pausar
    on_resume=notificar_retomada,             # Callback ao retomar
    log_level="DEBUG",                        # Nível de log
)

app.run()
```

### Opção 5: Via CLI (terminal)

Ideal para uso pessoal, sem escrever código

```bash
fort
```

> **Nota:** A CLI atualmente executa o FortScript a partir do `src\fortscript\cli\fortscript.yaml` o que não seria o ideal. Em versões futuras as configurações serão guardadas globalmente e comandos adicionais como `fort add` serão adicionados.

---

## Exemplo Prático: Modo Gaming

Imagine que você é um desenvolvedor que roda scripts de trabalho (bots, APIs, automações) durante o dia, mas quer jogar à noite sem que o PC fique travando.

### Estrutura do projeto

```text
meu_projeto/
├── bot_discord/
│   ├── .venv/
│   └── main.py              # Bot que consome RAM
├── api_local/
│   ├── node_modules/
│   └── package.json         # API Express rodando localmente
├── automacao/
│   └── backup.exe           # Script de backup automático
├── fortscript.yaml
└── modo_gaming.py
```

### Arquivo `fortscript.yaml`

```yaml
projects:
  - name: "Bot Discord"
    path: "./bot_discord/main.py"
  - name: "API Local"
    path: "./api_local/package.json"
  - name: "Backup Automático"
    path: "./automacao/backup.exe"

heavy_processes:
  - name: "GTA V"
    process: "gta5"
  - name: "Cyberpunk 2077"
    process: "cyberpunk2077"
  - name: "Valorant"
    process: "valorant"
  - name: "League of Legends"
    process: "leagueclient"
  - name: "CS2"
    process: "cs2"
  - name: "Fortnite"
    process: "fortnite"
  - name: "Apex Legends"
    process: "r5apex"

ram_threshold: 85
ram_safe: 75
log_level: "INFO"
```

### Arquivo `modo_gaming.py` (versão completa com todos os argumentos)

```python
import os
from fortscript import FortScript

# Caminhos dos projetos
base_dir = os.path.dirname(os.path.abspath(__file__))
bot_path = os.path.join(base_dir, "bot_discord", "main.py")
api_path = os.path.join(base_dir, "api_local", "package.json")
backup_path = os.path.join(base_dir, "automacao", "backup.exe")

# Projetos que serão gerenciados
meus_projetos = [
    {"name": "Bot Discord", "path": bot_path},
    {"name": "API Local", "path": api_path},
    {"name": "Backup Automático", "path": backup_path},
]

# Jogos e aplicativos pesados
meus_jogos = [
    {"name": "GTA V", "process": "gta5"},
    {"name": "Cyberpunk 2077", "process": "cyberpunk2077"},
    {"name": "Valorant", "process": "valorant"},
    {"name": "League of Legends", "process": "leagueclient"},
    {"name": "CS2", "process": "cs2"},
    {"name": "Fortnite", "process": "fortnite"},
    {"name": "Apex Legends", "process": "r5apex"},
    {"name": "Premiere Pro", "process": "premiere"},
    {"name": "After Effects", "process": "afterfx"},
]


def ao_pausar():
    """Executado quando os scripts são pausados."""
    print("=" * 50)
    print("🎮 MODO GAMING ATIVADO!")
    print("Seus scripts foram pausados para liberar recursos.")
    print("Bom jogo! 🚀")
    print("=" * 50)
    # Aqui você pode: enviar notificação, webhook Discord, etc.


def ao_retomar():
    """Executado quando os scripts são retomados."""
    print("=" * 50)
    print("💻 MODO TRABALHO ATIVADO!")
    print("Jogo fechado. Retomando seus scripts...")
    print("De volta ao trabalho! 📊")
    print("=" * 50)
    # Aqui você pode: reconectar serviços, enviar log, etc.


# Inicializa o FortScript com TODOS os argumentos disponíveis
app = FortScript(
    config_path="fortscript.yaml",    # Arquivo de configuração base (opcional)
    projects=meus_projetos,           # Lista de projetos para gerenciar
    heavy_process=meus_jogos,         # Lista de processos pesados
    ram_threshold=85,                 # Pausar se RAM ultrapassar 85%
    ram_safe=75,                      # Retomar apenas quando RAM < 75%
    on_pause=ao_pausar,               # Função callback ao pausar
    on_resume=ao_retomar,             # Função callback ao retomar
    log_level="DEBUG",                # Nível de log (DEBUG para ver tudo)
)


if __name__ == "__main__":
    print("🎯 FortScript: Modo Gaming")
    print("Monitorando sistema... Abra um jogo para testar!")
    print("-" * 50)
    app.run()
```

### Como funciona

1. **Inicie o script:** `python modo_gaming.py`
2. **Abra qualquer jogo da lista** (GTA V, Valorant, etc.)
3. **FortScript automaticamente:**
   - Detecta o jogo
   - Pausa o Bot Discord, API e Backup
   - Executa a função `ao_pausar()` (mostra mensagem de gaming)
4. **Feche o jogo**
5. **FortScript automaticamente:**
   - Detecta que o jogo fechou
   - Aguarda a RAM estabilizar abaixo de 75%
   - Retoma todos os scripts
   - Executa a função `ao_retomar()` (mostra mensagem de trabalho)

---

## Roadmap
> Se tiver uma ideia você pode sugerir novas funcionalidades criando uma `issue`

### Biblioteca

- [ ] **Funções customizadas**: Gerenciar funções Python criando treadhs.
- [ ] **Condições por Projeto** permitir que um projeto específico só pause se um aplicativo específico abrir. Exemplo: "Pausar o script do bot apenas se o Cyberpunk2077 abrir, mas deixar o Bot do Discord rodando".
- [ ] Tentar fazer um encerramento amigavel do script antes de usar um terminate()
- [ ] Tratamento de Processos Mortos: Se um script que o FortScript iniciou fechar sozinho (erro ou crash), a biblioteca ainda vai achar que ele está rodando até o próximo ciclo. Seria bom verificar se o processo ainda está "alive" periodicamente.
- [ ]bstração de Projetos (Refatoração): Atualmente, o 
start_scripts
 tem um if/elif gigante para detectar o tipo de arquivo. Seria muito mais elegante ter classes separadas: PythonProject, NodeProject, ExeProject, todas herdando de uma classe base Project. Assim, adicionar um novo tipo (como Go ou Docker) seria apenas criar uma nova classe.
- Type Hinting: Adicione dicas de tipo em todos os métodos para melhorar o intellisense para quem for usar sua biblioteca. Exm: def load_config(self, path: str) -> dict:.
### CLI

- [ ] **System Tray**: Rodar minimizado na bandeja do sistema.
- [ ] **Comandos adicionais**:
  - `fort add <path>` - Adicionar projeto ao config
  - `fort list` - Listar projetos configurados
  - `fort remove <name>` - Remover projeto


---

## Funcionalidades Atuais

- [x] Pausa automática ao detectar aplicativos pesados
- [x] Pausa automática por limite de RAM
- [x] Retomada com histerese (ram_safe vs ram_threshold)
- [x] Suporte a scripts Python com detecção de `.venv`
- [x] Suporte a projetos Node.js via `npm run start`
- [x] Suporte a executáveis `.exe` (Windows)
- [x] Configuração via arquivo YAML (`fortscript.yaml`)
- [x] Configuração via argumentos no código
- [x] Callbacks de eventos (`on_pause` e `on_resume`)
- [x] Níveis de log configuráveis (DEBUG, INFO, WARNING, ERROR)
- [x] Encerramento seguro de processos (tree-kill)

---

## Contribuição

Contribuições são bem-vindas! Veja o [Guia de Contribuição](CONTRIBUTING.md) para começar.

## Licença

MIT - Veja [LICENSE](LICENSE) para detalhes.

---

<div align="center">
  Desenvolvido com ❤️ por <a href="https://github.com/WesleyQDev">WesleyQDev</a>
</div>
