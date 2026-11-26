def puntaje_riesgo(probabilidad, impacto):
    return probabilidad * impacto


def categoria_riesgo(puntaje):
    if puntaje >= 15:
        return "CRITICO"
    if puntaje >= 9:
        return "ALTO"
    if puntaje >= 4:
        return "MEDIO"
    return "BAJO"


mis_riesgos = [
	# Fila modelo: quita los # para ver el resultado y luego reemplaza la fila por un riesgo de tu proyecto.
	# {"riesgo": "Inyeccion de prompt via comentario de usuario indexado",
	#  "probabilidad": 4,   # 1 a 5: probable, con la informacion que tienes hoy
	#  "impacto": 4,    	# 1 a 5: expone instrucciones internas y datos de clientes
	#  "mitigacion": "Filtro de patrones + delimitacion de contexto (Bloque 31)"},
	# Tus otras filas aqui, con la misma estructura (cinco como minimo)
    {"riesgo": "El modelo calcula mal las unidades y asigna una carga que excede el peso maximo del camion",
     "probabilidad": 3,   # 3.8-flash acerto 3/3, pero la muestra es chica y flash-lite fallo 3/3
     "impacto": 5,        # camion sobrecargado: riesgo de seguridad, multas y dano a la carga
     "mitigacion": "Validacion deterministica en codigo (unidades * peso <= capacidad y volumen) antes de despachar"},
    {"riesgo": "Datos de entrada erroneos (dimensiones o peso mal ingresados, mm confundidos con cm)",
     "probabilidad": 3,   # los datos los ingresa una persona; sin validacion de esquema hoy
     "impacto": 4,        # el modelo calcula bien sobre datos malos y la asignacion queda incorrecta
     "mitigacion": "Validar tipos, unidades y rangos razonables antes de enviar la consulta al modelo"},
    {"riesgo": "El modelo propone una distribucion que no es fisicamente factible (estiba, reparto de peso por eje)",
     "probabilidad": 3,   # el prompt pide no confundir limite por volumen con distribucion factible
     "impacto": 4,        # la carga no cabe o queda mal balanceada al momento de cargar
     "mitigacion": "Tratar la respuesta como estimacion y confirmar con el plan de carga del jefe de bodega"},
    {"riesgo": "Servicio del modelo no disponible (error 503 por sobrecarga)",
     "probabilidad": 3,   # gemini-3.6-flash fallo 2 de 3 pruebas con 503
     "impacto": 3,        # se detiene la asignacion y el despacho espera
     "mitigacion": "Reintentos con espera exponencial y procedimiento manual de respaldo"},
    {"riesgo": "Respuesta en texto libre que no se puede interpretar de forma automatica",
     "probabilidad": 3,   # el prompt pide un string en espanol sin formato fijo
     "impacto": 3,        # el sistema no puede extraer unidades y peso para asignar
     "mitigacion": "Salida estructurada (JSON con unidades y peso_total) y validacion del esquema"},
    {"riesgo": "Inyeccion de prompt en campos de texto libre (descripcion del producto o del camion)",
     "probabilidad": 2,   # usuarios internos, pero los campos de texto llegan sin filtro al prompt
     "impacto": 4,        # puede alterar el calculo o saltarse las restricciones del prompt
     "mitigacion": "Filtro de patrones y delimitacion de datos del usuario (prevencion_prompt_inyection.py)"},
    {"riesgo": "Latencia alta (~10 s por consulta) que retrasa la operacion en horas punta",
     "probabilidad": 4,   # promedio medido de 10.0 s con gemini-3.8-flash
     "impacto": 2,        # molesta y retrasa, pero no produce una asignacion incorrecta
     "mitigacion": "Cache de combinaciones camion/producto repetidas y timeout con aviso al usuario"},
    {"riesgo": "Costo por peticion crece con el volumen de despachos",
     "probabilidad": 2,   # ~$0.0047 por peticion; bajo con el volumen actual
     "impacto": 2,        # afecta presupuesto, no la operacion
     "mitigacion": "Monitorear tokens y costo por peticion (logs_rag.py) y fijar un tope mensual"},
]

for r in mis_riesgos:
    r["puntaje"] = puntaje_riesgo(r["probabilidad"], r["impacto"])
    r["categoria"] = categoria_riesgo(r["puntaje"])

for r in sorted(mis_riesgos, key=lambda x: -x["puntaje"]):
    print(f"{r['categoria']:8} ({r['puntaje']:2}) - {r['riesgo']}")


def esta_en_el_limite(probabilidad, impacto):
    categoria_actual = categoria_riesgo(puntaje_riesgo(probabilidad, impacto))
    vecinos = [
        (probabilidad + 1, impacto), (probabilidad - 1, impacto),
        (probabilidad, impacto + 1), (probabilidad, impacto - 1),
    ]
    for p2, i2 in vecinos:
        if not (1 <= p2 <= 5 and 1 <= i2 <= 5):
            continue
        if categoria_riesgo(puntaje_riesgo(p2, i2)) != categoria_actual:
            return True
    return False


for r in mis_riesgos:
    r["al_limite"] = esta_en_el_limite(r["probabilidad"], r["impacto"])
    if r["al_limite"]:
        print("revisar con otra persona:", r["riesgo"])
