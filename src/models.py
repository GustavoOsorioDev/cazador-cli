"""
models.py — Contratos Inmutables (CSDD)
Fuente de verdad: .specs/feature_scan.md → T1
ADR de referencia: .specs/adr_001_stack_cazador_cli.md

REGLA: Los modelos se instancian completos. No se mutan post-constructor.
       score = calcular(data); op = Modelo(score=score)  ← CORRECTO
       op = Modelo(); op.score = score                   ← SLOP, prohibido
"""

from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, Field, field_validator


# ─── CONTRATO: ScanTarget ───────────────────────────────────────────────────
# Spec ref: feature_scan.md § 2 (Límites de Alcance) y § 3 (Restricciones)

DOMINIOS_BLOQUEADOS = [".gov", ".mil"]
EXTENSIONES_BLOQUEADAS = [".exe", ".dll", ".bat", ".sh", ".msi"]


class ScanTarget(BaseModel):
    """Contrato de entrada del comando scan. Valida URL y patrón antes del procesamiento."""
    url: str
    query: str

    @field_validator("url")
    @classmethod
    def validar_url(cls, v: str) -> str:
        url_lower = v.lower()
        for dominio in DOMINIOS_BLOQUEADOS:
            if dominio in url_lower:
                raise ValueError(
                    f"[ETICA: BLOQUEADO] Dominio restringido detectado: '{dominio}'. "
                    f"Este escáner no opera sobre infraestructura gubernamental o militar."
                )
        for ext in EXTENSIONES_BLOQUEADAS:
            if url_lower.endswith(ext):
                raise ValueError(
                    f"[SEGURIDAD: BLOQUEADO] Extensión ejecutable detectada: '{ext}'. "
                    f"No se procesan archivos binarios."
                )
        return v


# ─── CONTRATO: Finding ──────────────────────────────────────────────────────
# Spec ref: feature_scan.md § 1 (Outcomes) — hallazgo normalizado e inmutable

class Finding(BaseModel):
    """Resultado inmutable de un escaneo. Nunca se muta post-instanciación."""
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    target: str
    query: str
    raw_data: str
    score: float = Field(ge=0.0, description="Número de coincidencias encontradas")
    found: bool


# ─── CONTRATO: Oportunidad ──────────────────────────────────────────────────
# Modelo heredado del motor RSS — se mantiene para compatibilidad con main.py
# Sync con: src/main.py L26-34 y .specs/01_data_contract.md

class Oportunidad(BaseModel):
    """Hallazgo del motor RSS de Reddit. Contrato binario con database.py."""
    fuente: str
    titulo: str
    comentarios: int = 0
    votos: int = 0
    enlace: str
    dolor: Optional[str] = None
    score_gap: float = Field(default=0.0, ge=0)
    fecha: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
