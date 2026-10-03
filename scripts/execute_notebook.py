"""Ejecuta el laboratorio por etapas y obtiene evidencia reproducible sin enviar formularios."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import nbformat
from nbclient import NotebookClient


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks" / "01_calculadora_neuronal_final.ipynb"
OFFICIAL = ROOT / "S13_Lab06_Calculadora_Neuronal_ESTUDIANTE.ipynb"
METRICS_DIR = ROOT / "artifacts" / "metricas"
TEMP_DIR = ROOT / ".tmp"


ANALYSIS = r'''
from pathlib import Path

metricas_dir = Path("artifacts/metricas")
metricas_dir.mkdir(parents=True, exist_ok=True)

por_cifras = {
    "base_con_atencion": {str(k): v for k, v in exactitud_por_cifras(modelo_atencion).items()},
    "base_sin_atencion": {str(k): v for k, v in exactitud_por_cifras(modelo_sin).items()},
    "torneo": {str(k): v for k, v in exactitud_por_cifras(modelo_torneo).items()},
}
metricas = {
    "identidad": {"nombre": NOMBRE, "carne": CARNE},
    "config_base": CONFIG_BASE,
    "config_torneo": CONFIG_TORNEO,
    "validacion": {
        "base_con_atencion": exactitud(modelo_atencion, validacion),
        "base_sin_atencion": exactitud(modelo_sin, validacion),
        "torneo": exactitud(modelo_torneo, validacion),
    },
    "por_cifras": por_cifras,
    "parametros": {
        "base_con_atencion": contar_parametros(modelo_atencion),
        "base_sin_atencion": contar_parametros(modelo_sin),
        "torneo": contar_parametros(modelo_torneo),
    },
    "huellas": {
        "base_con_atencion": huella(modelo_atencion),
        "base_sin_atencion": huella(modelo_sin),
        "torneo": huella(modelo_torneo),
    },
    "historias": {
        "base_con_atencion": historia_atencion,
        "base_sin_atencion": historia_sin,
        "torneo": historia_torneo,
    },
}
(metricas_dir / "resultados.json").write_text(
    json.dumps(metricas, ensure_ascii=False, indent=2), encoding="utf-8"
)

familias = [
    ("9999+1", "acarreo que atraviesa todas las columnas"),
    ("9998+2", "acarreo encadenado desde las unidades"),
    ("8999+1001", "acarreos simultáneos y cambio de longitud"),
    ("9999+9999", "acarreos en las cuatro posiciones"),
    ("1000-999", "préstamo encadenado con resultado pequeño"),
    ("4000-3999", "préstamos a través de ceros internos"),
    ("7000-2999", "préstamo largo desde la cifra más significativa"),
    ("9876-9875", "resta casi idéntica con salida de una cifra"),
    ("9090+919", "ceros internos y operandos de distinta longitud"),
    ("5005-4999", "ceros internos y préstamos consecutivos"),
]
rng_busqueda = random.Random(22193)
for _ in range(15000):
    p, _ = generar_problema(rng_busqueda, max_cifras=4)
    familias.append((p, "caso válido hallado en búsqueda determinista fuera del entrenamiento"))

unicos = []
vistos = set()
for problema, razon in familias:
    if problema not in vistos:
        vistos.add(problema)
        unicos.append((problema, razon))

fallos = []
for inicio in range(0, len(unicos), 512):
    lote = unicos[inicio:inicio + 512]
    predicciones = modelo_torneo.resolver([p for p, _ in lote])
    for (problema, razon), prediccion in zip(lote, predicciones):
        correcta = respuesta_correcta(problema)
        if prediccion != correcta:
            fallos.append({
                "problema": problema, "prediccion": prediccion,
                "correcta": correcta, "razon": razon,
            })
            if len(fallos) == 5:
                break
    if len(fallos) == 5:
        break

assert len(fallos) == 5, "No se encontraron cinco fallos válidos; amplíe la búsqueda."
(metricas_dir / "trampas_candidatas.json").write_text(
    json.dumps(fallos, ensure_ascii=False, indent=2), encoding="utf-8"
)
print("Artefactos de métricas guardados.")
print(json.dumps({"validacion": metricas["validacion"], "trampas": fallos}, ensure_ascii=False, indent=2))
'''


def execute(stage: str) -> None:
    notebook = nbformat.read(NOTEBOOK, as_version=4)
    stop = 25 if stage == "discover" else 30
    working = nbformat.v4.new_notebook(
        cells=[cell for cell in notebook.cells[:stop]] + [nbformat.v4.new_code_cell(ANALYSIS)],
        metadata=notebook.metadata,
    )
    TEMP_DIR.mkdir(exist_ok=True)
    path = TEMP_DIR / f"lab6_{stage}.ipynb"
    client = NotebookClient(
        working, timeout=1800, kernel_name="python3", resources={"metadata": {"path": str(ROOT)}},
    )
    print(f"Ejecutando etapa {stage} ({stop} celdas oficiales + análisis)...")
    client.execute()
    nbformat.write(working, path)

    if stage == "final":
        for index in range(stop):
            if notebook.cells[index].cell_type == "code":
                notebook.cells[index].execution_count = working.cells[index].execution_count
                notebook.cells[index].outputs = working.cells[index].outputs
        nbformat.write(notebook, NOTEBOOK)
        nbformat.write(notebook, OFFICIAL)
        print(f"Salidas integradas en {NOTEBOOK}")
    print(f"Ejecución guardada en {path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=("discover", "final"), required=True)
    args = parser.parse_args()
    METRICS_DIR.mkdir(parents=True, exist_ok=True)
    execute(args.stage)


if __name__ == "__main__":
    main()
