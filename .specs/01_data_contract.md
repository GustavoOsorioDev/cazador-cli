# ESPECIFICACIÓN: 01 — CONTRATO DE DATOS (Cazador Lite)

## 1. PROPÓSITO
Definir la estructura inmutable de los datos recolectados para asegurar que cualquier
integración futura (IA, DB, API) respete los tipos y campos obligatorios.

## 2. ESQUEMA (Dato Único — clase `Oportunidad`)

| Campo | Tipo | Obligatorio | Descripción |
| :--- | :--- | :---: | :--- |
| `fuente` | `str` | ✅ | Identificador del origen (ej. `r/webdev`) |
| `titulo` | `str` | ✅ | Título original del post |
| `comentarios` | `int` | — | Contador de comentarios (default: 0) |
| `votos` | `int` | — | Votos de la comunidad (default: 0) |
| `enlace` | `str` | ✅ | URL absoluta al post |
| `dolor` | `str \| None` | — | Snippet del contenido del post (max 200 chars). **Optional**: el RSS de Reddit no siempre entrega el cuerpo del post sin autenticación OAuth. |
| `score_gap` | `float ≥ 0` | — | Score de oportunidad calculado. **Siempre ≥ 0** (validado por Pydantic). |
| `fecha` | `str` | ✅ | Timestamp ISO 8601 UTC (auto-generado) |

## 3. LÓGICA DE NEGOCIO (Scoring)

La función `calcular_score()` es **pura**: recibe datos crudos, no el modelo.
Esto la hace testeable de forma aislada y evita dependencias circulares.

### Modo con Engagement (API oficial, futuro):
```
base_score = (comentarios * 0.4) + (votos * 0.0009)
multiplier = 1.0 + (coincidencias_dolor * 0.5)
score = base_score * multiplier
```

### Modo RSS / Zero-Quota (activo en v1.2):
```
score = float(count(PATRONES_DOLOR in titulo + dolor))
```
> **Nota de arquitectura:** El RSS de Reddit no expone `comentarios` ni `votos` sin
> OAuth. En Zero-Quota Mode, el scoring es 100% semántico. El campo `score_gap` en
> la DB reflejará valores bajos (1–5) vs valores amplificados en Modo API.
> La estructura del contrato no cambia entre modos — solo el valor del campo.

## 4. RESTRICCIONES INMUTABLES
- `enlace` debe ser único en la base de datos (`UNIQUE` en SQLite).
- `score_gap` nunca puede ser negativo.
- `fecha` se genera en UTC automáticamente — nunca se pasa manualmente.

---
*Versión: 1.1.0 — Actualizado para reflejar dolor como Optional y ge=0 en score_gap*
