#!/usr/bin/env python3
import os
import time
import requests
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from typing import List, Optional
from pydantic import BaseModel, Field

# Terminal setup for Windows UTF-8
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.live import Live

# Local imports
from database import Database
from engine import calcular_score, PATRONES_DOLOR
from models import Oportunidad

# --- CONFIGURATION ---
console = Console()
db = Database()

# --- LOGIC --- (calcular_score importado desde engine.py — fuente unica de verdad)

def fetch_reddit_rss(subreddit: str) -> List[Oportunidad]:
    # HACK ESTRATÉGICO EP01: En lugar de /new.rss (basura sin validar)
    # usamos /top.rss?t=week para asegurar tracción orgánica de la comunidad.
    url = f"https://www.reddit.com/r/{subreddit}/top.rss?t=week"
    headers = {"User-Agent": "CazadorLite/1.2 (Spec-Driven Tool)"}
    
    try:
        r = requests.get(url, headers=headers, timeout=15)
        
        # --- MANEJO PROFESIONAL DE 429 (Rate Limit) ---
        if r.status_code == 429:
            console.print(Panel(
                f"[bold yellow]⚠️ RATE LIMIT DETECTADO (429)[/]\n"
                f"Reddit nos pide enfriar motores. Entrando en modo sigilo por 60s...",
                title="Pausa de Seguridad",
                border_style="yellow"
            ))
            time.sleep(60)
            return []
            
        if r.status_code != 200:
            return []

        root = ET.fromstring(r.content)
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        resultados = []
        
        for entry in root.findall("atom:entry", ns)[:10]:
            title_node = entry.find("atom:title", ns)
            if title_node is None or title_node.text is None:
                continue
            titulo = title_node.text
            enlace = entry.find("atom:link", ns).get("href")
            content = entry.find("atom:content", ns)
            dolor_snippet = content.text[:200] if (content is not None and content.text is not None) else ""
            
            # El score se calcula con datos crudos ANTES de construir el modelo.
            # El modelo recibe datos ya validados — el contrato se respeta desde el origen.
            score = calcular_score(titulo=titulo, dolor=dolor_snippet)
            
            op = Oportunidad(
                fuente=f"r/{subreddit}",
                titulo=titulo,
                enlace=enlace,
                dolor=dolor_snippet,
                score_gap=score
            )

            if op.score_gap > 0:
                resultados.append(op)
                db.guardar_oportunidad(op)
                
        return resultados

    except Exception as e:
        console.print(f"[dim red]   ! Error en r/{subreddit}: {e}[/]")
        return []

def render_ui():
    recent = db.obtener_mejores(10)
    if not recent:
        return Panel("[yellow]Buscando señales de dolor en la red...[/]", border_style="dim")
        
    table = Table(expand=True, border_style="red", row_styles=["none", "dim"])
    table.add_column("Score", justify="right", style="bold yellow", width=8)
    table.add_column("Comunidad", style="magenta", width=15)
    table.add_column("Detección de Dolor (Nicho)", style="white", ratio=1)
    table.add_column("Vínculo (Fuente)", style="cyan", ratio=2, no_wrap=False, overflow="fold")
    
    for row in recent:
        table.add_row(
            f"{row['score_gap']:.1f}",
            row['fuente'],
            row['titulo'][:70] + "...",
            row[ 'enlace' ]
        )
    return table

if __name__ == "__main__":
    console.clear()
    console.print(Panel.fit(
        "[bold red]CAZADOR CLI[/bold red] | [bold white]Engine v1.2[/bold white]\n"
        "[dim]Spec-Driven Development / Zero-Quota Mode[/dim]",
        border_style="red"
    ))
    
    subreddits = ["learnprogramming", "webdev", "freelance", "python", "saas"]
    
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        for sub in subreddits:
            progress.add_task(description=f"[cyan]Escaneando r/{sub}...", total=None)
            fetch_reddit_rss(sub)
            time.sleep(2) # Respeto al crawler

    console.print(render_ui())
    
    # --- SUMARIO DE INVESTIGACIÓN (Para copiar links fácilmente) ---
    recent = db.obtener_mejores(10)
    if recent:
        console.print(f"\n[bold cyan]🔗 SUMARIO DE INVESTIGACIÓN PROFUNDA:[/]")
        for i, row in enumerate(recent, 1):
            console.print(f"  {i}. [white]{row['enlace']}[/]")
            
    console.print(f"\n[dim]Resultados persistidos en [white]{db.db_path}[/]. Proceso finalizado.[/]")
