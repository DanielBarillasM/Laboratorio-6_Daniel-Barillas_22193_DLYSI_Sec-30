# Task 03 · Paso del decoder

Cada paso embebe el token anterior, consulta la atención con el estado actual, actualiza la `GRUCell` con
`[embedding, contexto]` y proyecta `[nuevo_estado, contexto]` al vocabulario. La alternativa sin atención
reutiliza el resumen fijo del encoder y permite una comparación controlada.

La verificación oficial confirma logits `(B, 15)`, estado `(B, 6)`, pesos `(B, 4)` y enmascaramiento de
padding. La salida final contiene `OK - paso del decoder correcto`.
