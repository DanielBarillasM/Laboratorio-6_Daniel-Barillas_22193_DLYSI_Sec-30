# Presentación HTML · Calculadora Neuronal

Presentación interactiva y autónoma del proceso, experimento y resultados del Laboratorio 6. Utiliza la
paleta **Tech Innovation** y reutiliza únicamente evidencia existente en `artifacts/`.

## Abrir

Abra `index.html` directamente en Chrome, Edge o Firefox. No requiere servidor, instalación ni conexión a
internet.

También puede iniciarse desde la raíz del repositorio:

```powershell
Start-Process .\presentacion_html\index.html
```

## Controles

| Acción | Tecla o control |
|---|---|
| Avanzar | `→`, `Page Down` o espacio |
| Retroceder | `←`, `Page Up` o `Shift` + espacio |
| Primera / última | `Home` / `End` |
| Índice | `O` o botón **Índice** |
| Mostrar guion | `G` o botón **Guion** |
| Pantalla completa | `F` |
| Imprimir o exportar PDF | `Ctrl` + `P` |

La navegación también funciona con botones, índice lateral y gesto horizontal en dispositivos táctiles.

## Contenido verificado

- 15 secciones desde el reto hasta las conclusiones.
- Métricas reales: 83.70%, 67.25%, 97.20% y 95.00% en cuatro cifras.
- Checkpoint del torneo: 186,767 parámetros y huella `94e198ec75ec`.
- Siete figuras exportadas del notebook ejecutado.
- Cinco predicciones incorrectas reales.
- Estado transparente: el registro externo fue aceptado, la huella se conservó y el torneo sigue sin ejecutar con `CLAVE = None`.

## Archivos

```text
presentacion_html/
├── index.html
├── README.md
└── assets/
    ├── app.js
    ├── favicon.svg
    └── styles.css
```

Las imágenes no se duplican: se cargan mediante rutas relativas desde `../artifacts/`, manteniendo una
única fuente de verdad para las figuras del laboratorio.
