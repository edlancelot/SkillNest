# Límites de autonomía: Asistente de soporte de envíos y reembolsos


## Herramientas y nivel de riesgo

- consultar_estado_envio_detallado: bajo. Solo lee el diccionario
  `ESTADOS` y devuelve el estado (y el historial si se pide). No
  modifica nada.

- calcular_costo_envio: bajo. Solo hace una cuenta con el peso y la
  distancia que recibe (500 + 120 por kg + 3 por km). No ejecuta
  ninguna acción externa.

- generar_reembolso: alto. Es dinero que sale y no se puede devolver
  una vez hecho.

## Herramientas que requieren aprobación humana

- generar_reembolso: es la única que mueve dinero. Antes de ejecutar,
  llama a `esperar_aprobacion` y muestra el
  pedido y el monto. Solo se aprueba si la persona escribe "s". Si
  escribe otra cosa, o pasan 15 segundos sin respuesta, se rechaza por timeout.
  Cada decisión queda en `registro_aprobaciones` con la herramienta,
  los argumentos, si se aprobó y la hora.

## Revisión de trazas

- Frecuencia: cada reembolso (aprobado o rechazado) se revisa el mismo
  día. Las demás interacciones, una vez por semana o cada 20
  interacciones, lo que ocurra primero.

- Qué se busca:
  - un reembolso sin que el cliente lo haya pedido, o por un monto
    distinto al que escribió
  - la misma herramienta llamada varias veces seguidas con los mismos
    argumentos
  - un número de pedido o de seguimiento que el cliente nunca
    mencionó (dato inventado)
  - una respuesta final con una cifra distinta a la de la
    observación de la herramienta
  - respuesta final que dice que el reembolso se hizo cuando la
    observación dice que no fue aprobado
  - interacciones sin ninguna acción cuando la pregunta pedía una


## Qué hacer ante un comportamiento inesperado

1. Detener el agente (Ctrl+C).
2. Si el problema involucra dinero, sacar `generar_reembolso` de la
   lista `herramientas` de `agente_con_memoria.py`. Con eso el agente solo puede
   consultar y calcular.
3. Buscar la interacción en `trazas_agente.json` por `session_id` y
   comparar los argumentos, la observación y la respuesta final.
4. Corregir según la causa: si eligió mal la herramienta, ajustar su
   descripción; si inventó argumentos, mejorar las descripciones del
   esquema de argumentos; si ignora lo que devolvió la herramienta,
   ajustar el prompt del sistema.
5. Repetir la misma entrada y comparar la traza nueva con la anterior.
6. Volver a activar la herramienta solo si la traza sale correcta.
