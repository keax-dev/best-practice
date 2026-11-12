# Separación de responsabilidades

## ¿Qué es?

Es mantener el cálculo de negocio separado de cómo recibes o presentas los datos.

## ¿Cómo funciona y para qué sirve?

Una función de negocio devuelve un resultado; otra función decide cómo mostrarlo. Cambiar la interfaz no obliga a cambiar el cálculo.

## Qué muestra el ejemplo

Las dos versiones imprimen 10. Amplía el principio en [responsabilidad única](../../../solid/01_single_responsibility/definition.md).

Tecnología: **Python; el mismo criterio se aplica a controladores y servicios de Spring Boot**.

## Cómo revisarlo o ejecutarlo

Desde la raíz del repositorio:

```powershell
.\.venv\Scripts\python.exe -B .\BP\03_architecture\01_separation_of_responsibilities\before.py
.\.venv\Scripts\python.exe -B .\BP\03_architecture\01_separation_of_responsibilities\after.py
```

## Qué pide la organización

La guía interna pide aplicar esta práctica según el tipo de componente. Los valores del ejemplo son didácticos y no representan parámetros productivos aprobados.

## Límites y aclaraciones

El ejemplo aísla una práctica. No representa una aplicación completa ni todas sus validaciones.

## Referencias

Consulta [general](../../SOURCES.md#general) para identificar el manual de origen.
Las precisiones pendientes se registran en [CLARIFICATIONS.md](../../CLARIFICATIONS.md).
