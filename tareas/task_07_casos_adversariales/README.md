# Task 07 · Casos adversariales

La búsqueda determinista encontró cinco expresiones válidas que el modelo final falla:

| Problema | Predicción | Correcta |
|---|---:|---:|
| `9999+1` | `0000` | `10000` |
| `9998+2` | `0000` | `10000` |
| `9999+9999` | `18998` | `19998` |
| `1000-999` | `11` | `1` |
| `4000-3999` | `001` | `1` |

Los casos combinan cambios de longitud, acarreos globales, préstamos a través de ceros y resultados
cortos. Demuestran que una exactitud promedio alta no equivale a haber aprendido un algoritmo universal.
El mapa comparativo se conserva en `artifacts/mapas_atencion/07_trampa_vs_control.png`.
