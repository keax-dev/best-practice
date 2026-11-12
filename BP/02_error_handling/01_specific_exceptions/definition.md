# Excepciones específicas

## ¿Qué es?

Es indicar qué problema esperas y capturarlo sin ocultar errores de programación diferentes.

## ¿Cómo funciona y para qué sirve?

Una entrada no numérica puede provocar ValueError. Un error de otro tipo debe continuar hacia una capa que sepa tratarlo.

## Qué muestra el ejemplo

La versión anterior oculta el fallo con None. La posterior distingue la conversión inválida. Complementa [manejo explícito de errores](../../../clean_code/06_explicit_error_handling/definition.md).

Tecnología: **Python**.

## Cómo revisarlo o ejecutarlo

Desde la raíz del repositorio:

```powershell
.\.venv\Scripts\python.exe -B .\BP\02_error_handling\01_specific_exceptions\before.py
.\.venv\Scripts\python.exe -B .\BP\02_error_handling\01_specific_exceptions\after.py
```

## Qué pide la organización

La guía interna pide aplicar esta práctica según el tipo de componente. Los valores del ejemplo son didácticos y no representan parámetros productivos aprobados.

## Límites y aclaraciones

El ejemplo aísla una práctica. No representa una aplicación completa ni todas sus validaciones.

## Referencias

Consulta [general](../../SOURCES.md#general) para identificar el manual de origen.
Las precisiones pendientes se registran en [CLARIFICATIONS.md](../../CLARIFICATIONS.md).
