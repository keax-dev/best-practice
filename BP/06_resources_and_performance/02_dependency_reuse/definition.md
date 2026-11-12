# Reutilizar dependencias

## ¿Qué es?

Es crear una herramienta reutilizable una vez por el alcance adecuado y usarla en varias operaciones.

## ¿Cómo funciona y para qué sirve?

Una dependencia costosa no necesita reconstruirse por cada elemento. La composición de la aplicación decide su ciclo de vida.

## Qué muestra el ejemplo

Los resultados de catálogo coinciden. El ejemplo cuenta construcciones, no pretende medir una mejora de rendimiento real.

Tecnología: **Python**.

## Cómo revisarlo o ejecutarlo

Desde la raíz del repositorio:

```powershell
.\.venv\Scripts\python.exe -B .\BP\06_resources_and_performance\02_dependency_reuse\before.py
.\.venv\Scripts\python.exe -B .\BP\06_resources_and_performance\02_dependency_reuse\after.py
```

## Qué pide la organización

La guía interna pide aplicar esta práctica según el tipo de componente. Los valores del ejemplo son didácticos y no representan parámetros productivos aprobados.

## Límites y aclaraciones

No compartas automáticamente sesiones transaccionales u objetos no seguros entre hilos. Reutilizar depende de su contrato y del alcance de solicitud o aplicación.

## Referencias

Consulta [general](../../SOURCES.md#general) para identificar el manual de origen.
Las precisiones pendientes se registran en [CLARIFICATIONS.md](../../CLARIFICATIONS.md).
