# Inyección de dependencias

## ¿Qué es?

Es entregar a un objeto las herramientas que necesita, en lugar de que las construya dentro de su lógica.

## ¿Cómo funciona y para qué sirve?

El constructor recibe un repositorio. En una prueba puedes proporcionar uno en memoria y en otro entorno una implementación diferente.

## Qué muestra el ejemplo

La salida coincide. Aquí se explica la entrega de dependencias; [inversión de dependencias](../../../solid/05_dependency_inversion/definition.md) explica la dirección de los contratos.

Tecnología: **Python; Spring Boot realiza la composición mediante beans e inyección por constructor**.

## Cómo revisarlo o ejecutarlo

Desde la raíz del repositorio:

```powershell
.\.venv\Scripts\python.exe -B .\BP\03_architecture\02_dependency_injection\before.py
.\.venv\Scripts\python.exe -B .\BP\03_architecture\02_dependency_injection\after.py
```

## Qué pide la organización

La guía interna pide aplicar esta práctica según el tipo de componente. Los valores del ejemplo son didácticos y no representan parámetros productivos aprobados.

## Límites y aclaraciones

El ejemplo aísla una práctica. No representa una aplicación completa ni todas sus validaciones.

## Referencias

Consulta [general](../../SOURCES.md#general) para identificar el manual de origen.
Las precisiones pendientes se registran en [CLARIFICATIONS.md](../../CLARIFICATIONS.md).
