# FortScript

Um supervisor de processos com controle de execução baseado no estado dos recursos do sistema.

[English](README.md) | [Português](README_ptBR.md)


## 1. Biblioteca Python

O FortScript pode ser integrado em qualquer projeto Python como uma biblioteca para gerenciar scripts filhos.

Você pode usar o FortScript para iniciar scripts e parar quando determinada quantidade de memória RAM for usada. Ou quando determinado aplicativo/processo for inicializado.

Um caso de uso por exemplo seria utilizar a biblioteca para uma criação de um Modo gaming, onde dentro do seu projeto você consegue definir scripts que serão pausados quando determinados jogos forem iniciados e retomados quando os jogos forem fechados.

### Instalação
O FortScript foi desenvolvido utilizando UV. Recomendamos o uso do UV para instalar a biblioteca.

```bash
uv add fortscript
```

Se você estiver usando o Python padrão, você pode instalar a biblioteca do FortScript com o pip.

```bash
pip install fortscript
```

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

#### 1. Gerenciando Módulos Independentes
Você pode usar o FortScript como um controlador central para vários scripts espalhados pelo seu sistema.

**config.yaml**:
```yaml
# Lista de projetos a serem gerenciados
projects:
  - name: "Bot de Trade"
    path: "C:/Users/Dev/Finance/bot.py"
  - name: "Monitor de Servidor"
    path: "C:/Users/Dev/Server/monitor.js"

# Processos que, quando detectados, pausarão seus projetos
heavy_processes:
  - name: "Fortnite"
    process: "fortnite"
  - name: "Editor de Vídeo"
    process: "resolve"

# Limite de porcentagem de uso de RAM para acionar o desligamento seguro
ram_threshold: 90
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

### Opções de Configuração

O arquivo `config.yaml` suporta os seguintes campos:

| Campo | Descrição | Tipo | Padrão |
| :--- | :--- | :--- | :--- |
| `projects` | Lista de aplicações para gerenciar. Cada item precisa de `name` e `path`. | Lista | `[]` |
| `heavy_processes` | Lista de processos que ativam a pausa. Cada item precisa de `name` e `process` (parte do nome do executável). | Lista | `[]` |
| `ram_threshold` | Porcentagem máxima de uso de RAM permitida antes de parar os scripts. | Inteiro | `80` |

---

## 2. CLI

A CLI é uma interface projetada para um público amplo, permitindo o gerenciamento fácil de processos.

### Uso
Se você estiver desenvolvendo localmente:
```bash
uv run fort
```
Após a instalação, basta executar:
```bash
fort
```

- **Configuração**: A CLI procura por um arquivo `config.yaml` no mesmo diretório do script.
- **Auto-detecção**: Em breve, será possível adicionar o script principal de inicialização à CLI executando apenas um comando dentro da pasta do projeto.

---

## Roadmap & Funcionalidades

A lista a seguir acompanha o progresso de nossas funcionalidades e futuras implementações:

- [x] **Monitorar Processos Pesados**: Detecção de aplicativos que consomem muitos recursos.
- [x] **Monitorar Uso de Memória RAM**: Gatilhos automáticos baseados na porcentagem de memória.
- [x] **Executor de Scripts Unificado**:
    - [ ] Executáveis nativos (`.exe`)
    - [x] Scripts Python (`.py`)
    - [ ] Projetos JavaScript/TypeScript (`package.json`)
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

