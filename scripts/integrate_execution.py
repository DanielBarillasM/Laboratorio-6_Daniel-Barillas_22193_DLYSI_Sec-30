"""Integra una ejecución temporal ya completada en el notebook final."""

from pathlib import Path

import nbformat


ROOT = Path(__file__).resolve().parents[1]
target_path = ROOT / "notebooks" / "01_calculadora_neuronal_final.ipynb"
official_path = ROOT / "S13_Lab06_Calculadora_Neuronal_ESTUDIANTE.ipynb"
executed_path = ROOT / ".tmp" / "lab6_final.ipynb"

target = nbformat.read(target_path, as_version=4)
executed = nbformat.read(executed_path, as_version=4)
for index in range(30):
    if target.cells[index].cell_type == "code":
        target.cells[index].execution_count = executed.cells[index].execution_count
        target.cells[index].outputs = executed.cells[index].outputs

nbformat.write(target, target_path)
nbformat.write(target, official_path)
print(f"Salidas integradas desde {executed_path.name} en {target_path.name}")
print(f"Copia oficial actualizada: {official_path.name}")
