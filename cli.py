import json
import subprocess
import psutil
from pathlib import Path
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

app = typer.Typer(
    help="🎮 FortScript CLI - Gerenciador de processos monitorados",
    rich_markup_mode="rich",
    add_completion=False,
    no_args_is_help=True,
)
console = Console()
CONFIG_FILE = Path(__file__).parent / "config.json"
PROJECT_DIR = Path(__file__).parent
MAIN_SCRIPT = PROJECT_DIR / "main.py"


def is_fortscript_running() -> tuple[bool, list[psutil.Process]]:
    """Verifica se o FortScript já está rodando."""
    main_path = str(MAIN_SCRIPT).lower()
    running_processes = []
    
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info.get('cmdline') or []
            cmdline_str = ' '.join(cmdline).lower()
            if 'main.py' in cmdline_str and 'fortscript' in cmdline_str:
                running_processes.append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    return len(running_processes) > 0, running_processes


def load_config() -> dict:
    """Carrega a configuração do arquivo JSON."""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"processes": [], "poll_interval": 5}


def save_config(config: dict) -> None:
    """Salva a configuração no arquivo JSON."""
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)


@app.command("list", help="📋 Lista todos os processos monitorados")
def list_processes():
    config = load_config()
    processes = config.get("processes", [])
    
    if not processes:
        console.print(Panel("[yellow]Nenhum processo configurado.[/yellow]", title="Processos"))
        return
    
    table = Table(title="Processos Monitorados", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="cyan", justify="center")
    table.add_column("Nome do Processo", style="green")
    
    for i, process in enumerate(processes, 1):
        table.add_row(str(i), process)
    
    console.print(table)
    console.print(f"\n[dim]Intervalo de verificação: {config.get('poll_interval', 5)} segundos[/dim]")


@app.command("add", help="➕ Adiciona um novo processo para monitorar")
def add_process(nome: str = typer.Argument(None, help="Nome do processo a adicionar")):
    config = load_config()
    
    if nome is None:
        nome = Prompt.ask("[cyan]Nome do processo[/cyan]")
    
    if not nome.strip():
        console.print("[red]❌ Nome do processo não pode ser vazio.[/red]")
        raise typer.Exit(1)
    
    if nome in config["processes"]:
        console.print(f"[yellow]⚠️ Processo '{nome}' já está na lista.[/yellow]")
        raise typer.Exit(1)
    
    config["processes"].append(nome)
    save_config(config)
    console.print(f"[green]✅ Processo '{nome}' adicionado com sucesso![/green]")


@app.command("remove", help="➖ Remove um processo da lista de monitoramento")
def remove_process(nome: str = typer.Argument(None, help="Nome ou ID do processo a remover")):
    config = load_config()
    processes = config.get("processes", [])
    
    if not processes:
        console.print("[yellow]Nenhum processo para remover.[/yellow]")
        raise typer.Exit(1)
    
    if nome is None:
        list_processes()
        nome = Prompt.ask("\n[cyan]Nome ou ID do processo a remover[/cyan]")
    
    # Tenta interpretar como ID (número)
    try:
        idx = int(nome) - 1
        if 0 <= idx < len(processes):
            removed = processes.pop(idx)
            save_config(config)
            console.print(f"[green]✅ Processo '{removed}' removido com sucesso![/green]")
            return
        else:
            console.print("[red]❌ ID inválido.[/red]")
            raise typer.Exit(1)
    except ValueError:
        pass
    
    # Tenta remover pelo nome
    if nome in processes:
        processes.remove(nome)
        save_config(config)
        console.print(f"[green]✅ Processo '{nome}' removido com sucesso![/green]")
    else:
        console.print(f"[red]❌ Processo '{nome}' não encontrado.[/red]")
        raise typer.Exit(1)


@app.command("edit", help="✏️  Edita o nome de um processo existente")
def edit_process(
    antigo: str = typer.Argument(None, help="Nome ou ID do processo a editar"),
    novo: str = typer.Argument(None, help="Novo nome do processo")
):
    config = load_config()
    processes = config.get("processes", [])
    
    if not processes:
        console.print("[yellow]Nenhum processo para editar.[/yellow]")
        raise typer.Exit(1)
    
    if antigo is None:
        list_processes()
        antigo = Prompt.ask("\n[cyan]Nome ou ID do processo a editar[/cyan]")
    
    # Encontra o índice do processo
    idx = None
    try:
        idx = int(antigo) - 1
        if not (0 <= idx < len(processes)):
            console.print("[red]❌ ID inválido.[/red]")
            raise typer.Exit(1)
    except ValueError:
        if antigo in processes:
            idx = processes.index(antigo)
        else:
            console.print(f"[red]❌ Processo '{antigo}' não encontrado.[/red]")
            raise typer.Exit(1)
    
    if novo is None:
        novo = Prompt.ask("[cyan]Novo nome do processo[/cyan]", default=processes[idx])
    
    if not novo.strip():
        console.print("[red]❌ Nome do processo não pode ser vazio.[/red]")
        raise typer.Exit(1)
    
    if novo in processes and novo != processes[idx]:
        console.print(f"[yellow]⚠️ Processo '{novo}' já está na lista.[/yellow]")
        raise typer.Exit(1)
    
    old_name = processes[idx]
    processes[idx] = novo
    save_config(config)
    console.print(f"[green]✅ Processo '{old_name}' alterado para '{novo}'![/green]")


@app.command("interval", help="⏱️  Define o intervalo de verificação (em segundos)")
def set_interval(segundos: int = typer.Argument(None, help="Intervalo em segundos")):
    config = load_config()
    
    if segundos is None:
        segundos = int(Prompt.ask(
            "[cyan]Intervalo de verificação (segundos)[/cyan]",
            default=str(config.get("poll_interval", 5))
        ))
    
    if segundos < 1:
        console.print("[red]❌ Intervalo deve ser maior que 0.[/red]")
        raise typer.Exit(1)
    
    config["poll_interval"] = segundos
    save_config(config)
    console.print(f"[green]✅ Intervalo definido para {segundos} segundos![/green]")


@app.command("clear", help="🗑️  Remove todos os processos da lista")
def clear_processes():
    config = load_config()
    
    if not config.get("processes"):
        console.print("[yellow]Lista já está vazia.[/yellow]")
        return
    
    if Confirm.ask("[yellow]Tem certeza que deseja remover todos os processos?[/yellow]"):
        config["processes"] = []
        save_config(config)
        console.print("[green]✅ Todos os processos foram removidos![/green]")
    else:
        console.print("[dim]Operação cancelada.[/dim]")


@app.command("start", help="🚀 Inicia o monitoramento do FortScript")
def start_monitoring():
    """Inicia o FortScript executando o main.py."""
    start_bat = PROJECT_DIR / "start.bat"
    
    if not start_bat.exists():
        console.print("[red]❌ Arquivo start.bat não encontrado.[/red]")
        raise typer.Exit(1)
    
    is_running, processes = is_fortscript_running()
    if is_running:
        console.print("[yellow]⚠️ FortScript já está em execução![/yellow]")
        for proc in processes:
            console.print(f"[dim]  PID: {proc.pid}[/dim]")
        console.print("[dim]Use 'fort stop' para parar ou 'fort restart' para reiniciar.[/dim]")
        raise typer.Exit(1)
    
    console.print("[cyan]🚀 Iniciando FortScript...[/cyan]")
    subprocess.Popen(str(start_bat), shell=True, cwd=str(PROJECT_DIR))
    console.print("[green]✅ FortScript iniciado em uma nova janela![/green]")


@app.command("stop", help="⏹️  Para o FortScript")
def stop_monitoring():
    """Para todas as instâncias do FortScript."""
    is_running, processes = is_fortscript_running()
    
    if not is_running:
        console.print("[yellow]FortScript não está em execução.[/yellow]")
        return
    
    console.print(f"[cyan]Parando {len(processes)} instância(s) do FortScript...[/cyan]")
    
    for proc in processes:
        try:
            # Mata processos filhos primeiro
            for child in proc.children(recursive=True):
                child.kill()
            proc.kill()
            console.print(f"[green]✅ Processo {proc.pid} encerrado.[/green]")
        except psutil.NoSuchProcess:
            pass
        except psutil.AccessDenied:
            console.print(f"[red]❌ Sem permissão para encerrar processo {proc.pid}.[/red]")
    
    console.print("[green]✅ FortScript parado![/green]")


@app.command("restart", help="🔄 Reinicia o FortScript")
def restart_monitoring():
    """Para e inicia o FortScript novamente."""
    is_running, _ = is_fortscript_running()
    
    if is_running:
        console.print("[cyan]Parando FortScript...[/cyan]")
        stop_monitoring()
        import time
        time.sleep(1)
    
    start_monitoring()


@app.command("status", help="📊 Mostra o status do FortScript")
def status():
    """Mostra se o FortScript está em execução."""
    is_running, processes = is_fortscript_running()
    
    if is_running:
        console.print(Panel(
            f"[green]● FortScript está em execução[/green]\n"
            f"[dim]Instâncias: {len(processes)}[/dim]",
            title="Status"
        ))
        for proc in processes:
            console.print(f"[dim]  PID: {proc.pid}[/dim]")
    else:
        console.print(Panel(
            "[red]● FortScript não está em execução[/red]",
            title="Status"
        ))


if __name__ == "__main__":
    app()
