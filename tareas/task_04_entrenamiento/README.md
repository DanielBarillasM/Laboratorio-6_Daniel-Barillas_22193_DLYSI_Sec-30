# Task 04 · Entrenamiento controlado

Ambos baselines usan semilla 2026, 40,000 ejemplos, 15 épocas, lote 128, Adam con `lr=3e-3` y la misma
capacidad. La única diferencia es el uso de atención.

| Modelo | Validación | Parámetros |
|---|---:|---:|
| Con atención | **83.70 %** | 186,767 |
| Sin atención | 67.25 % | 186,767 |

Los historiales completos se encuentran en `artifacts/metricas/resultados.json` y las curvas en
`artifacts/figuras/02_curvas_entrenamiento.png`.
