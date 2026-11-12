# Caché con límites y expiración

## ¿Qué es?

Es guardar resultados temporalmente con un máximo de elementos y un tiempo de validez.

## ¿Cómo funciona y para qué sirve?

El ejemplo inyecta un reloj para comprobar expiración sin esperar. Si se llena la capacidad, elimina el elemento más antiguo.

## Qué muestra el ejemplo

La capacidad queda en dos elementos. Al avanzar el reloj hasta el vencimiento, get deja de devolver el valor.

Tecnología: **Python**.

## Cómo revisarlo o ejecutarlo

Desde la raíz del repositorio:

```powershell
.\.venv\Scripts\python.exe -B .\BP\06_resources_and_performance\03_bounded_cache\before.py
.\.venv\Scripts\python.exe -B .\BP\06_resources_and_performance\03_bounded_cache\after.py
```

## Qué pide la organización

La guía interna pide aplicar esta práctica según el tipo de componente. Los valores del ejemplo son didácticos y no representan parámetros productivos aprobados.

## Límites y aclaraciones

Esta caché FIFO educativa no es thread-safe y expira al leer. Una caché no reemplaza el almacenamiento de pedidos: no deben desaparecer datos de negocio por un TTL.

## Referencias

Consulta [general](../../SOURCES.md#general) para identificar el manual de origen.
Las precisiones pendientes se registran en [CLARIFICATIONS.md](../../CLARIFICATIONS.md).
