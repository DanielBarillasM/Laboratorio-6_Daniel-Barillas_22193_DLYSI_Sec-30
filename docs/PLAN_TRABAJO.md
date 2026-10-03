# Plan de trabajo - Laboratorio 6

## Objetivo

Construir, interpretar y validar una calculadora neuronal `seq2seq` que produzca el resultado carácter por carácter mediante una GRU bidireccional, atención aditiva de Bahdanau y un decoder recurrente.

## Identidad y restricciones

- Estudiante: Pablo Daniel Barillas Moreno.
- Carné: 22193.
- Curso: Deep Learning 2026, sección 30.
- Dispositivo oficial: CPU.
- Semilla: 2026.
- Entrenamiento: números de uno a cuatro dígitos.
- Límite del torneo: 750,000 parámetros.
- Dependencias dentro del notebook: PyTorch, Matplotlib y biblioteca estándar.
- No se permite NumPy ni `nn.MultiheadAttention`.

## Fases

1. Preservar el machote y completar identidad e investigación.
2. Implementar la atención aditiva sin modificar las verificaciones.
3. Implementar un paso del decoder y validar formas tensoriales.
4. Entrenar baselines con y sin atención.
5. medir exactitud por cifras e interpretar mapas de atención.
6. probar la hipótesis de invertir la salida para facilitar el acarreo.
7. localizar cinco casos adversariales válidos y explicarlos.
8. ejecutar el notebook de arriba abajo y congelar los pesos.
9. construir README, informe y presentación del repositorio.
10. validar artefactos, compilar PDF y sincronizar GitHub.

## Criterio experimental

La comparación principal modifica únicamente `invertir_salida`. Se considerará útil si mejora la exactitud de cuatro cifras y de acarreos en cadena sin superar el límite de parámetros. Las cifras cinco y seis se reportan como evaluación fuera de distribución y nunca se usan para entrenar.

## Cierre de entrega y acción futura

El registro del Laboratorio 6 fue enviado desde un kernel reiniciado y el notebook conserva la confirmación
del formulario junto con la huella `94e198ec75ec`. La clave secreta continúa reservada para el Laboratorio 7:
la última celda no se ejecutó y `CLAVE = None` permanece intacto hasta que el profesor revele la clave.
