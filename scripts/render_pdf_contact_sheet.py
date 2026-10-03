"""Renderiza todas las páginas de un PDF en una hoja de contacto para revisión visual."""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import fitz
from PIL import Image, ImageDraw


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--columns", type=int, default=3)
    args = parser.parse_args()

    document = fitz.open(args.pdf)
    thumbnails = []
    for number, page in enumerate(document, start=1):
        pixmap = page.get_pixmap(matrix=fitz.Matrix(0.75, 0.75), alpha=False)
        image = Image.frombytes("RGB", (pixmap.width, pixmap.height), pixmap.samples)
        image.thumbnail((430, 560))
        canvas = Image.new("RGB", (450, 600), "white")
        canvas.paste(image, ((450 - image.width) // 2, 28))
        ImageDraw.Draw(canvas).text((16, 8), f"Página {number}", fill="#1e1e1e")
        thumbnails.append(canvas)

    rows = math.ceil(len(thumbnails) / args.columns)
    sheet = Image.new("RGB", (450 * args.columns, 600 * rows), "#dce8f7")
    for index, image in enumerate(thumbnails):
        sheet.paste(image, ((index % args.columns) * 450, (index // args.columns) * 600))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(args.output)
    print(f"{len(thumbnails)} páginas renderizadas en {args.output}")


if __name__ == "__main__":
    main()
