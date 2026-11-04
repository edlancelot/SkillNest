from collections import Counter
from src.pipeline_limpieza import procesar_texto
from src.cliente import consultar_modelo
import json


def contar_coincidencias(
    tokens_referencia: list[str],
    tokens_respuesta: list[str],
) -> int:
    """Cuenta las coincidencias entre referencia y respuesta."""
    conteo_referencia = Counter(tokens_referencia)
    conteo_respuesta = Counter(tokens_respuesta)
    interseccion = conteo_referencia & conteo_respuesta
    return sum(interseccion.values())

def calcular_precision_cobertura_f1(
    tokens_referencia: list[str],
    tokens_respuesta: list[str],
) -> dict[str, float]:
    """Calcula precisión, cobertura y F1 de dos listas de tokens."""
    coincidencias = contar_coincidencias(
        tokens_referencia, tokens_respuesta
    )

    if not tokens_respuesta or not tokens_referencia:
        return {"precision": 0.0, "cobertura": 0.0, "f1": 0.0}

    precision = coincidencias / len(tokens_respuesta)
    cobertura = coincidencias / len(tokens_referencia)

    if precision + cobertura == 0:
        f1 = 0.0
    else:
        f1 = 2 * precision * cobertura / (precision + cobertura)

    resultado = {
        "precision": precision,
        "cobertura": cobertura,
        "f1": f1,
    }

    return resultado

def calcular_metricas(texto_referencia, texto_respuesta):
    tokens_referencia = procesar_texto(texto_referencia)
    tokens_respuesta = procesar_texto(texto_respuesta)

    return calcular_precision_cobertura_f1(
        tokens_referencia, tokens_respuesta
    )

casos = [
    (
        "Cada pallet mide 100 mm de alto. ¿Cuántos pallets caben en la rampla sin apilar?",
        "Caben 22 pallets: 11 filas de 2 pallets, con el pallet de 1400 mm a lo largo y 1200 mm a lo ancho; la altura total es 2594 mm.",
    ),
    (
        "Cada pallet mide 150 mm de alto. ¿Cuántos pallets caben en la rampla?",
        "No caben pallets: la altura total es 2644 mm y supera los 2599 mm de alto de la rampla.",
    ),
    (
        "¿Cuántos pallets caben en la rampla?",
        "Falta la altura del pallet; se debe solicitar ese dato antes de calcular la capacidad vertical.",
    ),
    (
        "¿Cuántas filas caben a lo largo si el pallet va con 1400 mm en el sentido del largo?",
        "Caben 11 filas, que ocupan 15400 mm de los 15685 mm de largo.",
    ),
    (
        "¿Cuántos pallets caben si se orientan con 1200 mm en el sentido del largo, sin apilar?",
        "Caben 13 filas de 1 pallet, es decir 13 pallets, porque dos pallets de 1400 mm suman 2800 mm y superan el ancho de 2507 mm.",
    ),
    (
        "¿Cuánto largo sobra con 11 filas de pallets de 1400 mm?",
        "Sobran 285 mm de largo, porque 11 filas ocupan 15400 mm de 15685 mm.",
    ),
    (
        "¿Cuánto ancho sobra con dos pallets de 1200 mm de ancho en la rampla?",
        "Sobran 107 mm de ancho, porque dos pallets ocupan 2400 mm de 2507 mm.",
    ),
    (
        "Autorizo apilar. Cada pallet mide 100 mm de alto. ¿Se puede poner una segunda capa?",
        "No se puede: una capa mide 2594 mm de alto y dos capas superarían los 2599 mm de la rampla.",
    ),
    (
        "¿Cuántos pallets caben en una fila a lo ancho?",
        "Caben 2 pallets a lo ancho con 1200 mm cada uno, y sobran 107 mm.",
    ),
    (
        "¿Cuál es el área del piso de la rampla y cuántos pallets da como límite teórico?",
        "El piso mide 39322295 mm2 y cada pallet ocupa 1680000 mm2, así que el límite teórico por área es 23 pallets.",
    ),
    (
        "¿Es posible cargar 23 pallets si el límite por área es 23?",
        "No, el límite por área es solo teórico: la distribución física validada permite 22 pallets.",
    ),
    (
        "Con pallets de 100 mm de alto, ¿cuánta altura libre queda bajo el techo?",
        "Quedan 5 mm de holgura, porque la altura total de 2594 mm se compara con 2599 mm.",
    ),
    (
        "¿Cabe el producto de 2494 mm de alto en la rampla sin considerar el pallet?",
        "El producto cabe con 105 mm de margen, pero ese margen debe cubrir la altura del pallet.",
    ),
    (
        "¿Cuál es la altura máxima de pallet permitida?",
        "La altura máxima del pallet es 105 mm, porque 2599 menos 2494 deja 105 mm de margen.",
    ),
    (
        "Cada pallet mide 120 mm de alto. ¿Caben bajo el techo?",
        "No caben: la altura total es 2614 mm y excede en 15 mm los 2599 mm de la rampla.",
    ),
    (
        "¿Se pueden apilar dos pallets con producto de 2494 mm?",
        "No, no se debe apilar sin autorización y además dos niveles de 2494 mm superarían los 2599 mm de alto.",
    ),
    (
        "¿Cuántos pallets caben a lo ancho si el lado de 1400 mm va atravesado?",
        "Cabe 1 pallet a lo ancho, y sobran 1107 mm de ancho sin poder aprovecharlos.",
    ),
    (
        "Con pallets de 100 mm de alto, ¿caben 20 pallets?",
        "Sí, 20 pallets caben porque el máximo es 22, distribuidos en 10 filas de 2 pallets.",
    ),
    (
        "Con pallets de 100 mm de alto, ¿caben 24 pallets?",
        "No, 24 pallets no caben: el máximo es 22 pallets.",
    ),
    (
        "¿Cuánto largo ocupan 11 filas de pallets de 1400 mm?",
        "Ocupan 15400 mm de largo.",
    ),
    (
        "¿Cuántos pallets hay en 5 filas de 2 pallets?",
        "En 5 filas de 2 pallets hay 10 pallets.",
    ),
    (
        "¿Cuál es el peso máximo que soporta la rampla?",
        "No se conoce el peso máximo ni el peso de cada pallet; se debe solicitar ese dato.",
    ),
    (
        "¿Qué porcentaje del piso ocupan 22 pallets?",
        "22 pallets ocupan 36960000 mm2, cerca del 94 por ciento del piso de la rampla.",
    ),
    (
        "¿Esta estimación de 22 pallets es una distribución físicamente validada?",
        "No, es una estimación geométrica; no considera peso, estiba real ni holguras de maniobra.",
    ),
    (
        "Con pallets de 100 mm, ¿cuál es la altura total de pallet más producto?",
        "La altura total es 2594 mm, que cabe en los 2599 mm de la rampla.",
    ),
]

SYSTEM_INSTRUCTION = (
    "Eres un especialista en logística y optimización de carga de camiones. "
    "Tu tarea es calcular la cantidad máxima de pallets que caben dentro de una rampla, "
    "considerando sus dimensiones interiores, las dimensiones de los pallets y las restricciones físicas de carga. "
    "Todas las medidas deben manejarse en milímetros. "
    "Rampla: largo 15685 mm, ancho 2507 mm y alto 2599 mm. "
    "Cada pallet tiene una base de 1400 mm de largo por 1200 mm de ancho y contiene un producto de 2494 mm de alto. "
    "No asumas que la altura del producto incluye el pallet: si no se conoce la altura del pallet, "
    "solicita ese dato antes de calcular la capacidad vertical. "
    "Evalúa las posibles orientaciones de los pallets en el piso de la rampla, respetando sus dimensiones y "
    "sin permitir superposiciones, salientes ni ubicaciones físicamente imposibles. "
    "Considera la altura total del producto más el pallet para verificar que la carga quepa bajo el techo. "
    "No permitas apilar pallets salvo que el usuario lo autorice expresamente. "
    "Entrega la cantidad máxima estimada de pallets, la distribución propuesta a lo largo y ancho de la rampla, "
    "los cálculos utilizados y las restricciones detectadas. "
    "Distingue entre una estimación geométrica y una distribución físicamente validada. "
    "No inventes datos faltantes; solicita aclaraciones cuando sean necesarias. "
    "Responde en español, en máximo tres oraciones, sin listas ni Markdown."
)

resultados = []

for consulta, referencia in casos:
    respuesta = consultar_modelo(consulta, system_instruction=SYSTEM_INSTRUCTION)

    metricas = calcular_metricas(referencia, respuesta)

    print("Consulta:", consulta)
    print("Respuesta:", respuesta)
    print("Métricas:", metricas)

    resultados.append({
        "consulta": consulta,
        "respuesta": respuesta,
        **metricas,
    })

    resultados=sorted(resultados, key=lambda r: r["f1"])
    
with open(
    "docs/resultados_metricas.json", "w", encoding="utf-8"
) as archivo:
    json.dump(resultados, archivo, indent=2, ensure_ascii=False)

def resumir_metricas(resultados):

    if not resultados:
        return {
            "precision_promedio": 0,
            "cobertura_promedio": 0,
            "f1_promedio": 0,
        }
    n = len(resultados)

    return {
        "precision_promedio": sum(
            r["precision"] for r in resultados
        ) / n,
        "cobertura_promedio": sum(
            r["cobertura"] for r in resultados
        ) / n,
        "f1_promedio": sum(r["f1"] for r in resultados) / n,
    }

print("Promedios")
print(resumir_metricas(resultados))

peores_casos = sorted(resultados, key=lambda r: r["f1"])

for caso in peores_casos[:3]:
    print(caso["consulta"], caso["f1"])
# referencia = procesar_texto(
#     "Python es un lenguaje de programación interpretado."
# )

# texto_respuesta = consultar_modelo("¿Qué es Python?",
#                                    system_instruction="Responde en español con una definición breve, en una sola oración de máximo 15 palabras. Sin listas, ejemplos ni introducciones.")

# respuesta = procesar_texto(texto_respuesta)
# resultado = calcular_precision_cobertura_f1(referencia, respuesta)

# print("Respuesta:", texto_respuesta)
# print("Tokens de referencia:", len(referencia))
# print("Tokens de respuesta:", len(respuesta))
# print(resultado)