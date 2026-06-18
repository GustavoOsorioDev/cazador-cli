# ESPECIFICACIÓN 01 — REGLAS PARA LOS DATOS (Cazador)

## 1. ¿Para qué sirve esto?
Para que el bot siempre sepa qué información guardar y de qué tipo. Así, si mañana cambiamos la base de datos o le ponemos una IA más potente, todo seguirá funcionando sin romperse.

## 2. LA ESTRUCTURA (Clase `Oportunidad`)

| Campo | Tipo | ¿Obligatorio? | ¿Qué es? |
| :--- | :--- | :---: | :--- |
| `fuente` | `str` | ✅ | De dónde viene (ej. `r/webdev`) |
| `titulo` | `str` | ✅ | El título del post original |
| `comentarios` | `int` | — | Cuántos comentarios tiene (por defecto 0) |
| `votos` | `int` | — | Cuántos votos tiene (por defecto 0) |
| `enlace` | `str` | ✅ | El link directo al post |
| `dolor` | `str | None` | — | Un pedazo del texto del post. **A veces no viene** porque el RSS de Reddit es limitado. |
| `score_gap` | `float` | — | Qué tan buena es la oportunidad (0 o más). |
| `fecha` | `str` | ✅ | Cuándo se encontró (se genera solo) |

## 3. CÓMO CALCULAMOS EL VALOR (Scoring)

Usamos una función que solo recibe datos crudos. Esto permite probarla por separado sin enredos.

### Plan A: Con datos reales (API de Reddit)
`score = (comentarios * 0.4) + (votos * 0.0009)` multiplicado por las palabras de "frustración" encontradas.

### Plan B: Modo Gratis / RSS (El que usamos ahora)
`score = total de palabras de "frustración" encontradas en el título y el texto.`
> **Nota técnica:** Como el RSS no nos dice cuántos votos tiene un post, nos basamos 100% en el texto. Los resultados son números bajos (1-5), pero reales.

## 4. LO QUE NO PUEDE FALLAR
- El **enlace** no se puede repetir en la base de datos.
- El **score** nunca puede ser menor que 0.
- La **fecha** la pone el sistema siempre en modo automático.

---
*Versión 1.1.0 — "Dilo simple, construye sólido"*
