import json
import time
from prompts.banco import BANCO_DE_PROMPTS
from consumir_gemini import armar_peticion_evaluacion, enviar_peticion, extraer_datos, parsear_respuesta_json

registro = {}

try:
    for prompt in BANCO_DE_PROMPTS:
        exitos = 0
        intentos = 3
        for intento in range(intentos):
            url, body = armar_peticion_evaluacion(
                prompt["ejemplo_usuario"], 
                "gemini-3.5-flash-lite",
                prompt["system_instruction"], 
                prompt["response_schema"]
            )

            _result = enviar_peticion(url, body)

            _texto = extraer_datos(_result)
            try:
                datos = parsear_respuesta_json(_texto, prompt["claves_esperadas"])
                exitos += 1
                print(f"Respuesta: {datos}")
            except ValueError as error:
                print(f"Intento {intento + 1} falló: {error}")
            time.sleep(1)
        print(f"{prompt["nombre"]}: {exitos}/{intentos} respuestas validas")
        registro[prompt["nombre"]] = {"exitos": exitos, "intentos": intentos}
    with open("src/prompts/registro_resultados.json", "w", encoding="utf-8") as archivo:
        json.dump(registro, archivo, indent=2, ensure_ascii=False)



except (ValueError, RuntimeError) as error:
    print("No se pudo completar la operacion: ", error)

