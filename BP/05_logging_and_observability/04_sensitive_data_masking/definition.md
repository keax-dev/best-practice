# Protección de datos en logs

## ¿Qué es?

Es impedir que contraseñas, tokens y datos personales terminen en registros de diagnóstico.

## ¿Cómo funciona y para qué sirve?

Es más seguro construir un evento con campos permitidos que registrar todo y confiar en recordar todas las claves sensibles.

## Qué muestra el ejemplo

Los datos son ficticios. La salida mejorada no contiene el token ni el correo anidado.

Tecnología: **Python**.

## Cómo revisarlo o ejecutarlo

Desde la raíz del repositorio:

```powershell
.\.venv\Scripts\python.exe -B .\BP\05_logging_and_observability\04_sensitive_data_masking\before.py
.\.venv\Scripts\python.exe -B .\BP\05_logging_and_observability\04_sensitive_data_masking\after.py
```

## Qué pide la organización

La guía interna pide aplicar esta práctica según el tipo de componente. Los valores del ejemplo son didácticos y no representan parámetros productivos aprobados.

## Límites y aclaraciones

No existe una lista universal de claves que detecte todos los datos sensibles. La clasificación y los identificadores permitidos deben validarse según el dominio.

## Referencias

Consulta [general](../../SOURCES.md#general) para identificar el manual de origen.
Las precisiones pendientes se registran en [CLARIFICATIONS.md](../../CLARIFICATIONS.md).
