# Circuit breaker

## ¿Qué es?

Es dejar de llamar temporalmente a una dependencia que falla repetidamente y probar su recuperación después.

## ¿Cómo funciona y para qué sirve?

El ejemplo usa estados CLOSED, OPEN y HALF_OPEN. Un reloj inyectado permite avanzar hasta la prueba de recuperación sin esperar.

## Qué muestra el ejemplo

Después de dos fallos, la tercera solicitud no llega a la operación. Al avanzar el reloj se prueba una llamada que recupera el circuito.

Tecnología: **Python**.

## Cómo revisarlo o ejecutarlo

Desde la raíz del repositorio:

```powershell
.\.venv\Scripts\python.exe -B .\BP\08_resilience\05_circuit_breaker\before.py
.\.venv\Scripts\python.exe -B .\BP\08_resilience\05_circuit_breaker\after.py
```

## Qué pide la organización

La guía interna pide aplicar esta práctica según el tipo de componente. Los valores del ejemplo son didácticos y no representan parámetros productivos aprobados.

## Límites y aclaraciones

La implementación es secuencial y educativa, no thread-safe ni distribuida. Una librería de producción necesita controlar pruebas simultáneas, métricas y clasificación de fallos.

## Referencias

Consulta [general](../../SOURCES.md#general) para identificar el manual de origen.
Las precisiones pendientes se registran en [CLARIFICATIONS.md](../../CLARIFICATIONS.md).
