# Conservar la causa original

## ¿Qué es?

Es explicar el fallo con un error de tu aplicación sin perder la excepción que lo provocó.

## ¿Cómo funciona y para qué sirve?

raise NuevoError(...) from error conserva una relación explícita entre ambas excepciones. El registro técnico puede mostrar la causa sin enviarla al usuario.

## Qué muestra el ejemplo

Ambas rechazan el dato, pero solo after.py conserva ValueError como causa explícita.

Tecnología: **Python**.

## Cómo revisarlo o ejecutarlo

Desde la raíz del repositorio:

```powershell
.\.venv\Scripts\python.exe -B .\BP\02_error_handling\03_exception_chaining\before.py
.\.venv\Scripts\python.exe -B .\BP\02_error_handling\03_exception_chaining\after.py
```

## Qué pide la organización

La guía interna pide aplicar esta práctica según el tipo de componente. Los valores del ejemplo son didácticos y no representan parámetros productivos aprobados.

## Límites y aclaraciones

El ejemplo aísla una práctica. No representa una aplicación completa ni todas sus validaciones.

## Referencias

Consulta [general](../../SOURCES.md#general) para identificar el manual de origen.
Las precisiones pendientes se registran en [CLARIFICATIONS.md](../../CLARIFICATIONS.md).
