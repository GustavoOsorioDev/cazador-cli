"""
cli.py — Entrypoint Typer Formal
Fuente de verdad: .specs/feature_scan.md → T3
ADR de referencia: .specs/adr_001_stack_cazador_cli.md

Responsabilidad única: Interfaz de usuario (CLI).
- Recibe input del usuario.
- Delega validación al contrato (models.py → ScanTarget).
- Delega procesamiento al motor (engine.py → scan_url).
- Presenta el resultado. No contiene lógica de negocio.
"""

import sys
import typer

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from models import ScanTarget
from engine import scan_url

# ─── Windows UTF-8 fix (consistente con main.py) ────────────────────────────
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


app = typer.Typer(
    name="cazador",
    help="[bold red]CAZADOR CLI[/] — Spec-Driven Intelligence Tool. 'Ingeniería real, sin vibes.'",
    rich_markup_mode="rich",
    no_args_is_help=True,
)

console = Console()


# ─── COMANDO: scan ───────────────────────────────────────────────────────────
# Spec ref: feature_scan.md § 5 T3 y § 6 Criterios de Verificación

@app.command()
def scan(
    query: str = typer.Argument(
        ...,
        help="Patrón de búsqueda (string literal o regex básica)",
    ),
    target: str = typer.Option(
        ...,
        "--target",
        "-t",
        help="URL del objetivo a escanear",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        "-j",
        help="Emitir resultado como JSON puro (para pipelines)",
    ),
) -> None:
    """
    Escanea un [cyan]target[/] URL buscando el [yellow]patrón[/] especificado.

    \b
    Ejemplos:
      cazador scan "API_KEY" --target "http://localhost:8000/config"
      cazador scan "error" --target "https://example.com/logs" --json
    """
    # ── PASO 1: Validación del contrato (el modelo es la primera línea de defensa)
    try:
        scan_target = ScanTarget(url=target, query=query)
    except Exception as e:
        # ValidationError de Pydantic → el contrato rechaza el input
        console.print(
            Panel(
                f"[bold red]🚫 OPERACIÓN BLOQUEADA[/]\n\n{e}",
                title="Firewall de Contratos",
                border_style="red",
            )
        )
        raise typer.Exit(code=1)

    # ── PASO 2: Feedback visual pre-escaneo
    console.print(
        f"\n[dim]▶[/] Escaneando [white]{scan_target.url}[/] "
        f"en busca de [yellow]'{scan_target.query}'[/]...\n"
    )

    # ── PASO 3: Delegación al motor puro
    result = scan_url(scan_target)

    # ── PASO 4: Presentación del resultado
    if json_output:
        # Modo pipeline: JSON puro a STDOUT (sin decoración Rich)
        typer.echo(result.model_dump_json(indent=2))
        return

    if result.found:
        table = Table(
            title=f"Finding — {int(result.score)} coincidencias",
            border_style="green",
            show_header=True,
        )
        table.add_column("Campo", style="cyan", width=14)
        table.add_column("Valor", style="white")
        table.add_row("Target", result.target)
        table.add_row("Query", result.query)
        table.add_row("Score", f"[bold green]{result.score:.0f} coincidencias[/]")
        table.add_row("Timestamp", result.timestamp)
        table.add_row("Raw (500c)", result.raw_data[:120] + "..." if len(result.raw_data) > 120 else result.raw_data)
        console.print(table)
        console.print(f"\n[bold green]✅ PATRÓN ENCONTRADO[/]\n")
    else:
        console.print(
            Panel(
                f"[dim]Sin coincidencias para '[yellow]{result.query}[/]' en:\n{result.target}[/]\n\n"
                f"[dim italic]{result.raw_data if result.raw_data else 'Respuesta vacía o target inalcanzable.'}[/]",
                title="Resultado del Escaneo",
                border_style="dim",
            )
        )
        console.print(f"[dim]Score: 0.0 | found: False[/]\n")


# ─── ENTRYPOINT ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app()
