# Task 02 · Atención aditiva de Bahdanau

La implementación proyecta el estado del decoder y cada salida del encoder, aplica `tanh`, calcula un
puntaje escalar por posición y enmascara `<PAD>` con `-inf`. Después usa `softmax` y una multiplicación
por lotes para obtener el contexto ponderado.

```python
puntajes = self.v(torch.tanh(
    self.W_q(estado_dec).unsqueeze(1) + self.W_k(salidas_enc)
)).squeeze(-1)
puntajes = puntajes.masked_fill(mascara_pad, float("-inf"))
pesos = torch.softmax(puntajes, dim=-1)
contexto = torch.bmm(pesos.unsqueeze(1), salidas_enc).squeeze(1)
```

La celda oficial, preservada sin cambios, verifica formas, suma unitaria de pesos y peso cero en padding.
Su ejecución final imprime `OK - atención aditiva correcta`.
