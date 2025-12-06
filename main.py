"""
FortScript - Gerenciador inteligente de scripts
Pausa automaticamente scripts quando processos pesados estão em execução.
"""

import json
import subprocess
import time
import signal
import sys
from pathlib import Path
from typing import Optional

import psutil
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.layout import Layout

console = Console()
CONFIG_FILE = Path(__file__).parent / "config.json"
SCRIPTS_DIR = Path(__file__).parent / "scripts"

# Armazena os processos dos scripts em execução
running_scripts: dict[str, subprocess.Popen] = {}
scripts_paused = False
should_exit = False


def load_config() -> dict:
    """Carrega a configuração do arquivo JSON. Cria se não existir."""
    default_config = {"processes": [], "poll_interval": 5}
    
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    
    # Cria o arquivo de configuração padrão
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(default_config, f, indent=4, ensure_ascii=False)
    
    return default_config


def get_scripts() -> list[Path]:
    """Retorna todos os scripts suportados na pasta scripts/."""
    if not SCRIPTS_DIR.exists():
        SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
        return []
    
    supported_extensions = {".bat", ".py", ".exe"}
    scripts = []
    
    for file in SCRIPTS_DIR.iterdir():
        if file.is_file() and file.suffix.lower() in supported_extensions:
            scripts.append(file)
    
    return sorted(scripts)


def start_script(script_path: Path) -> Optional[subprocess.Popen]:
    """Inicia um script e retorna o processo."""
    try:
        if script_path.suffix.lower() == ".py":
            # Scripts Python são executados com uv run python
            process = subprocess.Popen(
                ["uv", "run", "python", str(script_path)],
                cwd=str(script_path.parent),
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
            )
        elif script_path.suffix.lower() == ".bat":
            # Arquivos batch
            process = subprocess.Popen(
                ["cmd", "/c", str(script_path)],
                cwd=str(script_path.parent),
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
            )
        elif script_path.suffix.lower() == ".exe":
            # Executáveis
            process = subprocess.Popen(
                [str(script_path)],
                cwd=str(script_path.parent),
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
            )
        else:
            return None
        
        return process
    except Exception as e:
        console.print(f"[red]❌ Erro ao iniciar {script_path.name}: {e}[/red]")
        return None


def start_all_scripts() -> None:
    """Inicia todos os scripts da pasta scripts/."""
    global running_scripts, scripts_paused
    
    scripts = get_scripts()
    
    if not scripts:
        console.print("[yellow]⚠️ Nenhum script encontrado na pasta scripts/[/yellow]")
        return
    
    console.print(f"\n[cyan]▶️ Iniciando {len(scripts)} script(s)...[/cyan]")
    
    for script in scripts:
        if script.name not in running_scripts or running_scripts[script.name].poll() is not None:
            process = start_script(script)
            if process:
                running_scripts[script.name] = process
                console.print(f"  [green]✓[/green] {script.name} [dim](PID: {process.pid})[/dim]")
    
    scripts_paused = False


def stop_all_scripts() -> None:
    """Para todos os scripts em execução."""
    global running_scripts, scripts_paused
    
    if not running_scripts:
        return
    
    console.print(f"\n[yellow]⏸️ Pausando {len(running_scripts)} script(s)...[/yellow]")
    
    for name, process in list(running_scripts.items()):
        try:
            if process.poll() is None:  # Processo ainda está rodando
                # Tenta encerrar processos filhos primeiro
                try:
                    parent = psutil.Process(process.pid)
                    for child in parent.children(recursive=True):
                        child.kill()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
                
                process.kill()
                process.wait(timeout=5)
                console.print(f"  [yellow]⏸[/yellow] {name}")
        except Exception as e:
            console.print(f"  [red]❌ Erro ao parar {name}: {e}[/red]")
    
    running_scripts.clear()
    scripts_paused = True


def is_monitored_process_running(processes_to_monitor: list[str]) -> tuple[bool, list[str]]:
    """Verifica se algum processo monitorado está em execução."""
    found_processes = []
    
    for proc in psutil.process_iter(['name']):
        try:
            proc_name = proc.info.get('name', '')
            if proc_name and proc_name.lower() in [p.lower() for p in processes_to_monitor]:
                found_processes.append(proc_name)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    return len(found_processes) > 0, list(set(found_processes))


def display_status(config: dict, detected_processes: list[str]) -> None:
    """Exibe o status atual do monitoramento."""
    processes = config.get("processes", [])
    interval = config.get("poll_interval", 5)
    
    # Status geral
    if scripts_paused:
        status_text = "[yellow]⏸️ PAUSADO[/yellow]"
        if detected_processes:
            status_text += f" - Detectado: {', '.join(detected_processes)}"
    else:
        status_text = "[green]▶️ EXECUTANDO[/green]"
    
    console.print(f"\n[bold]Status:[/bold] {status_text}")
    console.print(f"[dim]Próxima verificação em {interval} segundos...[/dim]")


def signal_handler(signum, frame):
    """Handler para sinais de interrupção."""
    global should_exit
    should_exit = True
    console.print("\n[yellow]🛑 Encerrando FortScript...[/yellow]")
    stop_all_scripts()
    sys.exit(0)


def main():
    """Loop principal de monitoramento."""
    global scripts_paused, should_exit
    
    # Registra handlers de sinal
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    console.print(Panel.fit(
        "[bold cyan]🎮 FortScript[/bold cyan]\n"
        "[dim]Gerenciador inteligente de scripts[/dim]",
        border_style="cyan"
    ))
    
    config = load_config()
    processes_to_monitor = config.get("processes", [])
    poll_interval = config.get("poll_interval", 5)
    
    if not processes_to_monitor:
        console.print("[yellow]⚠️ Nenhum processo configurado para monitorar.[/yellow]")
        console.print("[dim]Use 'fort add <processo>' para adicionar processos.[/dim]")
    else:
        console.print(f"\n[bold]📋 Monitorando {len(processes_to_monitor)} processo(s):[/bold]")
        for proc in processes_to_monitor:
            console.print(f"  [dim]•[/dim] {proc}")
    
    scripts = get_scripts()
    if scripts:
        console.print(f"\n[bold]📁 Scripts encontrados ({len(scripts)}):[/bold]")
        for script in scripts:
            console.print(f"  [dim]•[/dim] {script.name}")
    else:
        console.print("\n[yellow]⚠️ Nenhum script encontrado na pasta scripts/[/yellow]")
        console.print("[dim]Adicione arquivos .bat, .py ou .exe na pasta scripts/[/dim]")
    
    console.print(f"\n[bold]⏱️ Intervalo de verificação:[/bold] {poll_interval} segundos")
    console.print("\n" + "─" * 50)
    console.print("[dim]Pressione Ctrl+C para encerrar[/dim]")
    console.print("─" * 50)
    
    # Verifica se já há processo monitorado em execução antes de iniciar
    is_running, detected = is_monitored_process_running(processes_to_monitor)
    
    if is_running:
        console.print(f"\n[yellow]⚠️ Processo detectado: {', '.join(detected)}[/yellow]")
        console.print("[dim]Scripts não serão iniciados enquanto o processo estiver ativo.[/dim]")
        scripts_paused = True
    else:
        # Inicia todos os scripts
        start_all_scripts()
    
    # Loop principal de monitoramento
    while not should_exit:
        try:
            # Recarrega configuração para pegar alterações
            config = load_config()
            processes_to_monitor = config.get("processes", [])
            poll_interval = config.get("poll_interval", 5)
            
            is_running, detected = is_monitored_process_running(processes_to_monitor)
            
            if is_running and not scripts_paused:
                # Processo detectado - pausar scripts
                console.print(f"\n[bold yellow]🎮 Processo detectado: {', '.join(detected)}[/bold yellow]")
                stop_all_scripts()
            elif not is_running and scripts_paused:
                # Processo encerrado - reiniciar scripts
                console.print("\n[bold green]✅ Processo encerrado![/bold green]")
                start_all_scripts()
            
            # Verifica se algum script morreu e precisa ser reiniciado
            if not scripts_paused:
                for name, process in list(running_scripts.items()):
                    if process.poll() is not None:
                        # Script morreu, remove da lista
                        console.print(f"[yellow]⚠️ Script {name} encerrou (código: {process.returncode})[/yellow]")
                        del running_scripts[name]
            
            time.sleep(poll_interval)
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            console.print(f"[red]❌ Erro no loop principal: {e}[/red]")
            time.sleep(poll_interval)
    
    # Cleanup
    stop_all_scripts()
    console.print("[green]✅ FortScript encerrado.[/green]")


if __name__ == "__main__":
    main()
