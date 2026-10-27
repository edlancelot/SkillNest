## Registro del ensayo de rate limit
 
- Fecha: 2026-09-09
- Peticiones enviadas: 10
- Petición donde apareció el primer 429: la número 0, la primera. El registro no muestra el código HTTP, solo que falló y se reintentó, así que no puedo confirmar que fuera un 429.
- Esperas observadas: 2.0s, 4.1s, 2.1s, 2.2s, 2.0s, 2.2s, 2.1s, 4.0s. La primera espera ronda los 2s y la segunda los 4s (backoff exponencial con jitter, correcto). Ninguna petición llegó a una tercera espera de ~8s, porque el máximo es de 3 intentos.
- Costo total del ensayo: $0.00037 (una sola operación exitosa, 185 tokens)
- Resultado: solo 1 de 10 peticiones terminó con éxito (la 1). Las otras 9 fallaron definitivamente tras agotar los reintentos: la 0 con “El servicio no respondió” y las 2 a 9 con “Se agotó el tiempo”.