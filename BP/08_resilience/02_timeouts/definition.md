# Límites de espera

## ¿Qué es?

Es decidir cuánto esperar antes de devolver un fallo controlado. El trabajo remoto puede seguir ejecutándose después.

## ¿Cómo funciona y para qué sirve?

La versión mejorada limita una espera asíncrona y muestra la excepción. En una integración real diferencia conexión, lectura y presupuesto total.

## Qué muestra el ejemplo

after.py termina con DEPENDENCY_TIMEOUT en lugar de esperar toda la operación simulada.

Tecnología: **Python**.

## Cómo revisarlo o ejecutarlo

Desde la raíz del repositorio:

```powershell
.\.venv\Scripts\python.exe -B .\BP\08_resilience\02_timeouts\before.py
.\.venv\Scripts\python.exe -B .\BP\08_resilience\02_timeouts\after.py
```

## Qué pide la organización

La guía interna pide aplicar esta práctica según el tipo de componente. Los valores del ejemplo son didácticos y no representan parámetros productivos aprobados.

## Límites y aclaraciones

La cancelación de asyncio es cooperativa. No mata hilos ni revierte una operación remota. El timeout de lectura de requests tampoco equivale a un plazo total.

## Referencias

Consulta [general](../../SOURCES.md#general) para identificar el manual de origen.
Las precisiones pendientes se registran en [CLARIFICATIONS.md](../../CLARIFICATIONS.md).
