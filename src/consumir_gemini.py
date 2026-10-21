import os
import requests
from dotenv import load_dotenv

import time

load_dotenv()

MODELO="gemini-3.8-flash"
URL_BASE="https://generativelanguage.googleapis.com/v1beta/models/"
API_KEY=os.getenv("GEMINI_API_KEY")

#Función para crear la solicitud
def armar_peticion(pregunta):
    if not pregunta:
        raise ValueError(f"La pregunta no puede estar vacia.") 
    url= f"{URL_BASE}{MODELO}:generateContent?key={API_KEY}"
    body={
        "contents": [
            {
                "parts": [
                    {
                        "text": pregunta
                    }
                ]
            }
        ]
    }

    return url,body

#Función para crear la solicitud
def armar_peticion_evaluacion(pregunta, modelo, system_instructions):
    if not pregunta:
        raise ValueError(f"La pregunta no puede estar vacia.") 
    url= f"{URL_BASE}{modelo}:generateContent?key={API_KEY}"
    body={
        "systemInstruction":{
            "parts": [
                {
                    "text": system_instructions
                }
            ]
        },
        "contents": [
            {
                "parts": [
                    {
                        "text": pregunta
                    }
                ]
            }
        ]
    }

    return url,body

#def enviar_peticion(url: str, body: dic )
def enviar_peticion(url, body):
    try:
        respuesta = requests.post(url, json=body, timeout=30)
    except requests.exceptions.ConnectionError:
        raise RuntimeError("No se puede conectar con el servicio. Intenta de nuevo en unos momentos.")
    except requests.exceptions.Timeout:
        raise RuntimeError("Se agoto el tiempo. Intenta de nuevo en unos momentos.")

    if respuesta.status_code != 200:
        raise RuntimeError(f"Error en la petición, Status Code: {respuesta.status_code}")
    
    try:
        return respuesta.json(), respuesta.elapsed.total_seconds()
    except requests.exceptions.JSONDecodeError:
        raise RuntimeError("La respuesta del servicio no llegó en el formato esperado.")

#def extraer_datos(datos: dic)
def extraer_datos(datos):
    try:
        return "Respuesta:" + datos["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        raise RuntimeError("La respuesta no recibe el texto generado en el lugar definido.")

def obtener_dato_de_prueba(pregunta):
    system_instructions="Eres un asistente agresivo y respondes en máximo 2 oraciones."
    # url, body= armar_peticion(pregunta,"gemini-3.6-flash",system_instructions)
    url, body= armar_peticion_evaluacion(pregunta,"gemini-3.8-flash",system_instructions)

    inicio = time.perf_counter() #Empezar el contador

    datos, seg = enviar_peticion(url, body)

    fin = time.perf_counter() #Termina el contador
    latencia = fin - inicio

    costo = calcular_costo(datos, 0.00000075, 0.00000375)
    print(f"Latencia Time: {latencia:.2f} segundos")
    print(f"Latencia Requests: {seg:.3f} segundos")
    print(f"Costo de la petición: ${costo:.6f} USD")
    return extraer_datos(datos)

#def calcular_costo(datos: dic, precio_entrada float, precio_salida: float) ->float
def calcular_costo(datos, precio_entrada, precio_salida):
    #datos ={dict... usageMetadata}
    try:
        uso = datos["usageMetadata"]

        # uso = {
        #     "promptTokenCount": 12,
        #     "candidatesTokenCount": 682,
        #     "totalTokenCount": 1583,
        #     "promptTokensDetails": [
        #         {
        #             "modality": "TEXT",
        #             "tokenCount": 12
        #         }
        #     ],
        #     "thoughtsTokenCount": 889,
        #     "serviceTier": "standard"
        # }

        tokens_entrada = uso["promptTokenCount"]
        tokens_salida = uso["candidatesTokenCount"]
        tokens_razonamiento = uso.get("thoughtsTokenCount", 0)

        costo = (tokens_entrada * precio_entrada) + ( 
            (tokens_salida + tokens_razonamiento) * precio_salida )

        return costo
    except KeyError:
        raise RuntimeError("La respuesta no recibe el texto generado en el lugar definido.")


try:
    print(obtener_dato_de_prueba("Confirma la conexion"))
except (ValueError, RuntimeError) as error:
    print(f"No se pudo completar la operación: {error}")

# def obtener_dato_de_prueba(pregunta):
#     try:
#         api_key=os.getenv("GEMINI_API_KEY")
#         modelo = "gemini-flash-latest"

#         url= f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent?key={api_key}"

#         body={
#             "contents": [
#                 {
#                     "parts": [
#                         {
#                             "text": pregunta
#                         }
#                     ]
#                 }
#             ]
#         }

#         respuesta=requests.post(url,json=body)
#         datos= respuesta.json()

#         return "Respuesta:" + datos["candidates"][0]["content"]["parts"][0]["text"]
#     except Exception as e:
#         return print(f"Ocurrio un error: {e}")