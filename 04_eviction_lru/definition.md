# LRU — expulsión por uso menos reciente

## ¿Qué es?

Una política que retira la entrada que lleva más tiempo sin utilizarse cuando
la caché necesita espacio.

## ¿Cómo funciona?

Cada lectura o escritura mueve la entrada al final del orden de uso.
Cuando se supera la capacidad, se elimina la primera.

## ¿Cuándo usarla?

Cuando hay muchas claves posibles, memoria limitada y consultas que suelen
repetir productos vistos recientemente.

## ¿Cuándo evitarla?

Cuando casi todas las consultas son únicas o conviene priorizar otros criterios,
como la frecuencia de acceso o el coste de reconstruir cada dato.

## ¿Cómo aplicarla?

Establece una capacidad y actualiza el orden en cada acceso. El ejemplo limita
cantidad de entradas, no bytes. LRU no indica si un precio está actualizado:
para eso hacen falta TTL o invalidación.

## Ejemplo práctico

Ejecuta `py -3.14 .\04_eviction_lru\example.py`.
Tras consultar el producto 1 y añadir el 3, se expulsa el 2.

**Referencia:** [OrderedDict](https://docs.python.org/3.14/library/collections.html#collections.OrderedDict).
