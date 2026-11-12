# Identificadores de correlación

## ¿Qué es?

Es usar el mismo identificador para reconocer los pasos de una operación.

## ¿Cómo funciona y para qué sirve?

ContextVar mantiene el contexto separado entre tareas asíncronas. En HTTP, propaga un identificador validado entre llamadas; al terminar restablece el contexto.

## Qué muestra el ejemplo

Los dos pasos comparten request-1 y después el contexto vuelve a none.

Tecnología: **Python**.

## Cómo revisarlo o ejecutarlo

Desde la raíz del repositorio:

```powershell
.\.venv\Scripts\python.exe -B .\BP\05_logging_and_observability\03_correlation_ids\before.py
.\.venv\Scripts\python.exe -B .\BP\05_logging_and_observability\03_correlation_ids\after.py
```

## Qué pide la organización

La guía interna pide aplicar esta práctica según el tipo de componente. Los valores del ejemplo son didácticos y no representan parámetros productivos aprobados.

## Límites y aclaraciones

ContextVar no viaja automáticamente por HTTP ni se copia siempre a nuevos hilos. Esa propagación debe realizarse explícitamente. El manual exige x-guid según el contrato aplicable.

## Referencias

Consulta [general](../../SOURCES.md#general) para identificar el manual de origen.
Las precisiones pendientes se registran en [CLARIFICATIONS.md](../../CLARIFICATIONS.md).
