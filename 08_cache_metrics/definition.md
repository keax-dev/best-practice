# Métricas de caché

## ¿Qué es?

Medir el uso de la caché para saber si evita trabajo y dónde ajustar su configuración.

## ¿Cómo funciona?

Se cuentan hits y misses. La proporción de aciertos es
`hits / (hits + misses)`; aquí se informa cero cuando todavía no hay consultas.
También se cuentan intentos de carga al origen y errores de carga.

## ¿Cuándo usarla?

Al decidir si la caché aporta valor y al ajustar capacidad, TTL o selección de datos.

## ¿Cuándo evitarla?

Evita juzgar el sistema solo por el porcentaje de hits. Un porcentaje alto no
demuestra que las respuestas sean correctas o estén actualizadas.

## ¿Cómo aplicarla?

Relaciona aciertos con latencia, errores, memoria y frescura. No utilices datos
personales como etiquetas de métricas. Estos contadores son locales, secuenciales
y se reinician con el programa.

## Ejemplo práctico

Ejecuta `py -3.14 .\08_cache_metrics\example.py`.
Cuatro consultas generan **dos hits, dos misses, dos cargas y 50 % de aciertos**.
Una carga fallida cuenta como miss y error, pero no guarda una entrada.

**Referencia:** [Información de caché en functools](https://docs.python.org/3.14/library/functools.html#functools.lru_cache).
