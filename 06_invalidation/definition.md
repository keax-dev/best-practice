# Invalidación

## ¿Qué es?

Eliminar una copia que ya no debe utilizarse, por ejemplo porque cambió el precio
guardado en el origen.

## ¿Cómo funciona?

En cache-aside se actualiza primero el origen. Si la escritura termina correctamente,
se elimina la entrada. La próxima lectura carga el nuevo valor.

## ¿Cuándo usarla?

Cuando la aplicación conoce los cambios y necesita dejar de servir la copia anterior
antes de que venza su TTL.

## ¿Cuándo evitarla?

Como única garantía si existen escritores externos, varias instancias o lecturas
concurrentes que puedan volver a introducir un valor antiguo.

## ¿Cómo aplicarla?

Invalida todas las claves afectadas, incluidos listados derivados. Si falla la
escritura del origen, conserva la copia previa. En sistemas distribuidos hacen
falta mecanismos adicionales de coordinación o propagación.

## Ejemplo práctico

Ejecuta `py -3.14 .\06_invalidation\example.py`.
El precio cambia de **1250 a 1500** y la lectura posterior consulta el origen.
El ejemplo es secuencial y usa un único proceso.

**Referencia:** [Actualización e invalidación en cache-aside](https://learn.microsoft.com/en-us/azure/architecture/patterns/cache-aside).
