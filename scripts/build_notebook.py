"""Construye el notebook final a partir del machote oficial sin alterar sus verificaciones."""

from __future__ import annotations

import json
from pathlib import Path

import nbformat


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "notebooks" / "00_machote_original.ipynb"
TARGET = ROOT / "notebooks" / "01_calculadora_neuronal_final.ipynb"
METRICS = ROOT / "artifacts" / "metricas" / "resultados.json"
TRAPS = ROOT / "artifacts" / "metricas" / "trampas_candidatas.json"


CSS = r"""
<style>
:root { --blue:#0066ff; --cyan:#00ffff; --ink:#1e1e1e; --paper:#ffffff; }
.jp-RenderedHTMLCommon h1, .jp-RenderedHTMLCommon h2, .jp-RenderedHTMLCommon h3 {
  color: var(--blue); font-family: "DejaVu Sans", sans-serif; font-weight: 700;
}
.jp-RenderedHTMLCommon h1 { border-bottom: 4px solid var(--cyan); padding-bottom: .35rem; }
.jp-RenderedHTMLCommon blockquote { border-left: 5px solid var(--cyan); background: #eef6ff; padding: .8rem 1rem; }
.jp-RenderedHTMLCommon table { border-collapse: collapse; }
.jp-RenderedHTMLCommon th { background: var(--ink); color: var(--paper); }
.jp-RenderedHTMLCommon code { color: #004bbd; }
.lab-card { border: 1px solid #bfd7ff; border-left: 6px solid var(--blue); border-radius: 8px;
  padding: 1rem 1.2rem; background: linear-gradient(135deg,#f7fbff,#ffffff); margin: 1rem 0; }
.lab-kicker { color:#0056d6; font-size:.82rem; font-weight:700; letter-spacing:.12em; text-transform:uppercase; }
</style>
<div class="lab-card"><div class="lab-kicker">Deep Learning · Laboratorio 6</div>
<strong>Bitácora reproducible:</strong> cada conclusión se apoya en las salidas visibles del notebook y en
artefactos versionados del experimento.</div>
"""


RESEARCH = r"""### Respuestas

**1.** Un encoder que comprime toda la secuencia en un único vector de tamaño fijo crea un cuello de
botella: conforme crece la entrada, ese vector debe conservar demasiada información y puede perder
detalles relevantes. Bahdanau propone que, en cada paso de salida, el decoder construya un contexto
$c_i$ como suma ponderada de todos los estados del encoder; así consulta de forma selectiva la parte útil
de la entrada en vez de depender de un solo resumen.  
**Fuente:** Bahdanau, Cho y Bengio (2014), sección 3.1 y figura 3.

**2.** Al escribir el tercer dígito, $s_{i-1}$ es el estado del decoder después de haber producido los dos
dígitos anteriores; resume el prefijo ya escrito y la información acumulada. Cada $h_j$ representa un
carácter concreto de `4821+3976` después de ser procesado por el encoder. En el Transformer, el vector
de consulta (*query*) del decoder desempeña el papel de $s_{i-1}$ y las claves/valores derivados de la
salida del encoder corresponden a los $h_j$.  
**Fuente:** Bahdanau, Cho y Bengio (2014), sección 3.1.

**3.** Sutskever et al. invirtieron la fuente para reducir la distancia mínima entre elementos relacionados
de entrada y salida, facilitando la optimización sin cambiar la longitud promedio de las dependencias.
Como la suma manual comienza por unidades y propaga acarreos hacia la izquierda, predigo que invertir
la **salida** será especialmente útil: el decoder generará primero unidades y podrá transportar el acarreo
en su estado recurrente. Mantendré la entrada original para aislar una sola modificación.  
**Fuente:** Sutskever, Vinyals y Le (2014), sección 3.3.
"""


GENERATOR_ANSWER = r"""**Respuesta 1.1.** Cada operando de exactamente cuatro cifras admite 9,000 valores.
Para la suma existen $9{,}000^2=81{,}000{,}000$ pares ordenados. En la resta no negativa se permiten
$9{,}000(9{,}000+1)/2=40{,}504{,}500$ pares con $a\ge b$. En total hay **121,504,500** problemas,
muy por encima de los 40,000 ejemplos de entrenamiento (menos de 0.033 % del espacio, incluso antes de
considerar longitudes menores). Por tanto, el modelo no puede memorizar todas las respuestas posibles:
para generalizar debe aprender regularidades sobre dígitos, posiciones, acarreos y préstamos.
"""


HYPOTHESIS = r"""**Hipótesis.** Creo que cambiar únicamente `invertir_salida=True` mejorará la exactitud en
problemas de cuatro cifras y con acarreos o préstamos encadenados, porque el decoder producirá primero
las unidades y podrá transportar esa información hacia las posiciones siguientes en su estado recurrente.
Lo consideraré útil si supera al baseline con atención en cuatro cifras y mantiene o mejora la exactitud
global de validación, sin aumentar parámetros, datos ni épocas.
"""


def source(cell) -> str:
    return cell.source if isinstance(cell.source, str) else "".join(cell.source)


def results_markdown(metrics: dict | None) -> tuple[str, str]:
    if not metrics:
        return (
            "**Preguntas 5.1 y 5.2.** Estas respuestas se completarán automáticamente después de ejecutar "
            "los dos modelos y medir sus resultados.",
            "**Resultado.** Se completará automáticamente después del experimento controlado.",
        )

    digit_att = metrics["por_cifras"]["base_con_atencion"]
    digit_no = metrics["por_cifras"]["base_sin_atencion"]
    digit_t = metrics["por_cifras"]["torneo"]
    gaps = {k: digit_att[k] - digit_no[k] for k in digit_att}
    best_digit = max(gaps, key=gaps.get)
    p51 = f"""**Pregunta 5.1.** La mayor ventaja observada de la atención apareció en **{best_digit} cifras**:
{digit_att[best_digit]:.1%} frente a {digit_no[best_digit]:.1%}, una diferencia de {gaps[best_digit]:+.1%}.
Con una o dos cifras la secuencia es corta y un resumen fijo todavía puede retener casi toda la información;
al crecer la entrada se intensifica el cuello de botella descrito en el Bloque 0. Fuera del rango de
entrenamiento (cinco y seis cifras), ambos modelos muestran además que la atención no garantiza por sí
sola extrapolación algorítmica.

**Pregunta 5.2.** En `4821+3976` el mapa no equivale a una regla simbólica rígida: distribuye peso entre
posiciones de ambos operandos, aunque concentra regiones distintas conforme avanza la salida. El baseline
debe escribir primero el dígito más significativo, pero ese dígito depende de acarreos originados a la
derecha; por eso necesita anticipar información que todavía no ha exteriorizado. La visualización se
interpreta como evidencia de alineación aprendida, no como prueba de que cada celda represente literalmente
una columna de la suma.
"""
    base4 = digit_att["4"]
    tour4 = digit_t["4"]
    val_base = metrics["validacion"]["base_con_atencion"]
    val_tour = metrics["validacion"]["torneo"]
    verdict = "se cumplió" if tour4 > base4 and val_tour >= val_base else "se cumplió parcialmente"
    result = f"""**Resultado.** La hipótesis **{verdict}**. Al invertir solo la salida, la exactitud de cuatro
cifras cambió de {base4:.1%} a {tour4:.1%} y la validación global de {val_base:.1%} a {val_tour:.1%}.
El mapa del modelo de torneo debe leerse en el orden de generación invertido: primero resuelve posiciones
de menor valor y luego avanza hacia la izquierda, una secuencia compatible con la propagación de acarreo.
La comparación está controlada porque conserva arquitectura, semilla, datos, épocas y capacidad; su
limitación es que utiliza una sola semilla y 300 ejemplos por longitud, por lo que no estima variabilidad
entre entrenamientos ni cubre exhaustivamente el espacio de problemas.
"""
    return p51, result


def trap_cell(traps: list[dict] | None) -> str:
    if not traps:
        problems = ["9999+1", "1000-999", "9090+919", "7000-2999", "9876-9875"]
        reasons = ["candidato previo a la búsqueda automática"] * 5
    else:
        problems = [item["problema"] for item in traps[:5]]
        reasons = [item["razon"] for item in traps[:5]]
    rows = "\n".join(f'    "{p}",  # {reason}' for p, reason in zip(problems, reasons))
    return f'''TRAMPAS = [
{rows}
]


def es_trampa_valida(texto):
    for operacion in "+-":
        partes = texto.split(operacion)
        if len(partes) == 2 and all(p.isdigit() and len(p) <= MAX_CIFRAS for p in partes):
            a, b = partes
            if (len(a) > 1 and a[0] == "0") or (len(b) > 1 and b[0] == "0"):
                return False
            return operacion == "+" or int(a) >= int(b)
    return False


assert len(TRAMPAS) == 5 and all(es_trampa_valida(t) for t in TRAMPAS), "Escriba 5 problemas válidos."
assert len(set(TRAMPAS)) == 5, "Los 5 problemas deben ser distintos."
rotas = 0
for trampa, respuesta in zip(TRAMPAS, modelo_torneo.resolver(TRAMPAS)):
    falla = respuesta != respuesta_correcta(trampa)
    rotas += falla
    print(f"{{trampa:>10}} -> {{respuesta:<7}} {{'FALLA' if falla else 'correcto: busque otro'}}")
print(f"OK - {{rotas}} de 5 problemas rompen su calculadora")
'''


def reflection(traps: list[dict] | None) -> str:
    if not traps:
        problem = "el primer caso adversarial"
        predicted = "una respuesta incorrecta"
        expected = "el resultado exacto"
    else:
        problem = f'`{traps[0]["problema"]}`'
        predicted = f'`{traps[0]["prediccion"]}`'
        expected = f'`{traps[0]["correcta"]}`'
    return f"""**Reflexión final.** {problem} es el caso que mejor expone la debilidad seleccionada: la red
produce {predicted} cuando la respuesta correcta es {expected}. El mapa de atención permite comprobar
que el modelo sí consulta caracteres pertinentes, pero la alineación visual no asegura que ejecute de
forma consistente una regla de acarreo o préstamo. Concluyo que aprendió una aproximación estadística que
**imita muchas sumas y restas** dentro de la distribución, no un algoritmo simbólico infalible: cinco
contraejemplos válidos bastan para refutar una regla universal, aun cuando su exactitud promedio sea alta.
"""


def main() -> None:
    notebook = nbformat.read(SOURCE, as_version=4)
    original_checks = {i: source(notebook.cells[i]) for i in (10, 14)}
    metrics = json.loads(METRICS.read_text(encoding="utf-8")) if METRICS.exists() else None
    traps = json.loads(TRAPS.read_text(encoding="utf-8")) if TRAPS.exists() else None

    notebook.cells[0].source = source(notebook.cells[0]) + "\n\n" + CSS
    notebook.cells[1].source = '''# Identificación individual solicitada por la guía.
NOMBRE = "Pablo Daniel Barillas Moreno"
CARNE = "22193"

assert CARNE != "00000" and NOMBRE != "Escriba aquí su nombre", "Complete NOMBRE y CARNE."
print("OK -", NOMBRE, CARNE)'''
    notebook.cells[2].source = source(notebook.cells[2]) + '''

# Sistema visual Tech Innovation: consistente en todas las figuras del laboratorio.
AZUL_ELECTRICO, CIAN_NEON, GRIS_OSCURO = "#0066ff", "#00ffff", "#1e1e1e"
plt.rcParams.update({
    "figure.facecolor": "white", "axes.facecolor": "#f7fbff", "axes.edgecolor": GRIS_OSCURO,
    "axes.titleweight": "bold", "axes.titlecolor": AZUL_ELECTRICO,
    "axes.labelcolor": GRIS_OSCURO, "axes.prop_cycle": plt.cycler(color=[AZUL_ELECTRICO, "#00a6a6", "#7048e8"]),
    "grid.color": "#d8e8ff", "grid.alpha": 0.65, "font.family": "DejaVu Sans",
})
'''
    notebook.cells[4].source = RESEARCH
    notebook.cells[7].source = GENERATOR_ANSWER
    notebook.cells[9].source = '''class AtencionAditiva(nn.Module):
    def __init__(self, dim_dec, dim_enc, dim_att):
        super().__init__()
        self.W_q = nn.Linear(dim_dec, dim_att, bias=False)
        self.W_k = nn.Linear(dim_enc, dim_att, bias=False)
        self.v = nn.Linear(dim_att, 1, bias=False)

    def forward(self, estado_dec, salidas_enc, mascara_pad):
        # e_j = v^T tanh(W_q s + W_k h_j), calculado para todas las posiciones T.
        puntajes = self.v(torch.tanh(
            self.W_q(estado_dec).unsqueeze(1) + self.W_k(salidas_enc)
        )).squeeze(-1)
        puntajes = puntajes.masked_fill(mascara_pad, float("-inf"))
        pesos = torch.softmax(puntajes, dim=-1)
        contexto = torch.bmm(pesos.unsqueeze(1), salidas_enc).squeeze(1)
        return contexto, pesos'''
    notebook.cells[13].source = '''class Decoder(nn.Module):
    def __init__(self, n_tokens, dim_emb, dim_dec, dim_enc, dim_att, usar_atencion=True):
        super().__init__()
        self.usar_atencion = usar_atencion
        self.embedding = nn.Embedding(n_tokens, dim_emb, padding_idx=PAD)
        self.atencion = AtencionAditiva(dim_dec, dim_enc, dim_att)
        self.gru = nn.GRUCell(dim_emb + dim_enc, dim_dec)
        self.salida = nn.Linear(dim_dec + dim_enc, n_tokens)

    def paso(self, token_previo, estado, salidas_enc, mascara_pad, resumen):
        """token_previo (B,), estado (B, dim_dec) -> logits, nuevo_estado, pesos."""
        if not self.usar_atencion:
            contexto, pesos = resumen, None
            emb = self.embedding(token_previo)
            nuevo_estado = self.gru(torch.cat([emb, contexto], dim=-1), estado)
            return self.salida(torch.cat([nuevo_estado, contexto], dim=-1)), nuevo_estado, pesos

        emb = self.embedding(token_previo)
        contexto, pesos = self.atencion(estado, salidas_enc, mascara_pad)
        nuevo_estado = self.gru(torch.cat([emb, contexto], dim=-1), estado)
        logits = self.salida(torch.cat([nuevo_estado, contexto], dim=-1))
        return logits, nuevo_estado, pesos'''
    notebook.cells[20].source, notebook.cells[24].source = results_markdown(metrics)
    notebook.cells[22].source = HYPOTHESIS
    notebook.cells[23].source = '''CONFIG_TORNEO = {
    **CONFIG_BASE,
    "invertir_salida": True,  # única perilla: generación desde unidades hacia la izquierda
}

modelo_torneo, historia_torneo = entrenar(CONFIG_TORNEO, f"torneo_{CARNE}")
print("Parámetros:", contar_parametros(modelo_torneo))

graficar_por_cifras({"base con atención": modelo_atencion, "torneo": modelo_torneo})
mapa_atencion(modelo_torneo, ["4821+3976", "9999+1", "7305-2618"])'''
    notebook.cells[26].source = trap_cell(traps)
    notebook.cells[27].source = reflection(traps)

    for index, cell in enumerate(notebook.cells):
        cell.id = f"lab6-{index:02d}"
        if cell.cell_type == "code":
            cell.execution_count = None
            cell.outputs = []
    notebook.metadata.setdefault("kernelspec", {"display_name": "Python 3", "language": "python", "name": "python3"})
    notebook.metadata["laboratorio"] = {
        "autor": "Pablo Daniel Barillas Moreno", "carne": "22193", "tema": "Tech Innovation"
    }

    assert source(notebook.cells[10]) == original_checks[10], "La verificación del Bloque 2 cambió."
    assert source(notebook.cells[14]) == original_checks[14], "La verificación del Bloque 3 cambió."
    nbformat.write(notebook, TARGET)
    print(f"Notebook construido: {TARGET}")


if __name__ == "__main__":
    main()
