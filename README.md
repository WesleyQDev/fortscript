# FortScript

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
