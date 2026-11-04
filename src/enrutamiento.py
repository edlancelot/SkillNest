from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI #modelo
from langchain_core.prompts import  PromptTemplate #Plantilla -> Prompt dinámico
from langchain_core.output_parsers import StrOutputParser #Parsea la respuesta y la transforma en solo textos
from langchain_core.runnables import (RunnableBranch, RunnablePassthrough) #Bifurcaciones/Ramificaciones

load_dotenv()

modelo = ChatGoogleGenerativeAI(model="gemini-3.6-flash")

plantilla_clasificacion = PromptTemplate.from_template(
    "Clasifica el siguiente mensaje de soporte en una sola palabra:"
    "pregunta, queja o sugerencia. Responde solo con esa palabra. \n\n {mensaje}"
)

paso_clasificacion = (
    plantilla_clasificacion
    | modelo
    | StrOutputParser()
    | (lambda texto: texto.strip().lower())
)

# mensaje_prueba = "Dame el nombre de tu creador."

# clasificacion = paso_clasificacion.invoke(
#     {"mensaje": mensaje_prueba}
# )

# print(clasificacion)

cadena_pregunta = (
    PromptTemplate.from_template("Responde esta pregunta técnica con precisión: \n\n {mensaje}")
    | modelo
    | StrOutputParser()
)

cadena_queja = (
    PromptTemplate.from_template("Responde esta queja con empatia, reconociendo el problema antes de ofrecer una solución: \n\n {mensaje}")
    | modelo
    | StrOutputParser()
)

cadena_sugerencia = (
    PromptTemplate.from_template("Agradece esta sugerencia y explica cómo se evaluara dentro del producto: \n\n {mensaje}")
    | modelo
    |StrOutputParser()
)

# Sintaxis RunnableBranch
# caminos = RunnableBranch(
#     {condicion_1, rama_1}, #if
#     {condicion_2, rama_2}, #elseif
#     {condicion_3, rama_3}, #elseif
#     rama_por_defecto #else
# ) #Cada condicion debe ser una función: sele ser un lambda

# = {"clasificacion": "queja", "mensaje": "Mi teléfono no funciona."}
bifurcacion = RunnableBranch(
    (lambda x: x["clasificacion"] == "queja", cadena_queja), #if x["clasificacion"] == "queja" -> cadena_queja
    (lambda x: x["clasificacion"] == "sugerencia", cadena_sugerencia), #elseif x["clasificacion"] == "sugerencia": cadena_sugerencia
    cadena_pregunta #else: cadena_pregunta
)

#cadena_con_enrutamiento, RunnablePAssthrough
cadena_con_enrutamiento = (
    #Ejecutar paso_clasificacion, obtener la respuesta como clasificacion y tambien conservar el mensaje original
    RunnablePassthrough.assign(clasificacion=paso_clasificacion) #{"mensaje": "Deberian tener mas agentes disponibles."}
    #"clasificacion":resultado de paso_clasificacion}
    | bifurcacion
)

resultado = cadena_con_enrutamiento.invoke(
    {"mensaje": "Deberia de tener mas agentes disponibles."}
)

print(resultado)

# Entrada inicial: {"mensaje":"Deberia de tener mas agentes disponibles." }
#-------------------------
#-------------------------
# RunnablePassthrough
#   1: Pasa el mensaje a paso clasificacion -> return "sugerencia o queja o pregunta"
#   2: Fusiono clasificacion y mensaje
#   3: return {"mensaje":"Deberia de tener mas agentes disponibles.","clasificacion": "sugerencia, queja o pregunta"}
#-------------------------
#-------------------------
# bifurcacion(RunnableBlanch)
#   ¿clasificacion == "queja"? NO
#   ¿clasificacion == "sugerencia" SI
#       Entra a la cadena_sugerencia
#       cadena_sugerencia.invoqke({"mensaje":"Deberia de tener mas agentes disponibles.","clasificacion": "sugerencia, queja o pregunta")