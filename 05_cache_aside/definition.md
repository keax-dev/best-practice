# Cache-aside

## ¿Qué es?

Una estrategia donde la aplicación consulta la caché y carga del origen
solamente los datos que faltan.

## ¿Cómo funciona?

Buscar la clave → devolver un hit o consultar el origen → guardar el resultado
válido → devolverlo. La aplicación controla ese recorrido.

## ¿Cuándo usarla?

Para catálogos con muchas lecturas repetidas y productos que no interesa cargar
todos al iniciar la aplicación.

## ¿Cuándo evitarla?

Cuando casi no hay reutilización o se necesita consistencia inmediata con cambios
realizados por otros procesos.

## ¿Cómo aplicarla?

Mantén separado el origen, define claves y combina con TTL, capacidad e invalidación.
Un fallo al cargar no debe almacenarse como si fuera un precio válido. Guardar
la ausencia de un producto sería otra decisión, llamada caché negativa.

## Ejemplo práctico

Ejecuta `py -3.14 .\05_cache_aside\example.py`.
Consultar dos veces el producto 1 y una vez el 2 produce **dos cargas**.

**Referencia:** [Patrón cache-aside](https://learn.microsoft.com/en-us/azure/architecture/patterns/cache-aside).
