# Límites de la métrica de evaluación


## Qué mide

Compara las palabras de la respuesta del modelo con las de una
referencia y cuenta cuántas coinciden (precisión, cobertura y F1). No
entiende si las cifras están bien.


## Modos de falla conocidos

- Una respuesta correcta puede sacar un F1 muy bajo si el modelo agrega
  texto de más. Ejemplo: "¿Cuánto largo ocupan 11 filas de pallets de
  1400 mm?", f1=0.06, la cifra (15400 mm) estaba bien pero la respuesta
  pedía datos que no hacían falta.

- Una respuesta con un error de cálculo saca un F1 parecido a una
  correcta. Ejemplo: "¿Esta estimación de 22 pallets es una distribución
  físicamente validada?", f1=0.08, dijo que 22 no caben porque dos filas
  de 1200 mm pasarían los 2507 mm, pero suman 2400 mm.

- Una respuesta equivocada puede sacar el F1 más alto. Ejemplo: "Cada
  pallet mide 100 mm de alto. ¿Cuántos pallets caben en la rampla sin
  apilar?", f1=0.35 (el más alto de los 25), dijo que caben 13 y que era
  la distribución "óptima validada", pero caben 22.

- Una respuesta puede contestar otra cosa y igual salir mejor que una
  correcta. Ejemplo: "¿Cuántos pallets caben si se orientan con 1200 mm
  en el sentido del largo, sin apilar?", f1=0.25, dijo 22 usando 1400 mm
  a lo largo, y debían ser 13. Sacó más que la respuesta correcta de
  "¿cuál es la altura total de pallet más producto?" (f1=0.22).

- Una respuesta correcta puede sacar F1 bajo solo por usar otras
  palabras. Ejemplo: "¿Cuál es el peso máximo que soporta la rampla?",
  f1=0.09, el modelo pidió el dato en vez de inventarlo, que era lo
  correcto.

- El F1 no ve que el mismo dato cambie entre respuestas. En la muestra el
  modelo dio como máximo de pallets 11, 13, 20 y 22 según la pregunta.


## Muestra revisada

Revisé a mano 10 casos de 25 respuestas generadas con gemini-3.5-flash:
los 5 con F1 más bajo (0.06 a 0.12) y los 5 con F1 más alto (0.22 a
0.35). Los califiqué con la rúbrica (corrección factual, completitud y
contradicción) y están en `docs/revision_manual.json`. De los 10, 5 son
correctos y 5 tienen algún error. No revisé los casos del medio.


## Recomendación de uso

Usar el F1 solo para comparar versiones del prompt o del modelo con las
mismas preguntas, no para decidir si una respuesta está bien o mal. En
este pipeline el F1 va de 0.06 a 0.35 (promedio 0.18) y no sirve como
nota de corte. Revisar a mano las respuestas con cantidades de pallets,
alturas o medidas, las que digan "validada" u "óptima" y las que falte
un dato (peso, altura del pallet).
