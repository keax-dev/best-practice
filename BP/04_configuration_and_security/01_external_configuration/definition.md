# Configuración externa

## ¿Qué es?

Es recibir desde fuera los valores que cambian entre entornos, sin editar la lógica del programa.

## ¿Cómo funciona y para qué sirve?

Las variables de entorno pueden proporcionar un timeout o una URL. La aplicación las lee al arrancar y conserva una configuración explícita.

## Qué muestra el ejemplo

Ejecuta after.py con APP_HTTP_TIMEOUT_SECONDS=3 para observar el cambio. La siguiente lección agrega validación.

Tecnología: **Python**.

## Cómo revisarlo o ejecutarlo

Desde la raíz del repositorio:

```powershell
.\.venv\Scripts\python.exe -B .\BP\04_configuration_and_security\01_external_configuration\before.py
.\.venv\Scripts\python.exe -B .\BP\04_configuration_and_security\01_external_configuration\after.py
```

## Qué pide la organización

La guía interna pide aplicar esta práctica según el tipo de componente. Los valores del ejemplo son didácticos y no representan parámetros productivos aprobados.

## Límites y aclaraciones

Leer variables de entorno al iniciar no permite actualizarlas en caliente automáticamente. Un valor predeterminado solo es apropiado si tiene sentido para ese parámetro.

## Referencias

Consulta [general](../../SOURCES.md#general) para identificar el manual de origen.
Las precisiones pendientes se registran en [CLARIFICATIONS.md](../../CLARIFICATIONS.md).
