"""
engine.py — Motor de Procesamiento Puro
Fuente de verdad: .specs/feature_scan.md → T2
ADR de referencia: .specs/adr_001_stack_cazador_cli.md

REGLA (Manifiesto Anti-Slop): Funciones puras. Sin side-effects de UI.
- Reciben primitivas o modelos validados.
- Retornan resultados predecibles.
- NO importan Console, Panel ni ningún elemento de presentación.
"""

import re
import requests
from typing import Optional

from models import ScanTarget, Finding, Oportunidad


# ─── PATRONES DE DOLOR (compartidos con main.py por compatibilidad) ──────────
PATRONES_DOLOR = [
    "struggle", "struggling", "hate", "sucks", "broken", "nightmare",
    "tired of", "how do you deal", "why is it so hard to", "mess",
    "spaghetti", "worst", "help", "giving up", "painful", "frustrated"
]


# ─── FUNCIÓN PURA: calcular_score ───────────────────────────────────────────
# Extraída de main.py L46-68. Contrato: primitivas → float. Sin side-effects.

def calcular_score(
    titulo: str,
    dolor: Optional[str] = None,
    comentarios: int = 0,
    votos: int = 0,
) -> float:
    """
    Función pura: recibe datos crudos, devuelve un float.
    No depende del modelo Oportunidad — testeable de forma aislada.

    Lógica según Contrato 01:
    - Con engagement real: (comentarios * 0.4) + (votos * 0.0009), amplificado por patrones.
    - Modo RSS (engagement = 0): score semántico puro por conteo de PATRONES_DOLOR.
      Razón: el RSS de Reddit no expone comentarios/votos sin OAuth.
    """
    base_score = (comentarios * 0.4) + (votos * 0.0009)
    coincidencias = sum(
        1 for patron in PATRONES_DOLOR
        if patron in (titulo + " " + (dolor or "")).lower()
    )

    if base_score == 0:
        return round(float(coincidencias), 2)

    multiplier = 1.0 + (coincidencias * 0.5)
    return round(base_score * multiplier, 2)


# ─── FUNCIÓN PURA: scan_url ──────────────────────────────────────────────────
# Implementación del T2 de feature_scan.md — motor del comando `scan`
# Recibe: ScanTarget (contrato validado). Retorna: Finding (contrato inmutable).

def scan_url(target: ScanTarget) -> Finding:
    """
    Función pura: recibe un ScanTarget ya validado, retorna un Finding.
    No lanza excepciones hacia el exterior — los errores se encapsulan en Finding.
    El caller (cli.py) decide cómo presentar el resultado al usuario.
    """
    headers = {"User-Agent": "CazadorLite/1.2 (Spec-Driven Tool)"}

    try:
        response = requests.get(target.url, headers=headers, timeout=10)
        content = response.text

        # Búsqueda: string literal + regex básica (spec § 2 IN-SCOPE)
        pattern = re.compile(re.escape(target.query), re.IGNORECASE)
        matches = pattern.findall(content)

        score = float(len(matches))
        # Captura contexto alrededor del primer match (máx 500 chars)
        raw_data = content[:500] if matches else ""

        # Contrato Inmutable: score se calcula ANTES de instanciar Finding
        return Finding(
            target=target.url,
            query=target.query,
            raw_data=raw_data,
            score=score,
            found=len(matches) > 0,
        )

    except requests.exceptions.Timeout:
        return Finding(
            target=target.url,
            query=target.query,
            raw_data="Error: Timeout — el target no respondió en 10s",
            score=0.0,
            found=False,
        )
    except requests.exceptions.RequestException as e:
        return Finding(
            target=target.url,
            query=target.query,
            raw_data=f"Error de red: {type(e).__name__}",
            score=0.0,
            found=False,
        )
