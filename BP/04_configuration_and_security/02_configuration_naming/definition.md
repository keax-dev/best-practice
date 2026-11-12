# Nombres de configuración

## ¿Qué es?

Es usar nombres que permitan identificar al dueño, la herramienta y el atributo configurado.

## ¿Cómo funciona y para qué sirve?

La convención interna usa ACRÓNIMO_HERRAMIENTA_COMPONENTE_ATRIBUTO. El componente es opcional. GEN es un acrónimo ficticio para evitar copiar identificadores internos.

## Qué muestra el ejemplo

Se comparan nombres de parámetros de ejemplo. No hay conexiones ni credenciales.

Tecnología: **Python**.

## Cómo revisarlo o ejecutarlo

Desde la raíz del repositorio:

```powershell
.\.venv\Scripts\python.exe -B .\BP\04_configuration_and_security\02_configuration_naming\before.py
.\.venv\Scripts\python.exe -B .\BP\04_configuration_and_security\02_configuration_naming\after.py
```

## Qué pide la organización

El manual requiere acrónimo propietario, herramienta y atributo; componente opcional. No adoptes los prefijos genéricos de otros ejemplos como reemplazo de esta convención sin aclararlo.

## Límites y aclaraciones

Los prefijos son una norma organizacional, no una obligación general de Python. El nombre debe coincidir con el aprovisionado por la plataforma.

## Referencias

Consulta [general](../../SOURCES.md#general) para identificar el manual de origen.
Las precisiones pendientes se registran en [CLARIFICATIONS.md](../../CLARIFICATIONS.md).
