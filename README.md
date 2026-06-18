# Cazador CLI — Detector de "Dolor de Usuario"

"Ingeniería real. Sin vibes."

Este es un **bot cazador de nichos** de software y herramientas, diseñado bajo la metodología **Spec-Driven Development (SDD)** y con la filosofía **Zero-Quota**. En lugar de depender de APIs complejas y costosas, utiliza técnicas de ingeniería ("Stealth RSS") para extraer verdaderos "patrones de frustración" y validarlos en tiempo real.

Este repositorio forma parte de la serie documental **Build In Public** de [@GustavoOsorioDev](https://github.com/GustavoOsorioDev).

## 🚀 Inicio Rápido

1. **Clonar e instalar dependencias:**
   ```bash
   git clone https://github.com/GustavoOsorioDev/cazador-cli.git
   cd cazador-cli
   pip install -r requirements.txt
   ```

2. **Ejecutar el radar:**
   ```bash
   python src/main.py
   ```

## 🧠 Arquitectura y Metodología

El código no se escribe a ciegas. Este proyecto demuestra:

1. **Contratos de Datos Estrictos**: Se utiliza `Pydantic` para garantizar que la recolección de datos respete un contrato inmutable definido *antes* de programar.
2. **Stealth Mode (Zero-Quota)**: Bypass ético de restricciones de scraping utilizando estándares abiertos como RSS (XML), evitando consumos de cuota o bloqueos `403`.
3. **Escáner Semántico Crudo**: Filtrado de oportunidades basándose exclusivamente en sintaxis de dolor (`struggle`, `hate`, `broken`, `help`), alejándonos de la data basura y buscando problemas reales por resolver.

Consulta la carpeta [`.specs/`](./.specs/) para ver el diseño técnico y los Contratos de Datos.

---
**Build in Public** • Desarrollado por [@GustavoOsorioDev](https://youtube.com/@GustavoOsorioDev)
