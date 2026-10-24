import os
import requests
from dotenv import load_dotenv
import re
import json

import time

load_dotenv()

MODELO="gemini-3.5-flash-lite"
URL_BASE="https://generativelanguage.googleapis.com/v1beta/models/"
API_KEY=os.getenv("GEMINI_API_KEY")

#Función armar_peticion(pregunta: str)
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

#def armar_peticion_evaluacion(pregunta: str, modelo: str, system_instructions: str, response_schema: dic )
def armar_peticion_evaluacion(pregunta, modelo, system_instructions,response_schema=None):
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

    if response_schema is not None:
        body["generationConfig"] ={
            "responseMimeType": "application/json",
            "responseSchema": response_schema
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


    if respuesta.status_code in(401, 403):
        raise ValueError("Credencial invalida o sin permiso. Revisa tu GEMINI_API_KEY.")
    if respuesta.status_code >= 500:
        raise TimeoutError("El proveedor no pudo procesar la peticion. Hay que esperar y reintentar.")
    if respuesta.status_code == 429:
        segundos = respuesta.headers.get("Retry-After")
        mensaje = f"Límite excedido. Reintente en {segundos}s." if segundos else "Límite excedido."
        raise TimeoutError(mensaje)

    if respuesta.status_code != 200:
        raise RuntimeError(f"Error en la petición, Status Code: {respuesta.status_code}")
    
    try:
        return respuesta.json()
    except requests.exceptions.JSONDecodeError:
        raise RuntimeError("La respuesta del servicio no llegó en el formato esperado.")

#def extraer_datos(datos: dic)
def extraer_datos(datos):
    try:
        return datos["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        raise RuntimeError("La respuesta no recibe el texto generado en el lugar definido.")

def obtener_dato_de_prueba(pregunta):

    response_schema = {
        "type": "OBJECT",
        "properties": {
            "categoria": {"type": "STRING"},
            "confianza": {"type": "NUMBER"} 
        },
        "required": ["categoria","confianza"] #obligatorios
    }

    system_instructions="Eres un asistente agresivo y respondes en máximo 2 oraciones, tambien responde con un objeto de JSON con claves: 'categoria' y 'confianza'"
    # url, body= armar_peticion(pregunta,"gemini-3.5-flash-lite",system_instructions)
    url, body= armar_peticion_evaluacion(pregunta,"gemini-3.5-flash-lite",system_instructions, response_schema)

    inicio = time.perf_counter() #Empezar el contador

    datos = enviar_peticion(url, body)

    fin = time.perf_counter() #Termina el contador
    latencia = fin - inicio

    costo = calcular_costo(datos, 0.00000075, 0.00000375)
    print(f"Latencia Time: {latencia:.2f} segundos")
    # print(f"Latencia Requests: {seg:.3f} segundos")
    print(f"Costo de la petición: ${costo:.6f} USD")

    texto = extraer_datos(datos)
    datos_formateados = parsear_respuesta_json(texto, ["categoria","confianza"])
    return datos_formateados
    # return extraer_datos(datos)

#def calcular_costo(datos: dic, precio_entrada float, precio_salida: float) ->float
def calcular_costo(datos, precio_entrada, precio_salida):
    #datos ={dict... usageMetadata}
    try:
        uso = datos["usageMetadata"]

        tokens_entrada = uso["promptTokenCount"]
        tokens_salida = uso["candidatesTokenCount"]
        tokens_razonamiento = uso.get("thoughtsTokenCount", 0)

        costo = (tokens_entrada * precio_entrada) + ( 
            (tokens_salida + tokens_razonamiento) * precio_salida )

        return costo
    except KeyError:
        raise RuntimeError("La respuesta no recibe el texto generado en el lugar definido.")

def parsear_respuesta_json(texto, claves_requeridas = None):
    """
    claves_requeridas = ["categoria","confianza"]
    """
    texto_limpio = texto.strip() #Quitar espacios
    texto_limpio = re.sub(r"^```(?:json)?\s*", "", texto_limpio) 
    texto_limpio = re.sub(r"\s*```$", "", texto_limpio)
    print(texto_limpio)
    try:
        datos = json.loads(texto_limpio)
    except json.JSONDecodeError:
        raise ValueError("La respuesta del modelo no es JSON válido.")

    if claves_requeridas:
        faltantes = [clave for clave in claves_requeridas if clave not in datos]
        if faltantes:
            raise ValueError("La respuesta no tiene la estructura esperada.")

    return datos

if __name__ == "__main__":
    try:
        for i in range(15):
            print(obtener_dato_de_prueba("Confirma la conexion"))
    except (ValueError, RuntimeError, TimeoutError) as error:
        print(f"No se pudo completar la operación: {error}")
