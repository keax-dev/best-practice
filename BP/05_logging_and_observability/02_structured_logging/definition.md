# Logs estructurados

## ¿Qué es?

Es registrar cada evento como datos con campos conocidos, en lugar de depender solo de una frase.

## ¿Cómo funciona y para qué sirve?

Un formatter produce JSON e incluye contexto explícito como order_id. Así los sistemas de consulta pueden filtrar sin analizar texto libre.

## Qué muestra el ejemplo

after.py produce JSON con application, timestamp, level, message y order_id. Estos son campos seleccionados, no una serialización indiscriminada del payload.

Tecnología: **Python**.

## Cómo revisarlo o ejecutarlo

Desde la raíz del repositorio:

```powershell
.\.venv\Scripts\python.exe -B .\BP\05_logging_and_observability\02_structured_logging\before.py
.\.venv\Scripts\python.exe -B .\BP\05_logging_and_observability\02_structured_logging\after.py
```

## Qué pide la organización

La guía interna pide aplicar esta práctica según el tipo de componente. Los valores del ejemplo son didácticos y no representan parámetros productivos aprobados.

## Límites y aclaraciones

El formatter no incluye automáticamente todas las propiedades de extra: hay que seleccionarlas y serializarlas. Nunca publiques credenciales como contexto.

## Referencias

Consulta [general](../../SOURCES.md#general) para identificar el manual de origen.
Las precisiones pendientes se registran en [CLARIFICATIONS.md](../../CLARIFICATIONS.md).
