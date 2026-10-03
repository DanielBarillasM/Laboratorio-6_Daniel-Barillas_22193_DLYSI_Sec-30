# Task 01 · Generador de problemas

El generador crea sumas y restas no negativas de hasta cuatro cifras sin depender de un dataset externo.
Para operandos de exactamente cuatro cifras existen 81,000,000 sumas y 40,504,500 restas válidas, un
total de **121,504,500** expresiones. Los 40,000 ejemplos vistos representan menos de 0.033 % de ese
espacio, por lo que memorizar todas las respuestas es imposible.

La semilla `2026` fija la reproducibilidad. La distribución de longitudes se conserva en
`artifacts/figuras/01_distribucion_longitudes.png`.
