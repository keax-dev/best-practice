# Reintentos seguros

## ¿Qué es?

Es repetir solo fallos temporales, con límites y una operación que no duplique efectos al repetirse.

## ¿Cómo funciona y para qué sirve?

El ejemplo reintenta una consulta de lectura. Inyecta la espera y el jitter para que la prueba no duerma y pueda verificar el backoff.

## Qué muestra el ejemplo

Una lectura falla una vez y luego funciona. La espera se registra en una lista en lugar de dormir.

Tecnología: **Python**.

## Cómo revisarlo o ejecutarlo

Desde la raíz del repositorio:

```powershell
.\.venv\Scripts\python.exe -B .\BP\08_resilience\03_safe_retries\before.py
.\.venv\Scripts\python.exe -B .\BP\08_resilience\03_safe_retries\after.py
```

## Qué pide la organización

La guía interna pide aplicar esta práctica según el tipo de componente. Los valores del ejemplo son didácticos y no representan parámetros productivos aprobados.

## Límites y aclaraciones

Esta lección aísla el backoff: no implementa un deadline total ni un circuit breaker integrado. Las llamadas reales deben tener timeout por intento y presupuesto total. Nunca repitas un pago o descuento sin garantías de idempotencia.

## Referencias

Consulta [general](../../SOURCES.md#general) para identificar el manual de origen.
Las precisiones pendientes se registran en [CLARIFICATIONS.md](../../CLARIFICATIONS.md).
