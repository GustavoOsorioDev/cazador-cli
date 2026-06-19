# 🛡️ FIREWALL LOCAL — cazador-cli

## 🎯 TRIGGERS ESPECÍFICOS (NIVEL 3 - SONNET/OPUS)
Cualquier cambio en la estructura de datos o lógica de negocio central activa el Yield Protocol:
- **Directorio `.specs/`**: Contratos de datos y reglas de arquitectura.
- **Directorio `src/models/`**: Definiciones de Pydantic y esquemas.
- **Directorio `db/`**: Lógica de persistencia SQLite.
- **Core Logic**: Cualquier cambio en el scoring o filtrado semántico.

## 🛑 PROTOCOLO DE INTEGRIDAD
1. Antes de modificar el código, verifica el Nivel en la Bitácora de Decisiones de @GustavoOsorioDev.
2. Si el modelo es Nivel 1/2 y la tarea toca los triggers anteriores, aplica YIELD.
3. Al finalizar, reporta siempre el ahorro de tokens (Efficiency Check).

---
"Ingeniería real, sin vibes."
