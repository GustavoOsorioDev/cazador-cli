# ROADMAP — Cazador Lite (Zero-Quota MVP)

Este documento traza la evolución de la herramienta pública para la comunidad de @GustavoOsorioDev.

## 🚀 Próximos Pasos (V1.3 - V1.5)

### 1. Conector HackerNews (Stealth Mode)
- Implementar parsing de la API de Firebase/HackerNews para capturar "Show HN" y detectar puntos de dolor en herramientas recién lanzadas.
- **Autoridad:** Muestra que el código es modular y fácil de extender a otras fuentes.

### 2. Filtro Local con LLM (Ollama/Llama3)
- Integrar una fase de "Validación de Calidad" usando un LLM local.
- El bot no solo contará palabras, sino que razonará si el problema es "un bug trivial" o "una oportunidad de negocio real".
- **Hook de Video:** "Cómo hacer que tu terminal piense por ti sin pagar a OpenAI".

### 3. Exportación a Notion/Obsidian
- Crear un comando `--export notion` para enviar los nichos encontrados directamente a un dashboard de investigación.
- Ideal para "Constructores Solos" que quieren organizar sus ideas de SaaS.

### 4. Modo "Deep Hunt" (Stealth Browsing)
- Simulación de navegación humana para entrar en foros con protecciones anti-bot más estrictas (sin usar Selenium, solo headers y tiempos de espera inteligentes).

---
"Construyendo en público, un commit a la vez."
