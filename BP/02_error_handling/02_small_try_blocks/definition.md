# Bloques try pequeños

## ¿Qué es?

Es poner dentro del try solo la operación cuyo error sabes interpretar.

## ¿Cómo funciona y para qué sirve?

Si capturas ValueError alrededor de toda una operación, puedes confundir una configuración inválida con un dato mal escrito por el usuario.

## Qué muestra el ejemplo

Se simula una política ausente. before.py acusa al usuario; after.py deja visible que el problema pertenece a la configuración.

Tecnología: **Python**.

## Cómo revisarlo o ejecutarlo

Desde la raíz del repositorio:

```powershell
.\.venv\Scripts\python.exe -B .\BP\02_error_handling\02_small_try_blocks\before.py
.\.venv\Scripts\python.exe -B .\BP\02_error_handling\02_small_try_blocks\after.py
```

## Qué pide la organización

La guía interna pide aplicar esta práctica según el tipo de componente. Los valores del ejemplo son didácticos y no representan parámetros productivos aprobados.

## Límites y aclaraciones

El ejemplo aísla una práctica. No representa una aplicación completa ni todas sus validaciones.

## Referencias

Consulta [general](../../SOURCES.md#general) para identificar el manual de origen.
Las precisiones pendientes se registran en [CLARIFICATIONS.md](../../CLARIFICATIONS.md).
