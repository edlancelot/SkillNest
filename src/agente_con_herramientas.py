from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool #Herramientas
from langchain_classic.agents import (
    AgentExecutor,
    create_tool_calling_agent
)
from langchain_core.prompts import (
    ChatPromptTemplate, #Me permite agregar system_instructions y user(human)
    MessagesPlaceholder
)

load_dotenv()

modelo = ChatGoogleGenerativeAI(model="gemini-3.6-flash")

#Tool/Herramienta es una funcion común de python. Descripción en lenguaje natural será lo que el modelo lea (prompt) para decidir si elige
# o no esta herramienta
@tool
def buscar_en_documentacion(consulta:str)-> str:
    """
    Buscar información relevante de la documentación interna del producto.
    Usar cuando la pregunta es soblre cómo funciona algo del sistema.
    """
    documentacion = {
        "reintentos": "El cliente reintenta hasta 3 veces ante un TimeoutError, con espera creciente",
        "costos": "El costo se calcula a partir de totalTokenCount, segun la tarifa vigente."
    }

    for clave, texto in documentacion.items():
        if clave in consulta.lower():
            return texto
    return "No se encontró información dobre esa conslta en la documentación."

@tool
def calcular(expresion: str) -> str:
    """
    Evalúa una expresión aritmética simple, como '350 + 250'.
    Usar cuando la pregunta requiere un calculo númerico.
    """
    permitido = set("0123456789+-*/().")
    if not set(expresion)<= permitido:
        return "expresión no permitida."
    try:
        return str(eval(expresion))
    except Exception as e:
        return f"Error al evaluar: {e}"

herramientas = [buscar_en_documentacion, calcular] #Lista de herramientas

#Plantilla, con system_instructions
prompt_agente = ChatPromptTemplate.from_messages([
    (
        "system", "Eres un asistente que responde solamente utilizando las herramientas disponibles cuando lo necesites, no inventes, no inventes información."
    ),
    (
        "human", "{entrada}"
    ),
    MessagesPlaceholder("agent_scratchpad") #El espacio donde langChain va anotando, pasos/ciclos razonar-actuar-observar, que herramientas 
    #Llamó y que devolvieron
])

#Agente: modelo, herramientas, prompt, formato

agente = create_tool_calling_agent(
    modelo,
    herramientas,
    prompt_agente
)

#Orquestador: es el que controla el ciclo entre razonar-actuar-observar
ejecutor_agente = AgentExecutor(
    agent=agente,
    tools=herramientas,
    verbose=True, #Imprime los pasos que va siguiendo
)

resultado = ejecutor_agente.invoke(
    {"entrada": "¿Que es langchain?"}
)

print("Respuesta Final:", resultado["output"][0]["text"])