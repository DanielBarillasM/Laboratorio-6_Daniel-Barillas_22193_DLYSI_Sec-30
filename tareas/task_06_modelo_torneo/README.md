# Task 06 · Modelo del torneo

## Hipótesis

Invertir únicamente la salida facilitará el acarreo porque el decoder producirá unidades primero y podrá
propagar información hacia la izquierda en su estado recurrente.

## Resultado

| Métrica | Baseline | Torneo | Cambio |
|---|---:|---:|---:|
| Validación | 83.70 % | **97.20 %** | +13.50 pp |
| Cuatro cifras | 70.33 % | **95.00 %** | +24.67 pp |
| Parámetros | 186,767 | 186,767 | 0 |

La hipótesis se cumple. La limitación principal es el uso de una sola semilla y una muestra de 300
problemas por longitud. Huella congelada del modelo: `94e198ec75ec`.
