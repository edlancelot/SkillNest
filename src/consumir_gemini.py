import os
import requests
from dotenv import load_dotenv

load_dotenv()

MODELO="gemini-3.6-flash"
URL_BASE="https://generativelanguage.googleapis.com/v1beta/models/"
API_KEY=os.getenv("GEMINI_API_KEY")

#Función para crear la solicitud
def armar_peticion(pregunta):
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

#Función envia la petición
def enviar_peticion(url, body):
    respuesta = requests.post(url, json=body)
    return respuesta.json()

#Función para extraer los datos
def extraer_datos(datos):
    return "Respuesta:" + datos["candidates"][0]["content"]["parts"][0]["text"]

def obtener_dato_de_prueba(pregunta):
    url, body= armar_peticion(pregunta)
    datos = enviar_peticion(url, body)

    return extraer_datos(datos)

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

print(obtener_dato_de_prueba("Confirma el estado de la conexión en 10 palabra."))