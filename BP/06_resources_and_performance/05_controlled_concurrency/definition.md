# Concurrencia controlada

## ¿Qué es?

Es limitar cuántas tareas pueden usar recursos simultáneamente y coordinar su cierre.

## ¿Cómo funciona y para qué sirve?

ThreadPoolExecutor administra trabajadores y with espera su finalización. En Python 3.14, buffersize limita además cuántos resultados quedan pendientes en map.

## Qué muestra el ejemplo

La versión mejorada devuelve los resultados en orden con un máximo de dos trabajadores.

Tecnología: **Python**.

## Cómo revisarlo o ejecutarlo

Desde la raíz del repositorio:

```powershell
.\.venv\Scripts\python.exe -B .\BP\06_resources_and_performance\05_controlled_concurrency\before.py
.\.venv\Scripts\python.exe -B .\BP\06_resources_and_performance\05_controlled_concurrency\after.py
```

## Qué pide la organización

La guía interna pide aplicar esta práctica según el tipo de componente. Los valores del ejemplo son didácticos y no representan parámetros productivos aprobados.

## Límites y aclaraciones

buffersize requiere Python 3.14. Un timeout de espera no mata automáticamente un hilo que ya empezó. Los datos compartidos mutables necesitan protección adicional.

## Referencias

Consulta [general](../../SOURCES.md#general) para identificar el manual de origen.
Las precisiones pendientes se registran en [CLARIFICATIONS.md](../../CLARIFICATIONS.md).
