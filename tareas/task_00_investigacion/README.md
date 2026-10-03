# Task 00 · Investigación guiada

## Objetivo

Explicar el cuello de botella de un único vector de tamaño fijo, el contexto dinámico de Bahdanau y la
motivación de invertir secuencias antes de formular una hipótesis experimental.

## Conclusiones

- La atención evita depender exclusivamente de un resumen fijo al construir un contexto distinto para
  cada paso de salida.
- El estado del decoder actúa como consulta; los estados por carácter del encoder aportan claves y valores.
- Invertir la salida alinea el orden de generación con la aritmética manual: unidades primero y acarreo
  hacia posiciones de mayor valor.

## Fuentes

- Bahdanau, Cho y Bengio (2014), sección 3.1 y figura 3.
- Sutskever, Vinyals y Le (2014), sección 3.3.

**Evidencia:** respuestas completas en el Bloque 0 del notebook final.
