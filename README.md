# Cazador CLI: Encuentra qué construir buscando de qué se queja la gente

"Ingeniería real. Sin humo."

Este es un bot para encontrar ideas de apps y herramientas analizando de qué se queja la gente en Reddit. No usa APIs caras ni complejas; usa ingeniería directa (RSS) para extraer problemas reales que la gente quiere resolver YA.

Este repo es parte del **Build In Public** de [@GustavoOsorioDev](https://github.com/GustavoOsorioDev).

## 🚀 Pruébalo en 1 minuto

1. **Clona e instala:**
   ```bash
   git clone https://github.com/GustavoOsorioDev/cazador-cli.git
   cd cazador-cli
   pip install -r requirements.txt
   ```

2. **Enciende el radar:**
   ```bash
   python src/main.py
   ```

## 🧠 ¿Cómo funciona? (Sin tecnicismos raros)

Aquí no tiramos código a lo loco. El proyecto se basa en tres pilares:

1. **Datos bien estructurados**: Usamos `Pydantic` para que la información que recolectamos sea sólida y no se rompa al primer cambio.
2. **Modo Sigilo (Zero-Quota)**: Saltamos las restricciones típicas de scraping usando RSS. Es rápido, ético y no gasta cuotas de API.
3. **Detector de "Dolor"**: El bot no busca palabras clave genéricas. Busca frustración real (`odio`, `roto`, `ayuda`, `pesadilla`) para encontrar problemas reales que valga la pena solucionar.

Mira la carpeta [`.specs/`](./.specs/) si quieres ver los planos técnicos de cómo se armó esto.

---
**Build in Public** • Por [@GustavoOsorioDev](https://youtube.com/@GustavoOsorioDev)
