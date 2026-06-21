# 📡 Cazador CLI (La Arquitectura Anti-Slop)
> "Ingeniería real. Sin vibes."

Este repositorio acompaña al **Episodio 1** del canal de YouTube. No es solo un bot de rastreo para foros; es **una demostración de Spec-Driven Development (SDD)**. 

Si programas asistido por IA, sabes que el mayor riesgo hoy es el "vibe coding": código fluido pero frágil, que explota silenciosamente en producción. Este repositorio demuestra cómo un **Firewall de Contratos (Pydantic)** detiene las alucinaciones costosas de cualquier LLM *antes* de tocar la red.

---

## ⚡ Modos de Operación

Cazador CLI opera bajo un modelo híbrido para maximizar la eficiencia y el ahorro de cómputo:

### 1. Modo Local (Zero-Quota / Gratis)
Utiliza **Sigilo RSS** para eludir el error `403` de Reddit sin necesidad de tokens de API.
*   **Filtros:** Patrones de frustración sintáctica (`nightmare`, `struggling`, `roto`).
*   **Ideal para:** Exploración rápida y descubrimiento de semillas.
*   **Costo:** $0.00 (Offline/Local).

### 2. Modo IA (Evolutivo)
Desbloquea el verdadero poder del motor inyectando inteligencia de clasificación. Requiere una **API Key** de la Red Central.
*   **Clasificación Cuantitativa:** Scoring de nichos basado en volumen y competencia.
*   **Cómputo en la Nube:** Procesa las señales crudas a través del `cazador-engine` privado.
*   **Gemini Sync:** Generación automática de guiones y planes de producto.

---

## 🚀 Despliegue Rápido

```bash
# 1. Clonar arquitectura
git clone https://github.com/GustavoOsorioDev/cazador-cli.git
cd cazador-cli

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar radar
python src/main.py
```

## 🔐 Obtener API Key (500 Créditos Gratis)

Para activar el **Modo IA**, sigue estos pasos:
1. Regístrate en [hq.gustavoosorio.dev](https://hq.gustavoosorio.dev) mediante **GitHub OAuth**.
2. Copia tu `CAZADOR_API_KEY` desde el dashboard.
3. Crea un archivo `.env` en la raíz de este proyecto y pega tu llave:
   ```env
   CAZADOR_API_KEY=tu_llave_aqui
   ```

## 🛠️ Especificaciones Técnicas (CSDD)

Este proyecto no es un script de fin de semana; es una pieza de ingeniería modular:
*   **Contratos Inmutables:** Información tipada estrictamente con `Pydantic`.
*   **UI Premium:** Interfaz de terminal de alta fidelidad con la librería `Rich`.
*   **Transparencia:** Consulta la carpeta [`.specs/`](./.specs/) para ver el Spec-Driven Development completo.

---

## 💎 Infraestructura Recomendada (Deploy & Escala)

Si planeas poner bots impulsados por IA en producción (como este), el hardware y el entorno importan tanto como el código. Esta es la pila tecnológica (CPA Links) que usamos para garantizar que Cazador opere sin fugas de presupuesto:

*   **⚡ Entorno de Código:** [Cursor IDE (Pruébalo gratis)]() — Escribe los contratos Pydantic tú mismo y deja que la IA haga la "carpintería" mundana.
*   **☁️ Servidor VPS:** [DigitalOcean ($200 Crédito)]() / [Hetzner]() — Despliega los scrapers en Docker. Evita que un error 429 queme la IP de tu casa.
*   **💾 Base de Datos:** [Supabase]() — Conecta PostgreSQL 1:1 con los esquemas Pydantic del Bot, garantizando Full-Stack Type Safety.

---
**Build in Public** • Ingeniería real por [@GustavoOsorioDev](https://youtube.com/@GustavoOsorioDev)
