# Compatibilidad hacia atrás

## ¿Qué es?

Es cambiar un contrato sin impedir que los consumidores anteriores sigan utilizándolo.

## ¿Cómo funciona y para qué sirve?

Renombrar un campo requerido rompe al cliente que todavía lo lee. Mantener el campo anterior puede permitir una transición documentada.

## Qué muestra el ejemplo

El consumidor anterior vuelve a leer status. reason es opcional para ese consumidor.

Tecnología: **Python**.

## Cómo revisarlo o ejecutarlo

Desde la raíz del repositorio:

```powershell
.\.venv\Scripts\python.exe -B .\BP\08_resilience\07_backward_compatibility\before.py
.\.venv\Scripts\python.exe -B .\BP\08_resilience\07_backward_compatibility\after.py
```

## Qué pide la organización

La guía interna pide aplicar esta práctica según el tipo de componente. Los valores del ejemplo son didácticos y no representan parámetros productivos aprobados.

## Límites y aclaraciones

Agregar un campo tampoco es siempre compatible: un consumidor con additionalProperties=false puede rechazarlo. Verifica ambos contratos y la estrategia de versionado.

## Referencias

Consulta [general](../../SOURCES.md#general) para identificar el manual de origen.
Las precisiones pendientes se registran en [CLARIFICATIONS.md](../../CLARIFICATIONS.md).
