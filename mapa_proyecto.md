# Mapa del Proyecto: cazador-cli

Este documento actúa como la fuente de verdad arquitectónica (Source of Truth) para el ecosistema **cazador-cli** (Detector de Dolor de Usuario / Zero-Quota MVP). Define la estructura del repositorio y el propósito central de cada módulo clave dentro del contexto "Build in Public".

## Estructura de Directorios

```text
cazador-cli/
├── .specs/                  # Spec-Driven Development (Contratos y Diseño Técnico)
│   └── 01_data_contract.md  # Contrato inmutable (Oportunidad) y lógica de scoring
├── docs/                    # Documentación Técnica Auxiliar
│   └── diagrama_flujo.md    # Flujo algorítmico en Mermaid.js del rastreador Stealth
├── db/                      # Persistencia Local
│   └── cazador.db           # Base de Datos SQLite (Resultados persistidos)
├── src/                     # Código Fuente y Lógica de Negocio
│   ├── main.py              # Motor principal (Formal Entry Point)
│   └── database.py          # Adaptador de persistencia SQLite
├── .env.example             # Plantilla de variables de entorno de referencia
├── README.md                # Presentación general del proyecto y quick-start
└── requirements.txt         # Dependencias Python (pydantic, requests, rich)
```

## Componentes Core del Ecosistema

### 1. Motor de Extracción y Análisis (`src/main.py`)
- **Método de Captura:** Utiliza *Stealth RSS parsing* para consumir las actualizaciones en tiempo real esquivando bloqueos convencionales de scraping (e.g., errores HTTP 403).
- **Detección de Interés:** Utiliza análisis semántico crudo comprobando contra `PATRONES_DOLOR` para rescatar solo los hilos que manifiestan frustración auténtica o problemas persistentes.
- **Renderizado UI:** Muestra al usuario final los resultados ordenados vía terminal usando la librería *Rich* para visualización elegante y clara mediante tablas de diagnóstico.

### 2. Estándares y Contratos de Datos (`.specs/01_data_contract.md`)
- Exige que cualquier integración actual o futura se adhiera al contrato base estructural de los items (incluyendo `fuente`, `titulo`, `score_gap`, entre otros), consolidando la escalabilidad del bot hacia BBDD, APIs, o flujos LLM.

### 3. Diagramación de Comportamiento (`docs/diagrama_flujo.md`)
- Ofrece transparencia visual del ciclo de vida del dato desde la invocación del subreddit hasta el ordenamiento matemático en memoria de las variables analizadas.

## Ciclo de Ejecución

Para iniciar una exploración, el entorno debe contener las dependencias listadas en `requirements.txt`. El script se ejecuta independientemente como:

```bash
python src/main.py
```

*(Nota: Se recomienda usar un entorno virtual como `venv` o `conda` y Python 3.10+)*.

## Filosofía "Build in Public"

Este MVP Zero-Quota expone abiertamente la metodología **"Spec-Driven Development"** a la comunidad. Prioriza un contrato de datos estricto (`.specs/`) antes del código, demostrando orden arquitectónico, autoridad técnica y evitando deudas técnicas prematuras. Constituye un eslabón primario para el ecosistema mayor.
