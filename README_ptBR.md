# FortScript

Um supervisor de processos com controle de execução baseado no estado dos recursos do sistema.

[English](README.md) | [Português](README_PT-BR.md)

**FortScript** é um Process Manager em Python, baseado em monitoramento de RAM e detecção de processos do sistema operacional, que inicia, pausa e encerra aplicações automaticamente usando políticas reativas de consumo de recursos.

---

## 1. A Biblioteca

O FortScript pode ser integrado em qualquer projeto Python como uma biblioteca para gerenciar processos filhos e monitorar a saúde do sistema.

### Início Rápido
```python
from fortscript import FortScript

# Inicialize com um arquivo de configuração
app = FortScript(config_path="minha_config.yaml")

# Execute o loop de gerenciamento
app.run()
```

### Por que usar a biblioteca?
-   **Ciclo de Vida Limpo**: Inicie e pare processos filhos com segurança (incluindo árvores de processos completas).
-   **Monitoramento de Recursos**: Hooks integrados para uso de RAM e atividade de processos.
-   **Multi-Runtime**: Suporta Python, Node.js (pnpm) e Executáveis nativos.

### Exemplos de Uso

#### 1. Gerenciando Módulos Independentes
Você pode usar o FortScript como um controlador central para vários scripts espalhados pelo seu sistema.

**config.yaml**:
```yaml
projects:
  - name: "Bot de Trade"
    path: "C:/Users/Dev/Finance/bot.py"
  - name: "Monitor de Servidor"
    path: "C:/Users/Dev/Server/monitor.js"
```

#### 2. Integração em projetos maiores
Importe o `FortScript` no ponto de entrada da sua aplicação principal para lidar com tarefas de segundo plano automaticamente.

```python
# controlador_principal.py
from fortscript import FortScript

def iniciar_servicos():
    # Detecta jogos/apps pesados e pausa esses serviços automaticamente
    gerenciador = FortScript(config_path="./config_servicos.yaml")
    gerenciador.run()
```

---

## 2. CLI

A CLI é uma interface projetada para um público amplo, permitindo o gerenciamento fácil de processos.

> **Nota:** A CLI está atualmente em desenvolvimento. Em breve estará disponível diretamente via `pip`.

- **Configuração**: Os paths dos arquivos de inicialização dos seus scripts ficam localizados em `cli/config.yaml`.
- **Futuro**: Em breve, será possível adicionar o script principal de inicialização à CLI executando apenas um comando dentro da pasta do projeto.

### Uso
```bash
uv run cli/cli.py
```

---

## Roadmap & Funcionalidades

A lista a seguir acompanha o progresso de nossas funcionalidades e futuras implementações:

- [x] **Monitorar Processos Pesados**: Detecção de aplicativos que consomem muitos recursos.
- [x] **Monitorar Uso de Memória RAM**: Gatilhos automáticos baseados na porcentagem de memória.
- [x] **Executor de Scripts Unificado**:
    - [x] Executáveis nativos (`.exe`)
    - [x] Scripts Python (`.py`)
    - [x] Projetos JavaScript/TypeScript (`package.json`)
- [ ] **Integração com o Sistema**:
    - [ ] Iniciar automaticamente com o Windows/Linux.
    - [ ] Suporte a System Tray (ícone na barra de tarefas) para operação em segundo plano.
- [x] **Interrupção Inteligente**:
    - [x] Parada automática quando processos pesados são detectados.
    - [x] Retomada automática quando os processos são fechados.
    - [x] Ciclo de parada/retomada baseado em RAM.

---

## Contribuição

Contribuições são bem-vindas! Por favor, leia o nosso [Guia de Contribuição](CONTRIBUTING.md) para detalhes sobre o nosso código de conduta e o processo para enviar pull requests.

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

Desenvolvido com ❤️ por [WesleyyDev](https://github.com/WesleyQDev)

