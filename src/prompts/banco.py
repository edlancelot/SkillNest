BANCO_DE_PROMPTS = [
    {
        "nombre": "clasificar_carga",
        "system_instruction": (
			"Clasifica la carga según su volumen en metros cúbicos. "
			"Si tiene hasta 2 m3, clasifícala como 'pequeña'. "
			"Si tiene más de 2 m3 y hasta 5 m3, clasifícala como 'mediana'. "
			"Si tiene más de 5 m3, clasifícala como 'grande'. "
			"Responde únicamente con un JSON con la clave 'categoria'."
        ),
        "ejemplo_usuario": (
            "La carga tiene un volumen de 5 m3."
        ),
        "claves_esperadas": ["categoria"],
        "response_schema": {
            "type": "OBJECT",
            "properties": {
                "categoria": {
                    "type": "STRING",
                    "enum": ["pequeña", "mediana", "grande"]
                }
            },
            "required": ["categoria"]
        },
    },
    {
        "nombre": "validar_capacidad_camion",
        "system_instruction": (
            "Determina si un camion tiene capacidad suficiente para "
            "transportar una carga. Compara el peso de la carga con "
            "la capacidad maxima del camion. Responde unicamente "
            "con un JSON con la clave 'capacidad_suficiente' "
            "de tipo booleano."
        ),
        "ejemplo_usuario": (
            "La carga pesa 8000 kg y el camion soporta un maximo "
            "de 10000 kg."
        ),
        "claves_esperadas": ["capacidad_suficiente"],
        "response_schema": {
            "type": "OBJECT",
            "properties": {
                "capacidad_suficiente": {
                    "type": "BOOLEAN"
                }
            },
            "required": ["capacidad_suficiente"]
        },
    },
    {
        "nombre": "asignar_anden",
        "system_instruction": (
            "Determina si un anden esta disponible para cargar un "
            "camion. Responde unicamente con un JSON con la clave "
            "'anden_asignado' de tipo booleano."
        ),
        "ejemplo_usuario": (
            "El anden 2 esta disponible y el camion se encuentra "
            "listo para cargar."
        ),
        "claves_esperadas": ["anden_asignado"],
        "response_schema": {
            "type": "OBJECT",
            "properties": {
                "anden_asignado": {
                    "type": "BOOLEAN"
                }
            },
            "required": ["anden_asignado"]
        },
    },
]