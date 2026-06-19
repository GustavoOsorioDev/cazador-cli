# 📡 Cazador CLI (v1.0)
> "Ingeniería real. Sin vibes."

Cazador CLI es un bot de rastreo local diseñado para identificar **anomalías de frustración** en foros masivos. En lugar de especular sobre qué construir, el motor analiza patrones lingüísticos de "dolor" real que usuarios finales están experimentando *ahora mismo*.

Este es el **Lead Magnet oficial** de la arquitectura [@GustavoOsorioDev](https://github.com/GustavoOsorioDev).

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
1. Regístrate en [gustavo-hq.com](https://gustavo-hq.com) mediante **GitHub OAuth**.
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
**Build in Public** • Ingeniería real por [@GustavoOsorioDev](https://youtube.com/@GustavoOsorioDev)

