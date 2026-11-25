# Fundamentos de caché

## ¿Qué es?

Una copia de datos que permite responder sin consultar otra vez el origen.
Un **hit** encuentra el dato; un **miss** obliga a buscarlo fuera de la caché.

## ¿Cómo funciona?

Se busca por una clave, como el ID del producto. Si falta, se consulta el origen
y se guarda su respuesta para las siguientes lecturas.

## ¿Cuándo usarla?

Cuando muchas consultas repiten los mismos datos y obtenerlos cuesta tiempo o recursos.

## ¿Cuándo evitarla?

Cuando casi nunca se repiten consultas o se exige información actualizada en cada lectura.

## ¿Cómo aplicarla?

Define la clave, el dato almacenado y la frescura aceptable. Después añade límite,
caducidad e invalidación según el caso; este ejemplo introductorio todavía no los implementa.

## Ejemplo práctico

Ejecuta `py -3.14 .\01_cache_basics\example.py` desde la raíz.
Verás una consulta lenta simulada y después un hit. El contador termina en **1**.
Los precios son enteros en centavos; solo se almacenan valores inmutables.

**Referencia:** [Patrón cache-aside](https://learn.microsoft.com/en-us/azure/architecture/patterns/cache-aside).
