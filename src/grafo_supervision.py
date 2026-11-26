from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt, Command
 
class EstadoDespliegue(TypedDict):
	huella_nueva: str
	aprobado: bool
 
def proponer(estado: EstadoDespliegue):
	return {}
 
def supervisar(estado: EstadoDespliegue):
	decision = interrupt({
    	"motivo": "aprobar nueva version de prompt en produccion",
    	"huella_propuesta": estado["huella_nueva"],
	})
	return {"aprobado": decision}
 
def aplicar(estado: EstadoDespliegue):
    if estado["aprobado"]:
        print("version", estado["huella_nueva"], "activada")
    else:
        print("version", estado["huella_nueva"], "rechazada, se mantiene la anterior")
    return {}
 
grafo = StateGraph(EstadoDespliegue)
grafo.add_node("proponer", proponer)
grafo.add_node("supervisar", supervisar)
grafo.add_node("aplicar", aplicar)
grafo.add_edge(START, "proponer")
grafo.add_edge("proponer", "supervisar")
grafo.add_edge("supervisar", "aplicar")
grafo.add_edge("aplicar", END)
 
app_despliegue = grafo.compile(checkpointer=InMemorySaver())
config = {"configurable": {"thread_id": "mi-despliegue-1"}}
huella = "ba2bcb4f4f13"  # la huella del ejemplo del Paso 1; usa la de tu propio registro
 
config_ej = {"configurable": {"thread_id": "ejemplo-1"}}
resultado = app_despliegue.invoke({"huella_nueva": huella, "aprobado": False}, config=config_ej)
print("1) tras invocar:", resultado)
print("2) pendiente:", app_despliegue.get_state(config_ej).interrupts[0].value)
resultado = app_despliegue.invoke(Command(resume=True), config=config_ej)
print("3) tras aprobar:", resultado)
 
config_ej2 = {"configurable": {"thread_id": "ejemplo-2"}}
app_despliegue.invoke({"huella_nueva": huella, "aprobado": False}, config=config_ej2)
resultado = app_despliegue.invoke(Command(resume=False), config=config_ej2)
print("4) tras rechazar:", resultado)