"""Extrae las figuras PNG embebidas del notebook ejecutado con nombres estables."""

from __future__ import annotations

import base64
from pathlib import Path

import nbformat


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks" / "01_calculadora_neuronal_final.ipynb"
FIGURES = ROOT / "artifacts" / "figuras"
ATTENTION = ROOT / "artifacts" / "mapas_atencion"

NAMES = {
    (6, 0): (FIGURES, "01_distribucion_longitudes.png"),
    (17, 0): (FIGURES, "02_curvas_entrenamiento.png"),
    (19, 0): (FIGURES, "03_exactitud_por_cifras_baselines.png"),
    (19, 1): (ATTENTION, "04_atencion_baseline.png"),
    (23, 0): (FIGURES, "05_exactitud_base_vs_torneo.png"),
    (23, 1): (ATTENTION, "06_atencion_torneo.png"),
    (28, 0): (ATTENTION, "07_trampa_vs_control.png"),
}


def main() -> None:
    notebook = nbformat.read(NOTEBOOK, as_version=4)
    for folder in (FIGURES, ATTENTION):
        folder.mkdir(parents=True, exist_ok=True)

    exported = []
    for cell_index, cell in enumerate(notebook.cells):
        image_index = 0
        for output in cell.get("outputs", []):
            data = output.get("data", {})
            if "image/png" not in data:
                continue
            key = (cell_index, image_index)
            if key not in NAMES:
                raise KeyError(f"Figura sin nombre estable: celda {cell_index}, imagen {image_index}")
            folder, name = NAMES[key]
            destination = folder / name
            destination.write_bytes(base64.b64decode(data["image/png"]))
            exported.append(destination.relative_to(ROOT).as_posix())
            image_index += 1

    expected = len(NAMES)
    assert len(exported) == expected, f"Se exportaron {len(exported)} de {expected} figuras."
    print("Figuras exportadas:")
    print("\n".join(f"- {path}" for path in exported))


if __name__ == "__main__":
    main()
