# Puertos y adaptadores

## ¿Qué es?

Es permitir que el negocio pida una operación sin conocer la herramienta externa que la realiza.

## ¿Cómo funciona y para qué sirve?

El puerto describe la capacidad y el adaptador la implementa. La composición conecta ambos. No se necesita una carpeta por cada clase para entender la dirección de las dependencias.

## Qué muestra el ejemplo

El mismo caso de uso utiliza dos adaptadores simulados. Ninguno envía correos reales.

Tecnología: **Python**.

## Cómo revisarlo o ejecutarlo

Desde la raíz del repositorio:

```powershell
.\.venv\Scripts\python.exe -B .\BP\03_architecture\03_ports_and_adapters\before.py
.\.venv\Scripts\python.exe -B .\BP\03_architecture\03_ports_and_adapters\after.py
```

## Qué pide la organización

La guía interna pide aplicar esta práctica según el tipo de componente. Los valores del ejemplo son didácticos y no representan parámetros productivos aprobados.

## Límites y aclaraciones

Clean Architecture y arquitectura hexagonal comparten ideas de independencia del negocio, pero no son nombres intercambiables para una estructura única.

## Referencias

Consulta [general](../../SOURCES.md#general) para identificar el manual de origen.
Las precisiones pendientes se registran en [CLARIFICATIONS.md](../../CLARIFICATIONS.md).
