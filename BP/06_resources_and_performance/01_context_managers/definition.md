# Cerrar recursos con with

## ¿Qué es?

Es asegurar que un archivo o una conexión se libere al terminar, incluso si una operación falla.

## ¿Cómo funciona y para qué sirve?

Un context manager ejecuta su limpieza al salir del bloque. El ejemplo usa un archivo temporal que se elimina automáticamente.

## Qué muestra el ejemplo

La versión mejorada demuestra el cierre después de un error deliberado, sin dejar un archivo en el repositorio.

Tecnología: **Python**.

## Cómo revisarlo o ejecutarlo

Desde la raíz del repositorio:

```powershell
.\.venv\Scripts\python.exe -B .\BP\06_resources_and_performance\01_context_managers\before.py
.\.venv\Scripts\python.exe -B .\BP\06_resources_and_performance\01_context_managers\after.py
```

## Qué pide la organización

La guía interna pide aplicar esta práctica según el tipo de componente. Los valores del ejemplo son didácticos y no representan parámetros productivos aprobados.

## Límites y aclaraciones

El ejemplo aísla una práctica. No representa una aplicación completa ni todas sus validaciones.

## Referencias

Consulta [general](../../SOURCES.md#general) para identificar el manual de origen.
Las precisiones pendientes se registran en [CLARIFICATIONS.md](../../CLARIFICATIONS.md).
