"""Auditoría reproducible del laboratorio contra los requisitos verificables de la guía."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import nbformat
import pymupdf
import torch


ROOT = Path(__file__).resolve().parents[1]
ORIGINAL = ROOT / "notebooks" / "00_machote_original.ipynb"
FINAL = ROOT / "notebooks" / "01_calculadora_neuronal_final.ipynb"
OFFICIAL = ROOT / "S13_Lab06_Calculadora_Neuronal_ESTUDIANTE.ipynb"
METRICS = ROOT / "artifacts" / "metricas" / "resultados.json"
TRAPS = ROOT / "artifacts" / "metricas" / "trampas_candidatas.json"
OUTPUT = ROOT / "artifacts" / "validacion" / "validation.json"


def fingerprint(state: dict[str, torch.Tensor]) -> str:
    text = "".join(repr(t.detach().cpu().flatten().tolist()) for t in state.values())
    return hashlib.sha256(text.encode()).hexdigest()[:12]


def require(condition: bool, message: str, checks: list[str]) -> None:
    if not condition:
        raise AssertionError(message)
    checks.append(message)


def stream_text(cell) -> str:
    return "".join(output.get("text", "") for output in cell.get("outputs", [])
                   if output.output_type == "stream")


def main() -> None:
    checks: list[str] = []
    original = nbformat.read(ORIGINAL, as_version=4)
    final = nbformat.read(FINAL, as_version=4)
    official = nbformat.read(OFFICIAL, as_version=4)

    require(len(final.cells) == 33, "El notebook conserva las 33 celdas oficiales.", checks)
    require(final.cells[10].source == original.cells[10].source,
            "La verificación oficial del Bloque 2 está intacta.", checks)
    require(final.cells[14].source == original.cells[14].source,
            "La verificación oficial del Bloque 3 está intacta.", checks)
    require(final == official, "La copia con nombre oficial es idéntica al notebook final.", checks)

    code = "\n".join(cell.source for cell in final.cells if cell.cell_type == "code")
    lowered = code.lower()
    require("import numpy" not in lowered and "from numpy" not in lowered,
            "El código del notebook no importa NumPy.", checks)
    require("nn.multiheadattention" not in lowered,
            "El código no utiliza nn.MultiheadAttention.", checks)
    require("TODO" not in code, "No quedan TODO en celdas de código.", checks)
    require('NOMBRE = "Pablo Daniel Barillas Moreno"' in code and 'CARNE = "22193"' in code,
            "Nombre y carné están completos.", checks)
    require("MAX_CIFRAS = 4" in code, "El entrenamiento conserva MAX_CIFRAS=4.", checks)
    require("CLAVE = None" in final.cells[32].source,
            "La clave del torneo permanece en None.", checks)

    errors = [(i, output.get("ename")) for i, cell in enumerate(final.cells)
              if cell.cell_type == "code" for output in cell.get("outputs", [])
              if output.output_type == "error"]
    require(not errors, "No hay salidas de error en el notebook.", checks)
    executed = [cell.execution_count for cell in final.cells[:30] if cell.cell_type == "code"]
    require(executed == list(range(1, 15)),
            "Las 14 celdas académicas previas al registro tienen conteos consecutivos.", checks)
    require(final.cells[30].execution_count is None,
            "El formulario externo no fue enviado automáticamente.", checks)
    require(final.cells[32].execution_count is None,
            "La celda del torneo no fue ejecutada antes de recibir la clave.", checks)
    require("OK - atención aditiva correcta" in stream_text(final.cells[10]),
            "La verificación de atención imprimió OK.", checks)
    require("OK - paso del decoder correcto" in stream_text(final.cells[14]),
            "La verificación del decoder imprimió OK.", checks)
    require("OK - 5 de 5 problemas rompen su calculadora" in stream_text(final.cells[26]),
            "Los cinco contraejemplos rompen el modelo final.", checks)

    metrics = json.loads(METRICS.read_text(encoding="utf-8"))
    traps = json.loads(TRAPS.read_text(encoding="utf-8"))
    require(metrics["validacion"]["base_con_atencion"] >= 0.60,
            "La exactitud base con atención supera 0.60.", checks)
    require(metrics["validacion"]["torneo"] == 0.972,
            "La exactitud congelada del torneo es 0.972.", checks)
    require(metrics["por_cifras"]["torneo"]["4"] == 0.95,
            "La exactitud del torneo en cuatro cifras es 0.95.", checks)
    require(len(traps) == 5 and len({item["problema"] for item in traps}) == 5,
            "Hay cinco trampas distintas documentadas.", checks)
    require(all(item["prediccion"] != item["correcta"] for item in traps),
            "Las cinco trampas contienen predicciones incorrectas reales.", checks)

    checkpoints = {
        "base_con_atencion": ROOT / "modelos_lab6" / "base_con_atencion.pt",
        "base_sin_atencion": ROOT / "modelos_lab6" / "base_sin_atencion.pt",
        "torneo": ROOT / "modelos_lab6" / "torneo_22193.pt",
    }
    checkpoint_report = {}
    for name, path in checkpoints.items():
        payload = torch.load(path, map_location="cpu", weights_only=True)
        count = sum(t.numel() for t in payload["estado"].values())
        mark = fingerprint(payload["estado"])
        require(count == metrics["parametros"][name],
                f"El checkpoint {name} conserva {count} parámetros.", checks)
        require(count <= 750_000, f"El checkpoint {name} respeta el límite de parámetros.", checks)
        require(mark == metrics["huellas"][name],
                f"La huella de {name} coincide: {mark}.", checks)
        require(len(payload["historia"]["perdida"]) == 15,
                f"El checkpoint {name} conserva 15 épocas.", checks)
        checkpoint_report[name] = {"ruta": path.relative_to(ROOT).as_posix(),
                                   "parametros": count, "huella": mark}

    required_artifacts = [
        ROOT / "artifacts" / "figuras" / "01_distribucion_longitudes.png",
        ROOT / "artifacts" / "figuras" / "02_curvas_entrenamiento.png",
        ROOT / "artifacts" / "figuras" / "03_exactitud_por_cifras_baselines.png",
        ROOT / "artifacts" / "figuras" / "05_exactitud_base_vs_torneo.png",
        ROOT / "artifacts" / "mapas_atencion" / "04_atencion_baseline.png",
        ROOT / "artifacts" / "mapas_atencion" / "06_atencion_torneo.png",
        ROOT / "artifacts" / "mapas_atencion" / "07_trampa_vs_control.png",
    ]
    require(all(path.exists() and path.stat().st_size > 0 for path in required_artifacts),
            "Las siete figuras exportadas existen y no están vacías.", checks)

    report_pdf = ROOT / "informe" / "informe_laboratorio_6.pdf"
    presentation_pdf = ROOT / "presentacion_repositorio" / "presentacion_repositorio.pdf"
    report_pages = len(pymupdf.open(report_pdf))
    presentation_pages = len(pymupdf.open(presentation_pdf))
    require(report_pages >= 12, f"El informe compilado tiene {report_pages} páginas.", checks)
    require(presentation_pages <= 12,
            f"La presentación compilada tiene {presentation_pages} páginas.", checks)

    task_docs = sorted((ROOT / "tareas").glob("task_*/README.md"))
    require(len(task_docs) == 8, "Los ocho bloques tienen documentación separada.", checks)

    html_presentation = ROOT / "presentacion_html" / "index.html"
    html_source = html_presentation.read_text(encoding="utf-8")
    html_slides = re.findall(r'<section\s+class="slide(?:\s|\")', html_source)
    require(len(html_slides) == 15,
            "La presentación HTML contiene 15 diapositivas.", checks)
    html_assets = [
        ROOT / "presentacion_html" / "assets" / "styles.css",
        ROOT / "presentacion_html" / "assets" / "app.js",
        ROOT / "presentacion_html" / "assets" / "favicon.svg",
    ]
    require(all(path.exists() and path.stat().st_size > 0 for path in html_assets),
            "Los estilos, controles y favicon de la presentación HTML existen.", checks)
    require(all(path.relative_to(ROOT).as_posix() in (ROOT / "README.md").read_text(encoding="utf-8")
                for path in [html_presentation]),
            "El README enlaza la presentación HTML interactiva.", checks)

    registration_marker = ROOT / "modelos_lab6" / "registro_enviado.txt"
    result = {
        "estado": "APROBADO_CON_ACCION_EXTERNA_PENDIENTE" if not registration_marker.exists() else "APROBADO",
        "checks_superados": len(checks),
        "comprobaciones": checks,
        "metricas_clave": {
            "validacion_atencion": metrics["validacion"]["base_con_atencion"],
            "validacion_sin_atencion": metrics["validacion"]["base_sin_atencion"],
            "validacion_torneo": metrics["validacion"]["torneo"],
            "torneo_cuatro_cifras": metrics["por_cifras"]["torneo"]["4"],
        },
        "checkpoints": checkpoint_report,
        "documentos": {"informe_paginas": report_pages, "presentacion_paginas": presentation_pages},
        "pendientes_manuales": ([] if registration_marker.exists() else [
            "Ejecutar la celda de registro del formulario con conexión a internet.",
            "Guardar el notebook después del envío y conservar la misma huella.",
            "Durante el torneo, escribir la clave revelada por el profesor y ejecutar la última celda.",
        ]),
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
