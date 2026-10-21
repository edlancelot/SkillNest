# Decisión de arquitectura: elección de modelo

Fecha de la comparación: Martes 21 de Octubre del 2026
Nombre de la miniaplicación: "mi miniaplicación"

## Modelo elegido

Elegí el modelo: gemini-3.8-flash

Mi miniaplicación sirve para: Asignar automáticamente las cargas a los camiones. Considera el tamaño de las cargas y la capacidad de cada camión.

## Diagrama de arquitectura

[Diagrama de Arquitectura] - (docs/diagrama_arquitectura.png)

## Comparación de candidatos

- Estas son las preguntas y condiciones con las cuales se midieron ambos modelos:

Actúa como un especialista en logística y optimización de carga de camiones.

Determina cuántas unidades de un producto pueden cargarse dentro de un camión, considerando sus dimensiones y peso.

DATOS DEL CAMIÓN:
- Largo interior: 6000 mm
- Ancho interior: 2400 mm
- Alto interior: 2400 mm
- Capacidad máxima de carga: 8000 kg

DATOS DEL PRODUCTO:
- Largo: 400 mm
- Ancho: 300 mm
- Alto: 250 mm
- Peso por unidad: 12 kg

RESTRICCIONES:
1. Los productos deben permanecer completamente dentro del camión.
2. Se permite rotar los productos en cualquiera de sus tres ejes.
3. Los productos no pueden superponerse ni sobresalir del camión.
4. Debes respetar las dimensiones y el peso máximo permitido.
5. Determina cuántas unidades pueden cargarse físicamente.
6. No confundas el límite teórico por volumen con una distribución físicamente factible.
7. No inventes datos ni afirmes que una distribución es óptima si no puedes demostrarlo.

Responde únicamente con un string en español que indique la cantidad máxima estimada de unidades que caben en el camión, el peso total y una explicación breve del cálculo.

No utilices JSON, listas, encabezados, Markdown ni texto adicional fuera de la respuesta solicitada.

| Criterio | gemini-3.5-flash-lite | gemini-3.8-flash | gemini-3.6-flash |
|---|---|---|---|
| Tarifa de entrada en USD por millón de tokens | $0.30 | $0.75 | $0.75 |
| Tarifa de salida en USD por millón de tokens | $2.50 | $3.75 | $3.75 |
| Latencias observadas en segundos | 2.603 / 2.787 / 2.245 | 9.373 / 10.983 / 9.649 | 11.701 (las pruebas 1 y 2 fallaron con error 503) |
| Latencia promedio en segundos | 2.545 | 10.002 | 11.701 (solo 1 prueba exitosa) |
| Calidad para nuestra miniaplicación | Baja: respuestas inconsistentes (660, 576 y 576 unidades) y contradictorias; el cálculo por peso da 666 y aun así reporta menos | Alta: respuesta consistente en las 3 pruebas (666 unidades, 7992 kg), explicación breve y alineada con el formato pedido | Alta en la única prueba exitosa (666 unidades, 7992 kg); sin datos suficientes para confirmar consistencia |

Fuente de las tarifas:
- gemini-3.5-flash-lite: https://ai.google.dev/gemini-api/docs/pricing
- gemini-3.8-flash: https://ai.google.dev/gemini-api/docs/pricing
- gemini-3.6-flash: https://ai.google.dev/gemini-api/docs/pricing

Observación sobre las pruebas:

Velocidad y estabilidad
gemini-3.5-flash-lite es ~75 % más rápido que gemini-3.8-flash en promedio (2.5 s frente a 10.0 s) y muy estable (2.2 a 2.8 s). gemini-3.8-flash varía de 9.4 a 11.0 s y es ~15 % más rápido que gemini-3.6-flash (11.7 s, una sola prueba). gemini-3.6-flash falló 2 de 3 pruebas con error 503 (sobrecarga del servicio), mientras que los otros dos completaron las 3.

Costo
gemini-3.8-flash costó ~376 % más por petición que gemini-3.5-flash-lite ($0.0047 frente a $0.0010). gemini-3.6-flash costó ~77 % más que gemini-3.8-flash en su única prueba exitosa ($0.0083 frente a $0.0047), a pesar de tener la misma tarifa por token, porque consumió más tokens.

Calidad de la respuesta
El resultado correcto es 666 unidades y 7992 kg, porque el límite lo impone el peso (8000 kg / 12 kg) y no el volumen, que permitiría hasta 1152 unidades. gemini-3.8-flash acertó en las 3 pruebas, con explicaciones breves y en el formato pedido. gemini-3.6-flash acertó en su única prueba. gemini-3.5-flash-lite no acertó en ninguna (660, 576 y 576 unidades) y se contradice: calcula 666 por peso y luego reporta una cifra menor.

## Justificación

Se usará gemini-3.8-flash porque entregó la respuesta correcta (666 unidades y 7992 kg) en las 3 pruebas, de forma ordenada y en el formato pedido.
El criterio más relevante fue la calidad de la respuesta, ya que una asignación incorrecta de carga no es aceptable en despacho.

## Alternativa descartada y por qué

Descarté gemini-3.5-flash-lite porque, aunque fue el más rápido (2.5 s) y barato, no entregó la respuesta correcta en ninguna prueba (660, 576 y 576 unidades frente a las 666 correctas) y se contradijo en sus cálculos.
Descarté gemini-3.6-flash porque tiene la misma tarifa que gemini-3.8-flash pero fue más lento (11.7 s), más caro por petición en su única prueba exitosa y falló 2 de 3 pruebas con error 503.