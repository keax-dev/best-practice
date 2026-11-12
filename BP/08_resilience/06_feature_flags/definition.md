# Feature flags

## ¿Qué es?

Es seleccionar entre comportamientos ya desplegados sin mezclar esa decisión con la regla que ejecutan.

## ¿Cómo funciona y para qué sirve?

Un proveedor de flags puede cambiar su respuesta durante la ejecución. En la demostración se actualiza un objeto local, sin afirmar que las variables de entorno cambien solas.

## Qué muestra el ejemplo

El resultado cambia de Classic checkout a New checkout en el mismo proceso.

Tecnología: **Python**.

## Cómo revisarlo o ejecutarlo

Desde la raíz del repositorio:

```powershell
.\.venv\Scripts\python.exe -B .\BP\08_resilience\06_feature_flags\before.py
.\.venv\Scripts\python.exe -B .\BP\08_resilience\06_feature_flags\after.py
```

## Qué pide la organización

La guía interna pide aplicar esta práctica según el tipo de componente. Los valores del ejemplo son didácticos y no representan parámetros productivos aprobados.

## Límites y aclaraciones

Un flag no sustituye permisos ni autenticación. Debe tener dueño, fecha de revisión y retirada cuando ya no se necesite.

## Referencias

Consulta [general](../../SOURCES.md#general) para identificar el manual de origen.
Las precisiones pendientes se registran en [CLARIFICATIONS.md](../../CLARIFICATIONS.md).
