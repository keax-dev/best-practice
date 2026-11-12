# Gestión de secretos

## ¿Qué es?

Es obtener credenciales sin guardarlas en el código ni mostrarlas en los mensajes del programa.

## ¿Cómo funciona y para qué sirve?

El ejemplo recibe un diccionario que representa un proveedor de configuración. En una aplicación real puede provenir de un gestor de secretos o de valores inyectados por la plataforma.

## Qué muestra el ejemplo

La entrada de la versión mejorada es simulada. Su representación no incluye el token.

Tecnología: **Python**.

## Cómo revisarlo o ejecutarlo

Desde la raíz del repositorio:

```powershell
.\.venv\Scripts\python.exe -B .\BP\04_configuration_and_security\04_secrets_management\before.py
.\.venv\Scripts\python.exe -B .\BP\04_configuration_and_security\04_secrets_management\after.py
```

## Qué pide la organización

La guía interna pide aplicar esta práctica según el tipo de componente. Los valores del ejemplo son didácticos y no representan parámetros productivos aprobados.

## Límites y aclaraciones

Una variable de entorno o un archivo .env no cifra automáticamente un secreto. Excluir un archivo de Git no borra credenciales ya publicadas.

## Referencias

Consulta [general](../../SOURCES.md#general) para identificar el manual de origen.
Las precisiones pendientes se registran en [CLARIFICATIONS.md](../../CLARIFICATIONS.md).
