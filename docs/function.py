#El nombre de la estudiante
#La calificación del curso
#El titulo de la segunda tarea
#Si la primera tarea está completada
estudiante = {
    "nombre": "Ana",
    "edad": 24,
    "curso": {
        "nombre": "Python",
        "calificacion": 92
    },
    "tareas": [
        {
            "titulo": "Variables",
            "completada": True
        },
        {
            "titulo": "Consumo de APIs",
            "completada": False
        }
    ]
}

print("Nombre de la estudiante: " + estudiante["nombre"])
print("La calificación del curso: " + str(estudiante["curso"]["calificacion"]))
print("El titulo de la segunda tarea: " + estudiante["tareas"][1]["titulo"])
print("Si la primera tarea está completada: " + "Tarea Completada" if estudiante["tareas"][0]["completada"] else "Tarea no completada")