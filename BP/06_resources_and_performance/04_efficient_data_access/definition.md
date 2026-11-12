# Evitar consultas repetidas

## ¿Qué es?

Es pedir los datos necesarios de una vez cuando puedes evitar una consulta por cada elemento.

## ¿Cómo funciona y para qué sirve?

El ejemplo cuenta accesos de un repositorio simulado. La versión por lotes recibe los identificadores juntos y devuelve sus nombres.

## Qué muestra el ejemplo

Se pasa de tres llamadas simuladas a una. SQL real se estudia en [consultas y filtros](../../09_database_practices/04_joins_and_filters/definition.md).

Tecnología: **Python**.

## Cómo revisarlo o ejecutarlo

Desde la raíz del repositorio:

```powershell
.\.venv\Scripts\python.exe -B .\BP\06_resources_and_performance\04_efficient_data_access\before.py
.\.venv\Scripts\python.exe -B .\BP\06_resources_and_performance\04_efficient_data_access\after.py
```

## Qué pide la organización

La guía interna pide aplicar esta práctica según el tipo de componente. Los valores del ejemplo son didácticos y no representan parámetros productivos aprobados.

## Límites y aclaraciones

En PostgreSQL y JPA hay que medir planes, volumen, tamaño del lote y relaciones. El contador no demuestra que toda consulta grande sea mejor.

## Referencias

Consulta [general](../../SOURCES.md#general) para identificar el manual de origen.
Las precisiones pendientes se registran en [CLARIFICATIONS.md](../../CLARIFICATIONS.md).
