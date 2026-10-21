import consumir_gemini
import time
import statistics

def evaluar_modelos(pregunta,modelo, precio_entrada, precio_salida):
    numero_pruebas = 3
    latencia_total = []
    costo_total = []

    for i in range(numero_pruebas):
        try:
            url, body = consumir_gemini.armar_peticion_evaluacion(
                pregunta,modelo
            )

            inicio = time.perf_counter() #Empezar el contador

            datos, seg = consumir_gemini.enviar_peticion(
                url, body
            )

            fin = time.perf_counter() #Termina el contador

            latencia = fin - inicio

            costo = consumir_gemini.calcular_costo(
                datos, precio_entrada, precio_salida
            )

            resultado = consumir_gemini.extraer_datos(datos)

            latencia_total.append(latencia)
            costo_total.append(costo)
            
            print(f"\nModelo: {modelo} | Prueba: {i + 1}")
            print(f"Latencia: {latencia:.3f} segundos")
            print(f"Costo: ${costo:.8f} USD")
            print(f"Respuesta: {resultado}")

        except (ValueError, RuntimeError) as error:
            print(f"Error en {modelo}, prueba {i + 1}: {error}")
    
    if not latencia_total:
        return {
            "modelo": modelo,
            "pruebas_exitosas": 0,
            "latencia_promedio": None,
            "latencia_mediana": None,
            "costo_promedio": None,
            "costo_total": None
        }

    return {
        "modelo": modelo,
        "pruebas_exitosas": len(latencia_total),
        "latencia_promedio": statistics.mean(latencia_total),
        "latencia_mediana": statistics.median(latencia_total),
        "costo_promedio": statistics.mean(costo_total),
        "costo_total": sum(costo_total)
    }

modelos = [
    {
        "modelo": "gemini-3.6-flash",
        "precio_entrada": 0.00000075,
        "precio_salida": 0.00000375
    },
    {
        "modelo": "gemini-3.5-flash-lite",
        "precio_entrada": 0.00000030,
        "precio_salida": 0.00000250
    },
    {
        "modelo": "gemini-3.8-flash",
        "precio_entrada": 0.00000075,
        "precio_salida": 0.00000375
    },
]

prompt = """
Actúa como un especialista en logística y optimización de carga de camiones.

Determina cuántas unidades de un producto pueden cargarse dentro de un camión, considerando sus dimensiones y peso.

DATOS DEL CAMIÓN:
- Largo interior: 6000 mm
- Ancho interior: 2400 mm
- Alto interior: 2400 mm
- Capacidad máxima de carga: 8000 kg

DATOS DEL PRODUCTO:
- Largo: 400 mm
- Ancho: 300 mm
- Alto: 250 mm
- Peso por unidad: 12 kg

RESTRICCIONES:
1. Los productos deben permanecer completamente dentro del camión.
2. Se permite rotar los productos en cualquiera de sus tres ejes.
3. Los productos no pueden superponerse ni sobresalir del camión.
4. Debes respetar las dimensiones y el peso máximo permitido.
5. Determina cuántas unidades pueden cargarse físicamente.
6. No confundas el límite teórico por volumen con una distribución físicamente factible.
7. No inventes datos ni afirmes que una distribución es óptima si no puedes demostrarlo.

Responde únicamente con un string en español que indique la cantidad máxima estimada de unidades que caben en el camión, el peso total y una explicación breve del cálculo.

No utilices JSON, listas, encabezados, Markdown ni texto adicional fuera de la respuesta solicitada.
"""
resultados = []

for modelo in modelos:
    resultado = evaluar_modelos(
        prompt,
        modelo["modelo"],
        modelo["precio_entrada"],
        modelo["precio_salida"]
    )

    resultados.append(resultado)

print("\n===== RESUMEN COMPARATIVO =====")

for resultado in resultados:
    print(resultado)