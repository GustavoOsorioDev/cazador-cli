# Diagrama de Flujo: cazador-cli (Engine v1.2)

Este documento detalla el comportamiento algorítmico y lógico del script principal `src/main.py`, responsable de la técnica **Stealth RSS**, la detección semántica de **"Dolor de Usuario"** (Zero-Quota Mode) y la persistencia local vía SQLite.

## Algoritmo de Extracción y Análisis

```mermaid
flowchart TD
    A([Inicio: Ejecución de src/main.py]) --> B[Inicializar Database en\nraiz/db/cazador.db]
    B --> C[Definir array de Subreddits:\nlearnprogramming, webdev, freelance, python, saas]
    
    C --> D{¿Quedan subreddits\npor analizar?}
    
    %% Loop principal por Subreddit
    D -- Sí --> E[Seleccionar Subreddit]
    E --> F[Invocación HTTP:\nfetch_reddit_rss]
    F --> G{¿Código 200 OK?}
    
    G -- No --> H{¿Error 429?}
    H -- Sí --> H1[Pausa de seguridad 60s]
    H -- No --> H2[Skip silencioso]
    H1 --> D
    H2 --> I
    
    %% Flujo de éxito para el feed
    G -- Sí --> J[Parsear XML en árbol de nodos]
    J --> K[Obtener top entradas\natom:entry]
    
    K --> L{¿Quedan\nentradas por\nprocesar?}
    
    %% Loop interno por Entrada
    L -- Sí --> M[Lectura de Título, Enlace y Contenido]
    M --> N[Llamar calcular_score\nFunción Pura]
    
    N --> O{¿Score > 0?}
    
    O -- Sí --> P[Construir objeto Oportunidad\nrespetando Contrato]
    P --> Q[db.guardar_oportunidad \nGuarda en SQLite]
    Q --> L
    
    O -- No --> L
    
    L -- No, fin de entradas --> I[Esperar 2 seg]
    I --> D
    
    %% Flujo de renderizado
    D -- No, fin lista --> U[Invocación render_ui]
    U --> V[db.obtener_recientes]
    V --> W{¿Hay registros?}
    
    W -- Sí --> X[Renderizar Tabla Rich y Sumario]
    W -- No --> Y[Mostrar mensaje de radar vacío]
    
    Y --> Z([Fin del Proceso])
    X --> X2[Imprimir Sumario de Links]
    X2 --> Z

    %% Estilos recomendados para el diagrama
    classDef init endObj fill:#f5f5f5,stroke:#333,stroke-width:2px;
    classDef logic fill:#e1f5fe,stroke:#03a9f4,stroke-width:2px;
    classDef data fill:#e8f5e9,stroke:#4caf50,stroke-width:2px;
    
    class A,Z init;
    class D,G,H,L,O,W logic;
    class B,P,Q,V,X data;
```

## Leyenda y Aspectos Técnicos
- **Stealth RSS:** El consumo de XML vía `top.rss?t=week` permite capturar data validada orgánicamente sin requerir credenciales de API (Zero-Quota).
- **Funciones Puras:** El core analítico (`calcular_score`) opera sin mutaciones laterales, asegurando previsibilidad.
- **Persistencia Local:** La capa `database.py` gestiona SQLite resolviendo la ruta con `abspath(__file__)` garantizando una ejecución inmune a diferencias de pathing (CWD).
- **Protección de API:** El factor de retraso artificial (`time.sleep`) en loops y la gestión activa de errores HTTP 429 evitan la asfixia proactiva del bot en entornos de red exigentes.
