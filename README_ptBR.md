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

### Como funciona

1. Você define quais scripts quer gerenciar (bots Python, projetos Node.js, etc.)
2. Você define quais aplicativos são "pesados" (jogos, editores de vídeo, etc.)
3. O FortScript monitora e faz o resto: pausa quando necessário, retoma quando possível.

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

- **Python 3.12+**
- **Node.js** (apenas se for gerenciar projetos JavaScript/TypeScript)

---

## Configuração

Independente de como você usa o FortScript (código ou CLI), a configuração é feita através de um arquivo `config.yaml`:

```yaml
# Scripts que o FortScript vai gerenciar
projects:
  - name: "Meu Bot Discord"
    path: "./bot/main.py"
  - name: "API Node"
    path: "./api/package.json"

# Aplicativos que vão pausar os scripts acima
heavy_processes:
  - name: "GTA V"
    process: "gta5"
  - name: "OBS Studio"
    process: "obs64"

# Pausa os scripts se a RAM ultrapassar este limite (%)
ram_threshold: 85
```

**Explicação:**
- `projects`: Lista de scripts/projetos que o FortScript vai iniciar e gerenciar.
- `heavy_processes`: Quando qualquer um desses aplicativos abrir, os scripts são pausados.
- `ram_threshold`: Se a RAM do sistema ultrapassar esse valor, os scripts também são pausados.

### Tipos de projeto suportados

| Tipo | Extensão | Comportamento |
|------|----------|---------------|
| Python | `.py` | Detecta automaticamente `.venv` na pasta do script |
| Node.js | `package.json` | Executa `npm run start` |

---

## Como Usar

### Opção 1: Via código Python

Ideal para integrar o FortScript em um projeto existente ou ter controle programático:

```python
from fortscript import FortScript

app = FortScript(config_path="config.yaml")
app.run()
```

### Opção 2: Via CLI (terminal)

Ideal para uso rápido sem escrever código:

```bash
# Navegue até a pasta com seu config.yaml
cd meu_projeto

# Execute
fort
```

> **Nota:** A CLI atualmente executa o FortScript a partir do `config.yaml`. Comandos adicionais como `fort add` estão planejados para versões futuras.

---

## Exemplo Prático

Imagine que você tem a seguinte estrutura de projeto:

```text
meu_projeto/
├── bot_discord/
│   ├── .venv/
│   └── main.py
├── api_express/
│   ├── node_modules/
│   └── package.json
├── config.yaml
└── gerenciador.py
```

O `gerenciador.py` seria:

```python
from fortscript import FortScript

app = FortScript(config_path="config.yaml")
app.run()
```

Quando você abrir o GTA V, o FortScript automaticamente:
1. Pausa o bot Discord
2. Pausa a API Express
3. Exibe no terminal o motivo da pausa

Quando você fechar o GTA V, tudo volta a funcionar automaticamente.

---

## Roadmap

### Biblioteca

- [ ] **Suporte a `.exe`**: Gerenciar executáveis diretamente.
- [ ] **Configuração via argumentos**: Passar `projects`, `heavy_processes` e `ram_threshold` diretamente no código, sem precisar de arquivo YAML.
- [ ] **Funções customizadas**: Gerenciar funções Python além de arquivos externos.
- [ ] **Módulo Games**: Lista pré-definida de jogos populares.

**Prévia do módulo Games:**

```python
from fortscript import FortScript
from fortscript.games import GAMES

# GAMES contém dezenas de jogos populares
app = FortScript(heavy_processes=GAMES)
app.run()
```

| Jogos incluídos | |
|-----------------|---|
| Minecraft, GTA V, Fortnite | Counter-Strike 2, Valorant, League of Legends |
| Roblox, Apex Legends | ...e muitos outros |

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
- [x] Suporte a scripts Python com detecção de `.venv`
- [x] Suporte a projetos Node.js via `npm run start`
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
