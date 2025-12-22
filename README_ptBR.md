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

## O que é Fortscript?

Fortscript é um supervisor de processos com controle de execução inteligente baseado no estado dos recursos do sistema e atividade de aplicações.

## Biblioteca Python

O FortScript atua como uma camada de controle inteligente para os scripts e serviços do seu projeto. Ele permite automatizar a pausa e a retomada de processos baseado em gatilhos ambientais, como o uso de memória RAM ou a execução de aplicativos específicos.

O foco principal é a **conveniência no desenvolvimento**: garantir que seus módulos de suporte (bots, APIs locais, workers) rodem apenas quando o sistema tem recursos disponíveis ou quando você não está em uma tarefa que exija foco total do hardware (como jogos ou edição de vídeo).

### Pré-requisitos

Antes de instalar, certifique-se de ter os seguintes requisitos:

- **Python**: Versão 3.12 ou superior.
- **Node.js**: (Opcional) Necessário apenas se você for gerenciar projetos JavaScript/TypeScript.
- **Gerenciador de Pacotes**: Recomendamos o [uv](https://github.com/astral-sh/uv) para uma experiência mais rápida, embora não seja obrigatório.

### Instalação

Você pode instalar o FortScript utilizando o gerenciador de sua preferência:

**Usando UV (Recomendado):**

```bash
uv add fortscript
```

**Usando Poetry:**

```bash
poetry add fortscript
```

**Ambiente Virtual (Manual):**

```bash
python -m venv .venv

# No Windows:
.venv\Scripts\activate

# No Linux/macOS:
source .venv/bin/activate

# Após ativar, instale:
pip install fortscript
```

### Início Rápido

```python
from fortscript import FortScript

# Inicialize com um arquivo de configuração
app = FortScript(config_path="fort_config.yaml")

# Execute o loop de gerenciamento
app.run()
```

### Funcionalidades Principais

- **Orquestração Inteligente**: Pausa scripts automaticamente ao detectar processos "pesados" configurados.
- **Gestão de Recursos**: Protege a estabilidade do sistema encerrando processos vinculados se a RAM atingir o limite definido.
- **Compatibilidade Nativa**: Detecta e utiliza automaticamente ambientes `.venv` dentro das pastas dos scripts Python.
- **Suporte Full-Stack**: Gerencia projetos Node.js através da detecção de arquivos `package.json`.

#### 1. Gerenciando Módulos do Projeto

O FortScript brilha ao gerenciar diversos componentes de um mesmo ecossistema. Em vez de rodar manualmente cada script, você centraliza o controle.

**Exemplo de estrutura suportada:**

```text
meu_projeto/
├── bot_servico/
│   ├── .venv/
│   └── main.py
├── api_node/
│   ├── node_modules/
│   └── package.json
└── dashboard.py (Gerenciador FortScript)
```

**config.yaml**:

```yaml
# Módulos internos do projeto
projects:
  - name: "Worker Python"
    path: "./bot_servico/main.py"
  - name: "Servidor Node"
    path: "./api_node/package.json"

# Processos que pausarão os scripts acima
heavy_processes:
  - name: "GTA V"
    process: "gta5"
  - name: "Obs Studio"
    process: "obs64"

# Limite de segurança (RAM %)
ram_threshold: 85
```

---

## 2. CLI

A CLI permite que você utilize todo o poder do FortScript diretamente pelo terminal, sem precisar escrever código Python adicional, usando apenas o arquivo de configuração.

> **⚠️ Nota:** A CLI está em **desenvolvimento**. Embora a auto-detecção de projetos ainda esteja sendo refinada, o comando base para rodar o arquivo `config.yaml` já está operacional.

### Instalação Global da CLI (Recomendado)

Para usar o comando `fort` em qualquer lugar do sistema, recomendamos a instalação via **pipx**:

```bash
pipx install fortscript
```

### Como usar

Navegue até a pasta do seu projeto (onde está o `config.yaml`) e execute:

```bash
fort
```

---

## Roadmap & Funcionalidades

- [x] **Monitorar Processos Pesados**: Detecção de apps que consomem muitos recursos.
- [x] **Monitorar Uso de RAM**: Gatilhos automáticos baseados em porcentagem.
- [x] **Executor Unificado**:
  - [x] Scripts Python (`.py`) com suporte automático a `.venv`.
  - [x] Projetos Node.js (`package.json`) via `npm`.
  - [ ] Executáveis nativos (`.exe`).
- [x] **Tree-kill**: Encerra corretamente toda a árvore de processos (evita processos órfãos).
- [ ] **Interface de Bandeja (System Tray)**: Operação silenciosa em segundo plano.

---

## Contribuição

Contribuições são fundamentais! Veja o nosso [Guia de Contribuição](CONTRIBUTING.md) para saber como ajudar.

## Licença

Distribuído sob a Licença MIT. Veja `LICENSE` para mais informações.

---

Desenvolvido com ❤️ por [WesleyyDev](https://github.com/WesleyQDev)
