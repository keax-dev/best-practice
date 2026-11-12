# Cambiar niveles de log

## ¿Qué es?

Es poder ajustar el detalle publicado sin modificar la regla de negocio.

## ¿Cómo funciona y para qué sirve?

Una función valida el nombre del nivel y cambia el logger. El ejemplo demuestra el cambio en el mismo proceso, sin exponer un endpoint de administración.

## Qué muestra el ejemplo

El nivel pasa de INFO a DEBUG sin reiniciar el proceso.

Tecnología: **Python**.

## Cómo revisarlo o ejecutarlo

Desde la raíz del repositorio:

```powershell
.\.venv\Scripts\python.exe -B .\BP\05_logging_and_observability\05_dynamic_log_levels\before.py
.\.venv\Scripts\python.exe -B .\BP\05_logging_and_observability\05_dynamic_log_levels\after.py
```

## Qué pide la organización

La guía interna pide aplicar esta práctica según el tipo de componente. Los valores del ejemplo son didácticos y no representan parámetros productivos aprobados.

## Límites y aclaraciones

En un servicio, la interfaz que habilita este cambio necesita autenticación y autorización. Cambiar una variable de entorno externa no llama a esta función por sí solo.

## Referencias

Consulta [general](../../SOURCES.md#general) para identificar el manual de origen.
Las precisiones pendientes se registran en [CLARIFICATIONS.md](../../CLARIFICATIONS.md).
