# Acceso concurrente

## ¿Qué es?

Coordinar solicitudes simultáneas para que una clave ausente no provoque muchas
cargas iguales. Esa avalancha de cargas se conoce como **cache stampede**.

## ¿Cómo funciona?

Un lock protege la comprobación, carga y almacenamiento. El primer hilo carga;
los siguientes esperan y reutilizan el resultado guardado.

## ¿Cuándo usarla?

Cuando varias solicitudes coinciden sobre datos ausentes o recién caducados y
consultar el origen resulta costoso.

## ¿Cuándo evitarla?

Un lock global no conviene si deben cargarse muchas claves diferentes a la vez:
también las bloquea entre sí. En ese caso conviene coordinación por clave.

## ¿Cómo aplicarla?

No protejas solamente la escritura: incluye la comprobación y la carga.
El ejemplo usa un lock global para enseñar el recorrido. No coordina otros
procesos; las llamadas externas reales necesitan además timeouts.

## Ejemplo práctico

Ejecuta `py -3.14 .\07_concurrent_access\example.py`.
Seis hilos consultan el mismo precio y el origen se carga **una sola vez**.
Si una carga falla, se libera el lock y otra llamada puede intentarlo.

**Referencia:** [threading.Lock](https://docs.python.org/3.14/library/threading.html#lock-objects).
