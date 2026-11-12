# Niveles de log

## ¿Qué es?

Es clasificar los mensajes según si describen el funcionamiento normal, un diagnóstico o un problema.

## ¿Cómo funciona y para qué sirve?

Usa DEBUG para diagnóstico, INFO para hitos normales, WARNING para situaciones anómalas y ERROR para operaciones fallidas.

## Qué muestra el ejemplo

Con INFO no se publica DEBUG. logging usa stderr por defecto; ver mensajes allí no significa que el script haya fallado.

Tecnología: **Python**.

## Cómo revisarlo o ejecutarlo

Desde la raíz del repositorio:

```powershell
.\.venv\Scripts\python.exe -B .\BP\05_logging_and_observability\01_log_levels\before.py
.\.venv\Scripts\python.exe -B .\BP\05_logging_and_observability\01_log_levels\after.py
```

## Qué pide la organización

La guía interna pide aplicar esta práctica según el tipo de componente. Los valores del ejemplo son didácticos y no representan parámetros productivos aprobados.

## Límites y aclaraciones

El ejemplo aísla una práctica. No representa una aplicación completa ni todas sus validaciones.

## Referencias

Consulta [general](../../SOURCES.md#general) para identificar el manual de origen.
Las precisiones pendientes se registran en [CLARIFICATIONS.md](../../CLARIFICATIONS.md).
