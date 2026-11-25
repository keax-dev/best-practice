# TTL — tiempo de vida

## ¿Qué es?

Una duración que determina hasta cuándo puede utilizarse una entrada de caché.

## ¿Cómo funciona?

Al guardar un dato se calcula su vencimiento. Al leerlo, si ya venció, se elimina
y se devuelve un miss. Aquí el TTL comienza al escribir y no se renueva al leer.

## ¿Cuándo usarla?

Cuando se tolera cierta desactualización, como un catálogo informativo.

## ¿Cuándo evitarla?

Como única protección de datos que deben estar actualizados inmediatamente,
como disponibilidad al confirmar una compra.

## ¿Cómo aplicarla?

Elige la duración según la frecuencia de cambios y la antigüedad aceptable.
Utiliza un reloj monotónico. Combina TTL con invalidación y límite de capacidad.
Este ejemplo elimina entradas vencidas al consultarlas, no mediante tareas periódicas.

## Ejemplo práctico

Ejecuta `py -3.14 .\03_expiration_ttl\example.py`.
Verás el precio y, tras esperar, `None`, que representa un miss. Las pruebas
usan un reloj controlado para verificar el instante exacto de caducidad.

**Referencia:** [time.monotonic](https://docs.python.org/3.14/library/time.html#time.monotonic).
