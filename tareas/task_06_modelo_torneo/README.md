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

## Resultado oficial · clave 5978

| Nivel | Aciertos | Puntaje |
|---|---:|---:|
| Calentamiento | 20/20 | 15.0/15 |
| Cuatro cifras | 17/20 | 25.5/30 |
| Acarreos en cadena | 16/16 | 40.0/40 |
| Jefe final | 0/10 | 0.0/15 |
| **Total** | **53/66** | **80.5/100** |

El checkpoint se cargó desde `modelos_lab6/torneo_22193.pt` sin ejecutar entrenamiento. La huella fue
`94e198ec75ec` antes y después, y el formulario confirmó el envío. El desempeño perfecto en acarreos y
la caída total en cinco cifras coinciden con los límites identificados durante el Laboratorio 6.
