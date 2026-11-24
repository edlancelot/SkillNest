# Decision de personalizacion

## 1. El problema
El clasificador de errores no responde con un formato consistente: de 20 respuestas revisadas, 6 (30 %) no vinieron como JSON limpio con los campos "categoria" y "accion_sugerida" (venian envueltas en un bloque ```json). El contenido es correcto; lo que falla es la consistencia de la salida.

## 2. Resultado del metodo de decision
- PEFT: 2 puntos
- Fine-tuning completo: 1 puntos
- RAG: 0 puntos

## 3. Tecnica elegida y por que
Elijo PEFT. El puntaje dio un ganador claro (PEFT 2, fine-tuning completo 1, RAG 0) y además tiene sentido por costo. Al modelo no le falta información: sabe qué es cada error, y lo que falla es la consistencia del formato, que es justo lo que un adapter pequeño aprende sin reentrenar todos los parámetros. Descarto RAG porque los tipos de error y sus soluciones no cambian seguido. Descarto el fine-tuning completo porque pide un dataset mucho mayor que el que tengo (8 ejemplos) y reentrenar todo el modelo cuesta más en cómputo y tiempo.

## 4. Que necesitarias para ejecutarla
Tengo 8 ejemplos etiquetados en `docs/ejemplos_tuning.json` y necesito al menos 200, así que me faltan 192: unas 16 horas de etiquetado a 5 minutos por ejemplo. Hoy están repartidos en 5 categorías: entorno 3, autenticacion 2, red 1, cuota 1, consistencia_indice 1. Las categorías con menos ejemplos tienen solo 1 y quiero llegar al menos a 30 por categoría. No necesito un corpus para indexar, porque no uso RAG.