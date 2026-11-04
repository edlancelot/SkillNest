import json

revision_manual = [
    {
        "consulta": "¿Cuánto largo ocupan 11 filas de pallets de 1400 mm?",
        "f1": 0.06,
        "correccion_factual": "si",
        "completitud": "si",
        "contradiccion": "no",
        "nota": "la cifra 15400 mm está bien pero enterrada; pide la orientación (que ya estaba en la pregunta) y la altura del pallet",
    },
    {
        "consulta": "¿Esta estimación de 22 pallets es una distribución físicamente validada?",
        "f1": 0.08,
        "correccion_factual": "no",
        "completitud": "no",
        "contradiccion": "no",
        "nota": "dice que 22 no cabe porque dos filas de 1200 mm pasarían los 2507 mm, pero suman 2400 mm; error de cálculo",
    },
    {
        "consulta": "¿Cuál es el peso máximo que soporta la rampla?",
        "f1": 0.09,
        "correccion_factual": "si",
        "completitud": "si",
        "contradiccion": "no",
        "nota": "no inventa el peso y pide la ficha técnica, que es lo correcto; el f1 es bajo solo por las palabras",
    },
    {
        "consulta": "¿Cuántos pallets caben a lo ancho si el lado de 1400 mm va atravesado?",
        "f1": 0.12,
        "correccion_factual": "no",
        "completitud": "si",
        "contradiccion": "no",
        "nota": "1 pallet y 1107 mm de sobra está bien, pero agrega que caben 11 a lo largo y serían 13",
    },
    {
        "consulta": "Con pallets de 100 mm de alto, ¿caben 20 pallets?",
        "f1": 0.12,
        "correccion_factual": "no",
        "completitud": "si",
        "contradiccion": "no",
        "nota": "dice que el máximo es 20 (dos filas de 10) y el máximo es 22; además pregunta si los 2494 mm incluyen el pallet cuando ya se dio la altura",
    },
    {
        "consulta": "Con pallets de 100 mm, ¿cuál es la altura total de pallet más producto?",
        "f1": 0.22,
        "correccion_factual": "si",
        "completitud": "si",
        "contradiccion": "no",
        "nota": "2594 mm con 5 mm de holgura, correcto; después pregunta por la orientación sin necesidad",
    },
    {
        "consulta": "¿Cuántos pallets caben si se orientan con 1200 mm en el sentido del largo, sin apilar?",
        "f1": 0.25,
        "correccion_factual": "no",
        "completitud": "no",
        "contradiccion": "si",
        "nota": "dice 22 'con la orientación solicitada' pero usa 1400 mm a lo largo; con 1200 mm a lo largo son 13",
    },
    {
        "consulta": "Cada pallet mide 150 mm de alto. ¿Cuántos pallets caben en la rampla?",
        "f1": 0.29,
        "correccion_factual": "si",
        "completitud": "si",
        "contradiccion": "no",
        "nota": "cero pallets porque 2644 mm pasa los 2599 mm; correcto",
    },
    {
        "consulta": "Cada pallet mide 120 mm de alto. ¿Caben bajo el techo?",
        "f1": 0.29,
        "correccion_factual": "si",
        "completitud": "si",
        "contradiccion": "no",
        "nota": "2614 mm no cabe bajo 2599 mm; correcto",
    },
    {
        "consulta": "Cada pallet mide 100 mm de alto. ¿Cuántos pallets caben en la rampla sin apilar?",
        "f1": 0.35,
        "correccion_factual": "no",
        "completitud": "si",
        "contradiccion": "no",
        "nota": "dice que caben 13 (o 11) en una sola fila y lo llama 'distribución óptima validada'; caben 22. Es el f1 más alto de los 25",
    },
]

with open(
    "docs/revision_manual.json", "w", encoding="utf-8"
) as archivo:
    json.dump(revision_manual, archivo, indent=2, ensure_ascii=False)

print(f"Guardados {len(revision_manual)} casos en docs/revision_manual.json")
